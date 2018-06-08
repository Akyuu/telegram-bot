## 简介

本项目是一个基于 Python 的 Telegram Bot，使用长轮询从服务器获取用户消息并多线程处理，目前的主要功能包括：

- 一个可扩展的处理用户消息的 Telegram Bot 框架
- 将 Sticker 转换为 png 和 jpg 格式的文件
- 将 mp4 转换为 gif 格式的文件

更多的关于本项目的相关内容还请移步 [我的博客](https://blog.sandtears.com/2018/06/06/telegram-bot-note-1.html)

## 依赖

- Python3 (基于 Python 3.6 开发)
- 位于 requirement.txt 的 python 第三方库
- ffmpeg，用于将 mp4 转换为 gif

## 部署

```
# 注：需安装 ffmpeg libffi-dev libwebp-dev git python3-pip 等相关依赖
git clone https://github.com/Akyuu/telegram-bot.git
cd telegram-bot/
pip3 install -r requirements.txt
# 之后需要修改 config.py 中 API_TOKEN 常量的值
python3 server.py
```

由于本项目未提供后台运行参数，建议用户使用 `screen` 命令运行本项目。

## 感谢

- sm.ms 图床

由于 Telegram Bot API 不支持发送 gif 文件（发送后会被强制转换为 mp4 格式），因此本项目使用 sm.ms 图床储存 gif，将图床的 url 发送给用户。
