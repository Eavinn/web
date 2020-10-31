# coding=utf-8

from flask import Blueprint, current_app, make_response
from flask_wtf.csrf import generate_csrf

html = Blueprint("html", __name__)


@html.route("/<re('.*'):file_name>")
def get_static_html(file_name):
    if file_name == "":
        file_name = "index.html"
    if file_name != "favicon.ico":
        file_name = "html/" + file_name

    response = make_response(current_app.send_static_file(file_name))

    # 生成csrf_token
    csrf_token = generate_csrf()
    response.set_cookie("csrf_token", csrf_token)

    return response
