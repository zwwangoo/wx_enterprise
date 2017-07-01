# -*- coding: utf-8 -*-
import json

from flask import render_template, request, redirect, url_for
from __init__ import client
from src.wechat.WXTool import weiTool


@client.route("/")
def index():
    return render_template("client/profile/index.html")


@client.route("/users")
def users():
    if request.method == 'GET':

        if request.args.has_key("departmentId"):
            we = weiTool()
            departmentId = request.args.get("departmentId")
            userList = we.getDepartmentUsers(departmentId)
            return render_template("client/profile/users.html", userList=userList)
        else:
            return redirect(url_for('client.departments'))


@client.route("/departments")
def departments():
    we = weiTool()
    departmentList = we.getDepartmentList()
    if len(departmentList) >= 0:
        deep_list = []
        id_list = []
        class_list = []
        for department in departmentList:
            deep_list.append(department["parentid"])
        deep_list = list(set(deep_list))
        for deep in deep_list:
            dem = {}
            departmentL = []
            for department in departmentList:

                if department["parentid"] == deep:
                    departmentL.append(department)
                    departmentList.remove(department)
                    print departmentList
                else:
                    pass
            dem[deep] = departmentL
            class_list.append(dem)
        print class_list
    return render_template("client/profile/departments.html", departmentList= departmentList)


@client.route("/sendMsg")
def sendMsg():
    we = weiTool()
    msg = request.args.get("message")
    users = request.args.get("userid")
    if msg != "":
        ret = we.sendMsg(users, msg)
        return json.dumps(ret)
    else:
        return 'null'
