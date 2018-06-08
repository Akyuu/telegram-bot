#!/usr/bin/env python3
# coding: utf-8
# author: alice12ml

from handler import TextHandler


class NotFoundHandler(TextHandler):
    def handle(self):
        self.send_message("Error: Command Not Found.")