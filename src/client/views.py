# -*- coding: utf-8 -*-
import json

from flask import render_template, request, redirect, url_for
from __init__ import client
from src.wechat.WXTool import weiTool


@client.route("/")
def index():
    return render_template("profile/index.html")


@client.route("/users")
def users():
    if request.method == 'GET':

        if request.args.has_key("departmentId"):
            we = weiTool()
            departmentId = request.args.get("departmentId")
            userList = we.getDepartmentUsers(departmentId)
            return render_template("profile/users.html", userList=userList)
        else:
            return redirect(url_for('client.departments'))


@client.route("/departments")
def departments():
    we = weiTool()
    departmentList = we.getDepartmentList()
    return render_template("profile/departments.html", departmentList= departmentList)


@client.route("/sendMsg")
def sendMsg():
    we = weiTool()
    msg = request.args.get("message")
    users = request.args.get("userid")
    if msg != "":
        ret = we.sendMsg(users, msg)
    return json.dumps(ret)