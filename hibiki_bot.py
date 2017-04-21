from telegram import ChatAction, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
import logging
import urllib3
from lxml.etree import HTML
import time
from imagetomp4 import videowriter

http = urllib3.PoolManager()

@run_async
def image(bot, update):
    def send_text(text, **kwargs):
        return bot.sendMessage(chat_id=update.message.chat_id, text = text, **kwargs)

    def send_md(text, **kwargs):
        return send_text(parse_mode=ParseMode.MARKDOWN, text = text, **kwargs)

    def send_photo(photo, **kwargs):
        return bot.sendPhoto(chat_id=update.message.chat_id, photo = photo, **kwargs)

    def send_typing(**kwargs):
        return bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING, **kwargs)

    send_typing()

    m = update.message
    image_num = 0
    if m.photo:
        left_image = m.photo[-1]
        send_md("Please send me another image as photo or file.")
        image_num = 1
    elif m.document:
        left_image = m.document
        send_md("Please send me another image as photo or file.")
        image_num = 1
    else:
        send_md("Please send me image as photo or file.")
        if image_num and m.photo:
            right_image = m.photo[-1]
            send_md("genarating.")
        elif image_num and m.document:
            right_image = m.photo[-1]
            send_md("genarating.")
        else:
            send_md("Please send me another image as photo or file.")
        return
    videowriter(left_image, right_image)
    photo = open(os.getcwd() + '/list/hibiki'+'.gif')
    if not photo:
        send_text("Sorry, we cannot find any matching")
        return
    send_photo()
    os.remove(os.getcwd() + '/list/hibiki'+'.gif')

def error(bot, update, error):
    print error

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("339651962:AAGx5buxhMFSe5oxVKkyox7RSMToU8iuvSU")
    updater.dispatcher.add_handler(MessageHandler([
        Filters.photo,
        Filters.document,

        # These will be returned with error
        Filters.text,
        Filters.sticker,
    ], image))
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
