import threading

from flask import Flask, redirect, url_for, abort, make_response, jsonify, request, session, current_app, \
    render_template, flash
from flask_mail import Mail, Message
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.routing import BaseConverter
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

from cart import cart_blu

"""
数据迁移
1.python 文件 db init
2.python 文件 db migrate -m"版本名(注释)"
3.python 文件 db upgrade 然后观察表结构
4.根据需求修改模型
5.python 文件 db migrate -m"新版本名(注释)"
6.python 文件 db upgrade 然后观察表结构
7.若返回版本,则利用 python 文件 db history查看版本号
8.python 文件 db downgrade(upgrade) 版本号

"""

app = Flask(__name__, static_folder="static", template_folder="templates")


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://meng:ml6666@192.168.49.139:3306/flask'
    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = True
    debug = True

    MAIL_SERVER = "smtp.163.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "mengliang.1992@163.com"
    MAIL_PASSWORD = "NZGHVXSDJZWQBKTP"
    MAIL_DEFAULT_SENDER = 'flask邮件<mengliang.1992@163.com>'


app.config.from_object(Config)
app.secret_key = 'silents is gold'

# app注册蓝图
app.register_blueprint(cart_blu)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

mail = Mail(app)


class Login(FlaskForm):
    username = StringField(label=u'用户：', validators=[DataRequired()])
    password = PasswordField(label=u'密码：', validators=[DataRequired(), EqualTo('re_password')])
    re_password = PasswordField(label=u'确认密码：', validators=[DataRequired()])
    submit = SubmitField(u'提交')


class Role(db.Model):
    # 定义表名
    __tablename__ = 'roles'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # backref能让user对象查到角色信息
    users = db.relationship('User', backref='role', lazy='dynamic')

    # repr()方法显示一个可读字符串
    def __repr__(self):
        return 'Role:%s' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return 'User:%s' % self.name


class RegexConverter(BaseConverter):
    # 自定义路由转换器类
    def __init__(self, url_map, regex):
        super(RegexConverter, self).__init__(url_map)
        self.regex = regex

    def to_python(self, value):
        # to_python提取参数转化并最终传递给视图函数
        return int(value)

    def to_url(self, value):
        # url_for会利用to_url的返回值拼接来生成反向解析url地址
        return str(value)


@app.template_filter("li_reverse")
def do_li_reverse(li):
    temp = list(li)
    temp.reverse()
    return temp


app.url_map.converters['id_re'] = RegexConverter


@app.route('/')
def index():
    print(request.method, request.url, request.path)
    abort(500)
    return redirect(url_for("order", order_id=123456))


@app.errorhandler(500)
def internal_server_error(e):
    # 自定义报错界面
    return '服务器搬家了'


# @app.route('/order/<int:order_id>', methods=["POST", "GET"])
# def order(order_id):
#     return "%s" % order_id

@app.route('/order/<id_re(r"\d{6}"):order_id>', methods=["POST", "GET"])
def order(order_id):
    response = make_response("%s" % order_id)
    response.status_code = 666
    response.headers['xiong'] = 'success'
    return response
    # return "%s" % order_id, 666, {"xiong": "success"}


@app.route("/set_session")
def set_cookie_session():
    response = make_response("set_session")
    response.set_cookie("name", "meng")
    session["age"] = 18
    return response


@app.route("/get_session")
def get_cookie_session():
    cookie_res = request.cookies.get("name", "")
    session_res = session.get("age", "")
    return "获取cookie和session：%s %s" % (cookie_res, session_res)


@app.route("/del_session")
def del_cookie_session():
    response = make_response("清除session")
    response.delete_cookie("name")

    # session.clear()
    session.pop("age")
    return response


@app.route('/json')
def do_json():
    hello = {"name": "stranger", "say": "hello"}
    return jsonify(**hello)
    # return jsonify(name="stranger", say="hello")


@app.route('/template')
def get_template():
    context = {
        "my_dict": {"dd": {"aa": "cc"}, "22": "dfff"},
        "my_list": [14, 18, 15],
        "my_str": 'abc'
    }
    flash(u'hello world!!!')
    return render_template('test1.html', **context)


@app.route('/wtf_form', methods=['GET', 'POST'])
def wtf_form():
    form = Login()
    if request.method == "GET":
        return render_template('wtf.html', form=form)
    else:
        if form.validate_on_submit():
            username = form.username.data
            passwd = form.password.data
            print(username, passwd)
            return "register success"
        else:
            flash(u'信息有误，请重新输入！')
            return render_template('wtf.html', form=form)


def async_send_mail():
    with app.app_context():
        # sender 发送方，recipients 接收方列表
        msg = Message("mail subject", recipients=['mengliang.1992@163.com'])
        # 邮件内容
        msg.body = "flask test --mail message"
        # 发送邮件
        mail.send(msg)


@app.route('/send_mail')
def send_mail():
    send_mail_thread = threading.Thread(target=async_send_mail)
    send_mail_thread.start()
    return "发送邮件成功"


if __name__ == '__main__':
    print(app.url_map)
    app.run()
