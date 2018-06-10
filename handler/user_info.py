#!/usr/bin/env python3
# coding: utf-8
# author: alice12ml

from handler import TextHandler
import json


class UserInfoHandler(TextHandler):
    def handle(self):
        user = self.message.get('forward_from')
        if not user:
            user = self.message.get('from')
        msg = json.dumps(user, sort_keys=True, indent=4, separators=(',', ': '))
        self.send_message(msg)
