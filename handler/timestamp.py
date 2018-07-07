#!/usr/bin/env python3
# coding: utf-8
# author: alice12ml

from handler import Handler
import datetime
import logging


class TimeStampHandler(Handler):
    @classmethod
    def response(cls, message):
        text = message.get('text', '')
        if text.startswith('/ts '):
            return TimeStampHandler(message)

    def handle(self):
        logging.info("[%s]: %s" % (self.sender, self.message['text']))
        timestamp = [i for i in self.message['text'].split(' ') if len(i) > 0]
        if len(timestamp) == 2:
            try:
                timestamp = float(timestamp[1])
                self.send_message(datetime.datetime.fromtimestamp(timestamp).isoformat(' '))
            except ValueError:
                self.send_message("/ts [float]")
        else:
            self.send_message("/ts [float]")