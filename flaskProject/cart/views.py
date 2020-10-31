from flask import render_template

from . import cart_blu


# 蓝图查找模板文件优先去项目目录temp目录查找，再去蓝图temp目录查找
@cart_blu.route("/cart_info")
def cart_info():
    return render_template("test2.html")

