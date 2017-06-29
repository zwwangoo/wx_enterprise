from flask import Blueprint

client = Blueprint(
    "client",
    __name__,
    template_folder='templates',
    static_folder='static'
)