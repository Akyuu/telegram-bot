#!/usr/bin/env python3
# coding: utf-8
# author: alice12ml

from handler import TextHandler
from time import sleep


class RepeatHandler(TextHandler):
    def handle(self):
        self.send_message(self.text)

