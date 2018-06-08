#!/usr/bin/env python3
# coding: utf-8
# author: alice12ml

import config
import requests
import logging
from handler.repeat import RepeatHandler
from handler.no_command import NotFoundHandler
from handler.sticker import StickerHandler
from handler.video import VideoHandler
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=16)
logging.basicConfig(level=logging.WARN)


def deliver_message(res):
    message = res['message']
    logging.debug(message)
    h = None

    if message.get('text'):  # 如果是文本消息
        text = message.get('text')
        if text.startswith('/ip '):  # 分发符合格式的消息
            h = NotFoundHandler(message)
        elif text.startswith('/'):  # 对于所有以 / 开头的消息进行处理
            h = NotFoundHandler(message)
        # else:  # 如果是普通的文本消息，就复读机
        #     h = RepeatHandler(message)
    elif message.get('sticker'):
        h = StickerHandler(message)
    elif message.get('document') and message['document'].get('mime_type') == 'video/mp4':
        h = VideoHandler(message)

    if h:  # 如果存在对应实现的 handler
        executor.submit(h.handle)


def main():
    offset = 0
    url = "https://api.telegram.org/bot%s/getUpdates" % config.API_TOKEN
    while True:
        payload = {'offset': offset, 'timeout': config.TIMEOUT}
        r = requests.get(url, params=payload)  # 发送请求
        r.encoding = 'utf-8'

        if r.status_code == requests.codes.ok and r.json()['ok']:  # 当请求正常时
            results = r.json()['result']
            if len(results) > 0:  # 获取到信息后分发给子线程
                offset = results[-1]['update_id'] + 1
                for res in results:
                    deliver_message(res)

        else:  # 请求出错
            logging.error(r.text)


if __name__ == "__main__":
    main()
