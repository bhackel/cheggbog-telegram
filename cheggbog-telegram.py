import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import time, os, glob, re
import webbrowser
import keyboard

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

with open('group_id.txt') as f:
    group_id = int(f.read())

def chegg(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    timestamp = time.strftime('%a %H:%M:%S')
    print(f"{timestamp}: {update.message.chat_id}: {update.message.text}")
    # Ignore messages outside of specified group
    if update.message.chat_id != group_id:
        return

    if "https://www.chegg.com/homework-help/" in update.message.text:
        # Get all Chegg homework URLs in message
        url_list = re.findall(r'(https://(?:www.)?chegg.com/homework-help/\S+)', update.message.text)
        
        # Send images for every url
        print(f' Chegging {url_list}')
        for url in url_list:
            # Open Chegg link
            update.message.reply_text("Chegging...")
            webbrowser.open(url)
            time.sleep(8)

            # Trigger the screenshot extension
            keyboard.press_and_release('alt+shift+p')

            # Get the file of the image by finding the newest one
            path = "C:/Users/[YOUR USERNAME]/Downloads/screenshots/*.jpg"
            
            # Continually check folder for a new image (assumes empty before)
            for i in range(20):
                print(f"Checking files {i}")
                files = glob.glob(path, recursive=True)
                if len(files) > 0:
                    file_loc = max(files, key=os.path.getmtime)
                    break

                time.sleep(1)
            else:
                print("Failed to find the image. Try checking the path.")
                return

            # Close the Chegg window
            keyboard.press_and_release('ctrl+w')

            # Send the image
            with open(file_loc, 'rb') as f:
                try:
                    update.message.reply_document(f)
                except Exception as e:
                    print("Errored out, trying again:", e)
                    update.message.reply_photo(f)

            # Delete the image
            os.remove(file_loc)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    with open('key.txt') as f:
        key = f.read()
    updater = Updater(key)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, chegg))

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
