#!/usr/bin/env python3
# coding: utf-8

import config
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext.filters import Filters

# handler
import datetime
import string
import random
import uuid
import subprocess
import requests
import json


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, _):
    readme = """大杂烩性质的Bot，目前功能包括：

1. 将 Sticker 转换为 png 和 jpg 格式的文件
2. 将 Telegram 自动转换而成的 mp4 转换回 gif 格式。
3. `/ts [float]` -> Unix 时间戳转换为标准时间
4. `/pw [length]` -> 生成 [length] 位随机密码
5. 其余信息将会返回消息发送者的 user_info 信息，支持转发的消息。
"""
    user = update.message.from_user
    username = user.username if user.username else user.first_name
    logging.info("[%s]: %s" % (username, update.message.text))
    update.message.reply_text(readme)


def error(update, context):
    logging.error(str(update))
    start(update, context)


def timestamp(update, context):
    user = update.message.from_user
    username = user.username if user.username else user.first_name
    logging.info("[%s]: %s" % (username, update.message.text))
    try:
        ts = float(context.args[0])
        update.message.reply_text(datetime.datetime.fromtimestamp(ts).isoformat(' '))
    except ValueError:
        update.message.reply_text("/ts [float]")


def password(update, context):
    user = update.message.from_user
    username = user.username if user.username else user.first_name
    logging.info("[%s]: %s" % (username, update.message.text))
    try:
        length = int(context.args[0])
        if length > 1024:
            raise ValueError
        alphabet = string.ascii_letters + string.digits
        update.message.reply_text("".join(random.choices(alphabet, k=length)))
    except ValueError:
        update.message.reply_text("/pw [length]")


def sticker(update, _):
    user = update.message.from_user
    username = user.username if user.username else user.first_name
    logging.info("[%s] sent a sticker." % username)
    filename = str(uuid.uuid4())
    s = update.message.sticker
    s.get_file(config.TIMEOUT).download(filename + ".webp")
    subprocess.run('ffmpeg -loglevel panic -i %s.webp %s.png' % (filename, filename), shell=True)
    with open(filename + ".png", 'rb') as f:
        update.message.reply_photo(f)
        f.seek(0)
        update.message.reply_document(f)
    subprocess.run('rm -f %s.webp %s.png' % (filename, filename), shell=True)


def animation(update, _):
    user = update.message.from_user
    username = user.username if user.username else user.first_name
    logging.info("[%s] sent a gif." % username)
    filename = str(uuid.uuid4())
    s = update.message.animation
    s.get_file(config.TIMEOUT).download(filename + ".mp4")
    subprocess.run(
        'ffmpeg -loglevel panic -i %s.mp4 -r 25 -vf "scale=iw/2:ih/2:flags=lanczos" %s.gif' % (filename, filename),
        shell=True)

    # 上传图片
    url = 'https://sm.ms/api/upload'
    gif = open(filename + '.gif', 'rb')
    files = {'smfile': gif}
    r = requests.post(url, files=files)
    code = r.json()['code']
    pic_url = r.json()['data']['url']
    if code == 'success':
        logging.info("gif url: " + pic_url)
        update.message.reply_text(pic_url)
    else:
        logging.error("request.text: " + r.text)
    gif.close()
    subprocess.run('rm -f %s.mp4 %s.gif' % (filename, filename), shell=True)


def user_info(update, _):
    user = update.message.forward_from if update.message.forward_from else update.message.from_user
    logging.info(str(update))
    msg = json.dumps(user.to_dict(), sort_keys=True, indent=4, separators=(',', ': '))
    msg = msg.encode().decode('unicode-escape')
    update.message.reply_text(msg)


def main():
    # init
    updater = Updater(token=config.API_TOKEN, use_context=True)
    dp = updater.dispatcher

    # add handler
    dp.add_error_handler(error)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ts", timestamp))
    dp.add_handler(CommandHandler("pw", password))
    dp.add_handler(MessageHandler(Filters.sticker, sticker))
    dp.add_handler(MessageHandler(Filters.animation, animation))
    dp.add_handler(MessageHandler(Filters.all, user_info))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
