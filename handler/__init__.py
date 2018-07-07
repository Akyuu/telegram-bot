#!/usr/bin/env python3
# coding: utf-8
# author: alice12ml

import requests
import config
from abc import abstractmethod


class Handler:
    def __init__(self, message):
        self.message = message
        self.chat_id = message['chat']['id']
        self.sender = message.get('from', {}).get('username', 'NoUser')

    @abstractmethod
    def handle(self):
        pass

    @classmethod
    def response(cls, message):
        return None

    def send_message(self, msg, chat_id=None, markdown=False):
        url = "https://api.telegram.org/bot%s/sendMessage" % config.API_TOKEN
        if not chat_id:
            chat_id = self.chat_id
        j = {"chat_id": chat_id, "text": msg}
        if markdown: j['parse_mode'] = 'Markdown'
        r = requests.post(url, json=j)

