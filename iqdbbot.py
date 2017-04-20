#!/usr/bin/env python

from telegram import ChatAction, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
import logging
import urllib3
from lxml.etree import HTML
import time

http = urllib3.PoolManager()

def sanitize_url(url):
    '''
    Sanitize URL for telegram:
    1. add http: to "//blah.com/blah" domains (auto scheme)
    2. append "__nouse=<timestamp>" to force telegram to re-generate the thumbnail
    @param url input url
    @return the sanitized url
    '''
    url  = ("http:" if url.startswith("//") else "") + url
    url += ("&" if "?" in url else "?") + "__nouse=%d" % int(time.time())
    return url

def iqdb(image, max=3, services=[1, 2, 3, 4, 5, 6, 11, 12, 13]):
    '''
    @param image the image binary string
    @param max max number of result
    @return a list of dicts for up to `max`: {image_url, url, site_name, size, similarity}
    '''

    fields = [("service[]", i) for i in services]
    fields.append(('file', ("a.jpg", image)))
    req = http.request("POST", "http://iqdb.org/", fields=fields)

    entries = HTML(req.data).xpath('//div[@id="pages"]/div/table')

    ret = []
    for i in entries[1:]:
        ent = {}

        # Check if image exists. If not, skip it
        if i.xpath('tr[2]/td/a/img/@src') == []: 
            continue

        ent["image_url" ] = "http://iqdb.org" + i.xpath('tr[2]/td/a/img/@src')[0]
        ent["url"       ] = sanitize_url(i.xpath('tr[2]/td/a/@href')[0])
        ent["site_name" ] = i.xpath('tr[3]/td/text()')[0].strip()
        ent["size"      ] = i.xpath('tr[4]/td/text()')[0].split(' ')[0].replace(u"\xc3\x97", u"x")
        ent["similarity"] = int(i.xpath('tr[5]/td/text()')[0].split('%')[0]) / 100.

        # Limit similarity to above 70%
        if ent["similarity"] < .7:
            continue

        ret.append(ent)

        # Finish if we got enough entries
        if len(ret) == max:
            break

    return ret

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
    if m.photo:
        file_obj = m.photo[-1]
    elif m.document:
        file_obj = m.document
    else:
        send_md("Please send me image as photo or file.")
        return 

    photo_file = bot.getFile(file_obj.file_id)
    data = http.request("GET", photo_file.file_path).data

    # Save image file for debugging
    file("debug/" + photo_file.file_path.split("/")[-1], "wb").write(data)

    results = iqdb(data, max=5, services=[1, 2, 3, 4, 5, 6])

    if results == []:
        send_text("Sorry, we cannot find any matching")
        return

    for i in results:
        #i["image"] = http.request("GET", i["image_url"]).data
        #m = send_photo(i["image_url"]) # Send directly from URL

        send_text("\n".join([
            "Url: %s" % i["url"],
            "Site: %s" % i["site_name"],
            "Dimensions: %s" %i["size"],
            "Similarity: %d %%" % int(i["similarity"] * 100),
        ]))#, reply_to_message_id=m.message_id)

def error(bot, update, error):
    print error

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("xxxxxxxxxxxxxxxx")
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
