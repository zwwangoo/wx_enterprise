from flask import Blueprint

wechat = Blueprint(
    "wechat",
    __name__,
    template_folder='templates',
    static_folder='static'
)
