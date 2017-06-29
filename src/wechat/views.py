# -*- coding: utf-8 -*-
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
    return render_template('wConfig.xml')