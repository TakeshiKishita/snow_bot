# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import json
import os
from . import generate_message
from . import send_dialogflow

def index(request):
    return HttpResponse("This is bot api.")

def callback(request):
    line_bot_api = LineBotApi('{YOUR_ACCESS_TOKEN}')
    handler = WebhookHandler('{YOUR_CHANNEL_SECRET}')

    for event in json.load(request)['events']:
        token = event['replyToken']
        usr_message = event['message']['text']
        user_id = event['source']['userId']

    ret_json = send_dialogflow.send_msg(usr_message,user_id)
    if ret_json["result"]["actionIncomplete"]:
        ret_message = ret_json["result"]["fulfillment"]["speech"]
    else:
        ret_message = generate_message.get_conditions(ret_json)

    line_bot_api.reply_message(token,TextSendMessage(text=ret_message))
    # return HttpResponse(ret_message)
