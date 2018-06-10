#!/usr/bin/env python3
# coding: utf-8
# author: alice12ml

import requests
import datetime

CHAT_ID = "you_user_id"
API_TOKEN = "your_telegram_api_token"
BWH_VEID = 'your_bwh_veid'
BWH_API_KEY = 'your_bwh_api_key'


def main():
    url = "https://api.64clouds.com/v1/getServiceInfo"
    r = requests.post(url, data={'veid': BWH_VEID, 'api_key': BWH_API_KEY})
    result = r.json()
    if result.get('error') == 0:
        msg = '你已经使用了 %.2f/%.2f GB 的流量，统计将会在 %s 重置'
        data_plan = float(result['plan_monthly_data']) / 1024 / 1024 / 1024
        data_used = float(result['data_counter']) / 1024 / 1024 / 1024
        if result.get('monthly_data_multiplier'):
            m = result.get('monthly_data_multiplier')
            data_plan = data_plan * m
            data_used = data_used * m
        reset_date = datetime.datetime.fromtimestamp(result['data_next_reset']).strftime('%Y-%m-%d')
        msg = msg % (data_used, data_plan, reset_date)
    else:
        msg = '获取 VPS 已使用流量出错'
    send_message('[bwh.py] ' + msg)


def send_message(msg, chat_id=CHAT_ID, markdown=False):
    url = "https://api.telegram.org/bot%s/sendMessage" % API_TOKEN
    j = {"chat_id": chat_id, "text": msg}
    if markdown: j['parse_mode'] = 'Markdown'
    r = requests.post(url, json=j)


if __name__ == '__main__':
    main()