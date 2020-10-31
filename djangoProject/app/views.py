from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from datetime import date, datetime

from django.urls import reverse
from django.utils.timezone import now
from django.views.defaults import page_not_found

from app.models import Department, User, Area
from app.add_func import verify_code
from djangoProject import settings

# Create your views here.


def index(request):
    """render渲染"""
    data = {
        'name': 'django',
        'sex': '男',
        'age': 25,
        'salary': 10000,
        'hobby': ['python', 'c/c++', 'java'],
        # 时间过滤器
        'my_date': now(),
        # html会把具有特殊含义的字符转成没有特殊含义的字符串，需要防止转义
        'my_html': '<font color="red">红色</font>',

    }
    # alt+Enter快速导包
    # template = loader.get_template('index.html')
    # html = template.render(data, request)
    # return HttpResponse(html)
    return render(request, 'index.html', data)


def show_deps(request):
    # departments = Department.objects.filter(is_delete=False)
    departments = Department.objects.all()
    data = {'departments': departments}
    return render(request, 'show_deps.html', data)


def show_dep(request, dep_id):
    """orm基本使用"""

    department = Department.objects.get(id=dep_id)
    employees = department.employee_set.all()
    data = {
        'department': department,
        'employees': employees
    }
    return render(request, 'show_dep.html', data)


def add_dep(request):
    """新增部门"""
    # d = Department()
    # d.name = '财务部'
    # d.create_date = date(2018, 1, 1)
    # d.save()
    Department.objects.create_dep('财务部', date(2018, 1, 1))
    return redirect('/show_deps')


def del_dep(request, dep_id):
    """删除部门"""
    Department.objects.filter(id=dep_id).update(is_delete=True)
    # reverse函数反向解析软编码
    return redirect(reverse("app:show_departments"))
    # return redirect('/show_deps')


def get(request):
    print(request.path, request.method, request.encoding)
    a = request.GET.get('a')
    b = request.GET.getlist('b')
    text = ('a = %s <br/>b = %s' % (a, b))
    return HttpResponse(text)


def post(request):
    """post表单"""
    if not request.session.get('username'):
        return redirect('/login')
    return render(request, 'post.html')


def do_post(request):
    """post提交"""
    username = request.POST.get('username')
    password = request.POST.get('password')
    gender = request.POST.get('gender')
    hobbies = request.POST.getlist('hobby')

    text = (
            'username = %s <br/>'
            'password = %s <br/>'
            'gender = %s <br/>'
            'hobbies = %s <br/>'
            % (username, password, gender, hobbies))
    return HttpResponse(text)


def json(request):
    print(request.META.get('REMOTE_ADDR'))
    return render(request, 'json.html')


def get_employee(request):
    """get employee info"""
    context = {
        'name': 'Jack',
        'age': 20,
        'sex': '男',
        'salary': 10000,
        'comment': '无'
    }
    return JsonResponse(context)


def set_cookie(request):
    """cookie若不设置有效时长，默认关闭浏览器删除"""
    response = HttpResponse('设置cookie')
    response.set_cookie('user_name', 'meng', 60*10)
    response.set_cookie('goods_ids', '1,2,3')
    return response


def get_cookie(request):
    user_name = request.COOKIES.get('user_name')
    goods_id = request.COOKIES.get('goods_ids')
    return HttpResponse('user_name=%s, goods_id=%s' % (user_name, goods_id))


def set_session(request):
    """设置session，session使用base64编码"""
    request.session['user_name'] = 'MENG'
    request.session['verify_code'] = '666'
    # value单位为s, 如果value为0关闭浏览器时过期，如果value为None则2 week后过期
    # request.session.set_expiry(5)
    # request.session.clear()
    return HttpResponse('设置session')


def get_session(request):
    """获取session"""
    user_name = request.session.get('user_name')
    verify_code = request.session.get('verify_code')
    return HttpResponse('user_name=%s, verify_code=%s' % (user_name, verify_code))


def inherit(request):
    """进入模板继承演示界面"""
    return render(request, 'child.html')


def login(request):
    """进入登录界面"""
    return render(request, 'login.html')


def do_login(request):
    """处理登录操作"""

    # 处理登录操作
    username = request.GET.get('username')
    password = request.GET.get('password')

    if username == 'admin' and password == '123':
        # 登录成功,进入发帖界面
        request.session['username'] = 'admin'
        return redirect('/post')
    else:
        # 登录失败,回到登录界面
        return redirect('/login')


def create_verify_code(request):
    rand_str, pic = verify_code.create_verify_code()
    request.session['verifycode'] = rand_str
    return HttpResponse(pic, 'image/png')


def show_verify_code(request):
    """进入显示验证码界面"""
    return render(request, 'show_verify_code.html')


def do_verify(request):
    code = request.POST.get('verify_code')
    code2 = request.session.get('verifycode')
    if code.upper() == code2.upper():
        return HttpResponse('校验通过')
    else:
        return HttpResponse('校验不通过')


def add_user(request):
    return render(request, 'add_user.html')


def do_add_user(request):
    """新增一个用户"""

    upload_file = request.FILES.get('avatar')
    if not upload_file:
        return render(request, 'add_user.html', {'errmsg': '请选择用户头像'})
    # 文件存储路径
    file_path = settings.MEDIA_ROOT + '/app/' + upload_file.name
    with open(file_path, 'wb') as file:
        # chucks循环写入文件内容
        for data in upload_file.chunks():
            file.write(data)

    user = User()
    user.avatar = '/app/' + upload_file.name
    user.name = request.POST.get('name')
    user.save()

    return redirect('/show_images')


def show_images(request):
    """'显示所有用户的头像"""
    # 查询所有用户
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'show_images.html', context)


def show_page(request, page_num=1):
    """显示分页数据"""

    # 查询所有的省份
    areas = Area.objects.filter(parent_id=1)
    paginator = Paginator(areas, 10)
    # print(paginator.num_pages)    # 总共有多少页
    # print(paginator.count)        # 总共有多少条数据
    # print(paginator.page_range)   # 页码列表

    page = paginator.page(page_num)
    # print(page.number)            # 当前第几页
    # print(page.paginator)         # 当前分页的paginator对象
    # print(page.has_next())               # 是否有下一页
    # print(page.next_page_number())       # 下一页的页码
    # print(page.has_previous())           # 是否有上一页
    # print(page.previous_page_number())   # 上一页的页码

    data = {'page': page}
    return render(request, 'show_page.html', data)


def show_areas(request):
    # 查询所有的省份数据
    provinces = Area.objects.filter(parent_id=1)
    context = {
        'provinces': provinces,
    }
    return render(request, 'show_areas.html', context)


def get_children(request, pid):
    """
    获取下级区域数据
    :param request:
    :param pid: 上级区域的id
    """
    areas = Area.objects.filter(parent_id=pid)

    my_list = []
    for area in areas:
        my_list.append((area.id, area.title))

    # 注意： 字典中不能有对象, 否则无法转换成json字符串
    return JsonResponse({'children': my_list})
