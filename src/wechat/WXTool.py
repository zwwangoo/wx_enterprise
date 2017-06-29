# -*- coding: utf-8 -*-
import json
import os
import urllib2

import xml.etree.cElementTree as ET

from src.wechat.WXBizMsgCrypt import WXBizMsgCrypt
from src.wechat.models import WechatError


class weiTool(object):
    def __init__(self):
        basePath = os.path.dirname(os.path.dirname(__file__))
        informationStateXml = os.path.join(
            basePath, "wechat/templates/wConfig.xml")
        print informationStateXml
        tree = ET.ElementTree(file=informationStateXml)
        self.sToken = tree.find("sToken").text
        self.sEncodingAESKey = tree.find("sEncodingAESKey").text
        self.sCorpID = tree.find("sCorpID").text
        self.sCorpSecret = tree.find("sCorpSecret").text

    @property
    def get_wxcpt(self):
        wxcpt = WXBizMsgCrypt(self.sToken, self.sEncodingAESKey, self.sCorpID)
        return wxcpt

    # 获取access_token函数
    def getToken(self):
        req = urllib2.Request('https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' +
                              self.sCorpID + '&corpsecret=' + self.sCorpSecret)
        response = urllib2.urlopen(req)
        the_page = response.read()
        return json.loads(the_page)['access_token']

    # 部门列表
    def getDepartmentList(self):
        req = urllib2.Request(
            'https://qyapi.weixin.qq.com/cgi-bin/department/list?access_token=' + self.getToken())
        response = urllib2.urlopen(req)
        the_page = response.read()
        return json.loads(the_page)['department']

    # 部门所有成员
    def getDepartmentUsers(self, departmentId):
        req = urllib2.Request(
            'https://qyapi.weixin.qq.com/cgi-bin/user/simplelist?access_token=' +
            self.getToken() +
            '&department_id=' + departmentId +
            '&fetch_child=0&status=1'
        )
        response = urllib2.urlopen(req)
        the_page = response.read()
        return  json.loads(the_page)['userlist']

    # 根据code获取用户信息
    def getuserinfo(self, code):
        access_token = self.getToken()
        urlreq = urllib2.Request(
            'https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token=' + access_token + '&code=' + code)
        urlresponse = urllib2.urlopen(urlreq)
        the_page = urlresponse.read()
        jsonreturn = json.loads(the_page)
        if jsonreturn.has_key('UserId'):
            return jsonreturn['UserId']
        return None

    # # 添加用户
    def saveuser(self, username, userid, usersex, userphone):
        access_token = self.getToken()
        postdata = {}
        postdata["userid"] = userid
        postdata["name"] = username
        postdata["department"] = [6]  # 教师组编号
        postdata["mobile"] = userphone
        postdata["gender"] = usersex
        encodedata = json.dumps(postdata, ensure_ascii=False)
        urlreq = urllib2.Request(
            "https://qyapi.weixin.qq.com/cgi-bin/user/create?access_token=" + access_token, encodedata)
        urlresponse = urllib2.urlopen(urlreq)
        the_page = urlresponse.read()
        jsonreturn = json.loads(the_page)
        if jsonreturn.has_key("errcode"):
            if jsonreturn["errcode"] != 0:
                raise WechatError("保存到微信发生错误，错误编码是"+jsonreturn["errcode"])
        return jsonreturn["errmsg"]

    # # 给指定用户发送消息
    def sendMsg(self, touser, content):
        access_token = self.getToken()

        # 这里需要说明：为什么不使用json.dumps(): 因为在发送消息时，消息格式如下这样：{ { }, ,}，
        # 里面有双层{}, ensure_ascii=False，不能改变里面一层的编码，
        # 所以一直报错 "errcode": 40008, "errmsg": "invalid message type"。
        # 这里用字符串拼接后，在装换编码格式就行，
        postdata = '{"text": {"content": "%s"}, "agentid": "%s", "touser": "%s", "msgtype": "text"}' \
                       % (content, self.sCorpID, touser)
        encodedata = postdata.encode('UTF-8')

        urlreq = urllib2.Request(
            "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + access_token, encodedata)
        urlresponse = urllib2.urlopen(urlreq)
        the_page = urlresponse.read()
        jsonreturn = json.loads(the_page)
        return jsonreturn