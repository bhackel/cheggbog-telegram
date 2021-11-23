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
            time.sleep(5)

            # Take a screenshot using the extension
            keyboard.press_and_release('alt+shift+p')
            # Textbook pages take much longer to capture
            if "/homework-help/questions-and-answers/" in url:
                time.sleep(7)
            else:
                time.sleep(10)

            # Close the Chegg window
            keyboard.press_and_release('ctrl+w')

            # Get the file of the image by finding the newest one
            path = "C:/Users/bryce/Downloads/screenshots/*"
            file_loc = max(glob.glob(path, recursive=True), key=os.path.getmtime)

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
