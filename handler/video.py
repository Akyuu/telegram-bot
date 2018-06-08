#!/usr/bin/env python3
# coding: utf-8
# author: alice12ml

from handler import Handler
from config import API_TOKEN
import requests
import logging
import subprocess
import uuid


class VideoHandler(Handler):
    def handle(self):
        logging.debug(self.message)
        file_id = self.message['document']['file_id']

        # 获取 file_path
        url = 'https://api.telegram.org/bot%s/getFile' % API_TOKEN
        r = requests.get(url, {'file_id': file_id})
        if r.status_code == requests.codes.ok and r.json()['ok']:
            file_path = r.json()['result']['file_path']
            logging.debug("Video: file_path" + file_path)

            # 下载 sticker 对应的 mp4 文件并保存
            filename = str(uuid.uuid1())
            url = 'https://api.telegram.org/file/bot%s/%s' % (API_TOKEN, file_path)
            r = requests.get(url)
            with open(filename + ".mp4", "wb") as f:
                f.write(r.content)

            # 利用 ffmpeg 转换文件
            # subprocess.run('ffmpeg -i %s.mp4 -r 25 "frames/%s-%%03d.jpg"' % (file_id, file_id), shell=True)
            # subprocess.run('convert -delay 4 -loop 1 frames/%s-*.jpg %s.gif' % (file_id, file_id), shell=True)
            # subprocess.run('rm -f frames/%s-*.jpg' % file_id, shell=True)
            subprocess.run('ffmpeg -i %s.mp4 -r 25 -vf scale=270:-1 %s.gif' % (filename, filename), shell=True)
            logging.debug("Video: convert video to gif.")

            # 上传文件，由于 Telegram 服务器会自动将 gif 转换为 mp4，故上传到图床
            url = 'https://sm.ms/api/upload'
            gif = open(filename+'.gif', 'rb')
            files = {'smfile': gif}
            r = requests.post(url, files=files)
            code = r.json()['code']
            pic_url = r.json()['data']['url']
            if code == 'success':
                logging.debug("Video: upload gif to sm.ms")
                # 发送图床链接
                self.send_message(pic_url)
                # 删除缓存文件
            else:
                logging.error("Video: " + r.text)

            gif.close()
            subprocess.run('rm -f %s.mp4 %s.gif' % (filename, filename), shell=True)
        else:
            logging.error("Video: " + r.text)
