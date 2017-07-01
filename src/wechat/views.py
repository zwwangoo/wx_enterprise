# -*- coding: utf-8 -*-
import json
import random

from flask import redirect, request, make_response, render_template
import hashlib
from __init__ import wechat
from src.wechat.WXTool import weiTool


@wechat.route("/validation", methods=['GET', 'POST'])
def validation():
    if request.method == 'GET':
        getData = request.args
        msg_signature = getData.get("msg_signature")
        timestamp = getData.get("timestamp")
        nonce = getData.get("nonce")
        echostr = getData.get("echostr")
        wxcpt = weiTool()
        ret, sEchoStr = wxcpt.get_wxcpt.VerifyURL(msg_signature, timestamp, nonce, echostr)
        return make_response(sEchoStr)

    elif request.method == 'POST':
        print request.args
        return make_response("hello")


@wechat.route("/xml")
def send():
    return render_template('wechat/wConfig.xml')


@wechat.route("/")
def index():
    # data = []
    # for i in range(30):
    #     data[i] = random.seed(a=None, version=2)
    data = {'1': 151, '2': 23, '3': 152.6, '4': 15, '5':125, '6': 12, '7': 52.6}
    return render_template("wechat/test.html", data=json.dumps(data, encoding='utf-8'))