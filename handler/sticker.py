#!/usr/bin/env python3
# coding: utf-8
# author: alice12ml

from handler import Handler
from config import API_TOKEN
import requests
import logging
import subprocess
import uuid


class StickerHandler(Handler):
    @classmethod
    def response(cls, message):
        if message.get('sticker'):
            return StickerHandler(message)

    def handle(self):
        file_id = self.message['sticker']['file_id']
        set_name = self.message['sticker'].get('set_name', 'NoSetName')
        logging.info("[%s] send a sticker from %s." % (self.sender, set_name))

        # 获取 file_path
        url = 'https://api.telegram.org/bot%s/getFile' % API_TOKEN
        r = requests.get(url, {'file_id': file_id})
        if r.status_code == requests.codes.ok and r.json()['ok']:
            file_path = r.json()['result']['file_path']
            logging.debug("Sticker: file_path"+file_path)

            # 下载 sticker 对应的 webp 文件并保存
            filename = str(uuid.uuid1())
            url = 'https://api.telegram.org/file/bot%s/%s' % (API_TOKEN, file_path)
            r = requests.get(url)
            with open(filename + ".webp", "wb") as f:
                f.write(r.content)

                # 利用 ffmpeg 转换文件
                subprocess.run('ffmpeg -loglevel panic -i %s.webp %s.png' % (
                filename, filename), shell=True)
                logging.debug("convert webp to png.")

            with open(filename + '.png', 'rb') as png:
                # 上传文件，由于 Telegram 服务器会自动将图片转换为 jpg，故通过 sendDocument 发送 png 版
                url = 'https://api.telegram.org/bot%s/sendDocument' % API_TOKEN
                files = {'document': (png.name, png, 'image/png')}
                r = requests.post(url, {"chat_id": self.chat_id}, files=files)
                logging.debug("send png file.")

                # 发送jpg版本图片
                url = 'https://api.telegram.org/bot%s/sendPhoto' % API_TOKEN
                files = {'photo': (png.name, png, 'image/png')}
                r = requests.post(url, {"chat_id": self.chat_id}, files=files)
                logging.debug("send jpg photo.")

            # 删除缓存文件
            subprocess.run('rm -f %s.webp %s.png' % (filename, filename), shell=True)
        else:
            logging.error("request.text: " + r.text)