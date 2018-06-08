#!/usr/bin/env python3
# coding: utf-8
# author: alice12ml

from handler import Handler
from config import API_TOKEN
import requests
import logging
import webp
from io import BytesIO
from PIL import Image


class StickerHandler(Handler):
    def handle(self):
        file_id = self.message['sticker']['file_id']

        # 获取 file_path
        url = 'https://api.telegram.org/bot%s/getFile' % API_TOKEN
        r = requests.get(url, {'file_id': file_id})
        if r.status_code == requests.codes.ok and r.json()['ok']:
            file_path = r.json()['result']['file_path']
            logging.debug("Sticker: file_path"+file_path)

            # 下载 sticker 对应的 webp 文件
            url = 'https://api.telegram.org/file/bot%s/%s' % (API_TOKEN, file_path)
            r = requests.get(url)
            webp_data = webp.WebPData.from_buffer(r.content)  # 从下载的文件流生成 webp 数据

            # 将 webp 数据转换为 png 数据
            png = Image.fromarray(webp_data.decode())

            # 上传文件，由于 Telegram 服务器会自动将图片转换为 jpg，故通过 sendDocument 发送 png 版
            url = 'https://api.telegram.org/bot%s/sendDocument' % API_TOKEN
            b = BytesIO()
            png.save(b, format='png')
            b = b.getvalue()
            files = {'document': (file_id+".png", b, 'image/png')}
            r = requests.post(url, {"chat_id": self.chat_id}, files=files)
            logging.debug("Sticker: send png file.")

            # 发送jpg版本图片
            url = 'https://api.telegram.org/bot%s/sendPhoto' % API_TOKEN
            files = {'photo': (file_id + ".png", b, 'image/png')}
            r = requests.post(url, {"chat_id": self.chat_id}, files=files)
            logging.debug("Sticker: send jpg photo.")
        else:
            logging.error("Sticker: " + r.text)