#!/usr/bin/env python3
# coding: utf-8
# author: alice12ml

import config
import requests
import logging
from handler import Handler
from handler.timestamp import TimeStampHandler
from handler.video import VideoHandler
from handler.sticker import StickerHandler
from handler.user_info import UserInfoHandler
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=16)
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] [%(filename)s] [%(funcName)s]'
                                               '\n%(message)s\n')

handler_list = [TimeStampHandler, StickerHandler, VideoHandler, UserInfoHandler]


def deliver_message(res):
    # 只处理 message
    if not res.get('message'):
        return
    message = res.get('message')
    logging.debug(message)

    # 交由不同Handler处理
    for handler in handler_list:
        h = handler.response(message)
        if isinstance(h, Handler):
            h.handle()
            break


def main():
    offset = 0
    url = "https://api.telegram.org/bot%s/getUpdates" % config.API_TOKEN
    while True:
        payload = {'offset': offset, 'timeout': config.TIMEOUT}
        try:
            r = requests.get(url, params=payload)  # 发送请求
            if r.status_code == requests.codes.ok and r.json()['ok']:  # 当请求正常时
                results = r.json()['result']
                if len(results) > 0:  # 获取到信息后分发给子线程
                    offset = results[-1]['update_id'] + 1
                    executor.map(deliver_message, results)

            else:  # 请求出错
                logging.error("request.text: " + r.text)
        except requests.exceptions.ConnectionError:
            logging.error('requests.exceptions.ConnectionError')


if __name__ == "__main__":
    main()
