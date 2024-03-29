import glob
import logging
import os
import re
import time
import webbrowser

from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from pynput.keyboard import Key, Controller

keyboard = Controller()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Read the id of the group that this bot will work in
with open('group_id.txt') as f:
    group_id = int(f.read())


async def chegg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Log the message
    timestamp = time.strftime('%a %H:%M:%S')
    print(f"{timestamp}: {update.message.chat_id}: {update.message.text}")
    # Ignore messages outside the specified group
    if update.effective_chat.id != group_id:
        return

    # Search for Chegg links in messages
    url_list = re.findall(r'chegg\.com/homework-help/\S+', update.message.text)
    if len(url_list) > 0:
        # Send images for every url
        print(f' Chegging {url_list}')
        for url in url_list:
            # Open Chegg link
            await update.message.reply_text("Chegging...")
            webbrowser.open(f'https://{url}')
            time.sleep(12)

            # Trigger the screenshot extension
            with keyboard.pressed(Key.alt), keyboard.pressed(Key.shift):
                keyboard.press('p')
                keyboard.release('p')

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
            with keyboard.pressed(Key.ctrl):
                keyboard.press('w')
                keyboard.release('w')

            # Send the image
            with open(file_loc, 'rb') as f:
                try:
                    await update.message.reply_document(f)
                except Exception as e:
                    print("Errored out, trying again:", e)
                    await update.message.reply_photo(f)

            # Delete the image
            os.remove(file_loc)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    with open('key.txt') as f:
        key = f.read().strip()

    application = ApplicationBuilder().token(key).build()
    
    chegg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chegg)
    
    application.add_handler(chegg_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
