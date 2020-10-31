import re
import pymysql
import urllib.parse as url

URL_FUNC_DICT = dict()


class Mysql(object):
    def __init__(self):
        self.db = pymysql.connect(host='192.168.49.134', port=3306, user='meng', password='ml6666',
                                  database='stock_db', charset='utf8')
        self.cursor = self.db.cursor()

    def __del__(self):
        self.cursor.close()
        self.db.close()


def route(request_url):
    def func_out(func):
        URL_FUNC_DICT[request_url] = func

        def func_in():
            func()
        return func_in
    return func_out


@route("/index.html")
def index(ret):
    with open("./templates/index.html") as f:
        content = f.read()

    sql = "select * from info;"
    mysql = Mysql()
    mysql.cursor.execute(sql)
    stock_info = mysql.cursor.fetchall()

    html_template = """
               <tr>
                   <td>%d</td>
                   <td>%s</td>
                   <td>%s</td>
                   <td>%s</td>
                   <td>%s</td>
                   <td>%s</td>
                   <td>%s</td>
                   <td>%s</td>
                   <td>
                       <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="%s">
                   </td>
                   </tr>"""
    html = ""

    for info in stock_info:
        html += html_template % (info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[1])

    content = re.sub(r'\{%content%\}', html, content)
    return content


@route("/center.html")
def center(ret):
    with open("./templates/center.html") as f:
        content = f.read()
    sql = "select code,short,chg,turnover,price,highs,note_info from info inner join focus on info.id=focus.id;"
    mysql = Mysql()
    mysql.cursor.execute(sql)
    stock_info = mysql.cursor.fetchall()

    html_template = """
               <tr>
                   <td>%s</td>
                   <td>%s</td>
                   <td>%s</td>
                   <td>%s</td>
                   <td>%s</td>
                   <td>%s</td>
                   <td>%s</td>
                   <td>
                       <a type="button" class="btn btn-default btn-xs" href="/update/%s.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
                   </td>
                   <td>
                       <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="%s">
                   </td>
               </tr>
               """
    html = ""

    for info in stock_info:
        html += html_template % (info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[0], info[0])

    content = re.sub(r'\{%content%\}', html, content)
    return content


@route(r"/add/(\d+)\.html")
def add(ret):
    stock_id = ret.group(1)
    mysql = Mysql()

    sql = "select * from info where code=%s;"
    mysql.cursor.execute(sql, (stock_id,))
    if not mysql.cursor.fetchall():
        return "没有这只股票"

    sql = "select * from focus where id=(select id from info where code=%s);"
    mysql.cursor.execute(sql, (stock_id,))
    if mysql.cursor.fetchall():
        return "股票已经被关注过"

    sql = "insert into focus(id) (select id from info where code=%s);"
    mysql.cursor.execute(sql, (stock_id,))
    mysql.db.commit()
    return "%s 添加成功！！" % stock_id


@route(r"/del/(\d+)\.html")
def delete(ret):
    stock_id = ret.group(1)
    mysql = Mysql()

    sql = "delete from focus where id=(select id from info where code=%s);"
    mysql.cursor.execute(sql, (stock_id,))
    mysql.db.commit()
    return "%s 删除成功！！" % stock_id


@route(r"/update/(\d+)\.html")
def update(ret):
    stock_id = ret.group(1)
    with open("./templates/update.html") as f:
        content = f.read()
    content = re.sub(r'\{%code%\}', stock_id, content)

    mysql = Mysql()
    sql = "select note_info from focus where id=(select id from info where code=%s);"
    mysql.cursor.execute(sql, (stock_id,))
    ret = mysql.cursor.fetchone()

    content = re.sub(r'\{%note_info%\}', ret[0], content)
    return content


@route(r"/update/(\d+)/(.*)\.html")
def update(ret):
    # unquote对url中文解码
    stock_id, note_info = ret.group(1), url.unquote(ret.group(2))
    mysql = Mysql()

    sql = "update focus set note_info=%s where id=(select id from info where code=%s);"
    mysql.cursor.execute(sql, (note_info, stock_id))
    mysql.db.commit()
    return "更新成功！！"


def application(environ, start_response):
    """符合wsgi协议的接口"""
    file_name = environ["url"]
    for rule, func in URL_FUNC_DICT.items():
        ret = re.match(rule, file_name)
        if ret:
            start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])
            return func(ret)
    else:
        start_response('404 Not Found', [('Content-Type', 'text/html;charset=utf-8')])
        return "%s 没有对应的函数" % file_name

