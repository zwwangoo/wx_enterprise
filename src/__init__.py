# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from wechat.views import wechat
from client.views import client
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Create beautiful Javascript charts with minimal code
# https://github.com/mher/chartkick.py
app.jinja_env.add_extension("chartkick.ext.charts")

app.config.from_object('config')

app.register_blueprint(client, url_prefix='/client')
app.register_blueprint(wechat, url_prefix='/wechat')

# db = SQLAlchemy(app)