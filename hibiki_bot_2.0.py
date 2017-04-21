from telegram import ChatAction, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
# from telegram.ext.dispatcher import run_async
import logging
import urllib3
import os
import PIL
# from lxml.etree import HTML
# import time
from imagetomp4 import videowriter



PHOTO = 1


# def start(bot, update):
#     update.message.reply_text('hellow')
#
#     return PHOTO1

def photo1(bot, update):
    user = update.message.from_user
    chat_id = update.message.chat_id
    image = bot.getFile(update.message.photo[-1].file_id)
    image.download(os.getcwd() + '/download/'+'left_image.jpg')
    update.message.reply_text('hellow!\ngot first image, please send me another')

    return PHOTO

def photo2(bot, update):
    user = update.message.from_user
    chat_id = update.message.chat_id
    image = bot.getFile(update.message.photo[-1].file_id)
    image.download(os.getcwd() + '/download/'+'right_image.jpg')
    update.message.reply_text('got second image, genarating......')
    left_image= PIL.Image.open(os.getcwd() + '/download/'+'left_image.jpg')
    right_image= PIL.Image.open(os.getcwd() + '/download/'+'right_image.jpg')
    videowriter(left_image, right_image)

    bot.sendDocument(chat_id=chat_id, document=open(os.getcwd() + '/list/hibiki.gif', 'rb'))

    return ConversationHandler.END

def cancel(bot, update):

    update.message.reply_text('Bye! I hope we can talk again some day.')

    return ConversationHandler.END

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))




def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("339651962:AAGx5buxhMFSe5oxVKkyox7RSMToU8iuvSU")


    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.photo, photo1)],

        states={


            # PHOTO1: [MessageHandler(Filters.photo, photo1)],


            PHOTO: [MessageHandler(Filters.photo, photo2)]




        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)



    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
