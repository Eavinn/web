import re

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django_redis import get_redis_connection
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired

from apps.goods.models import GoodsSKU
from apps.orders.models import OrderInfo, OrderGoods
from apps.users.models import User, Address
from apps.celery_tasks.tasks import send_active_email
from util.common import LoginRequiredMixin


def register(request):
    """进入注册界面 """
    return render(request, 'register.html')


def do_register(request):
    """处理注册逻辑"""

    # 获取请求参数
    # 用户名, 密码, 确认密码, 邮箱, 勾选用户协议
    username = request.POST.get('username')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    email = request.POST.get('email')
    allow = request.POST.get('allow')   # 是否勾选的用户协议

    # 校验参数合法性
    # 逻辑判断 0 0.0 '' None [] () {}  -> False
    # all: 所有的变量都为True, all函数才返回True, 否则返回False
    if not all([username, password, password2, email]):
        return render(request, 'register.html', {'message': '参数不完整'})

    # 判断两次输入的密码是否正确
    if password != password2:
        return render(request, 'register.html', {'message': '两次输入的密码不一致'})

    # 判断是否勾选了用户协议
    if allow != 'on':
        return render(request, 'register.html', {'message': '请先同意用户协议'})

    # 判断邮箱格式是否正确
    if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, 'register.html', {'message': '邮箱格式不正确'})

    # 业务处理：保存注册用户到数据库表
    # create_user 是django提供的方法,
    # 注意：参数先后顺序，会自动对密码进行加密处理
    user = None
    try:
        user = User.objects.create_user(username, email, password)
    except IntegrityError:  # 数据完整性错误
        # 判断注册用户是否已经存在
        return render(request, 'register.html', {'errmsg': '用户已存在'})

    # 修改用户的激活状态为未激活
    user.is_active = False
    user.save()

    # 发送激活邮件
    token = user.generate_active_token()
    # 同步发送，会阻塞 RegisterView.send_active_email(username, email, token)
    # 使用celery异步发送激活邮件
    send_active_email.delay(username, email, token)

    # 响应请求,返回html页面
    return redirect(reverse("users:login"))


class RegisterView(View):
    """类视图：处理注册"""
    @staticmethod
    def get(request):
        """处理GET请求，返回注册页面"""
        res = register(request)
        return res

    @staticmethod
    def post(request):
        """处理POST请求，实现注册逻辑"""
        res = do_register(request)
        return res


class ActiveView(View):
    @staticmethod
    def get(request, token: str):
        """
        激活注册用户
        :param request:
        :param token: 对{'confirm':用户id}字典进行加密后的结果
        :return:
        """
        # 解密数据，得到字典
        dict_data = dict()
        try:
            s = TimedJSONWebSignatureSerializer(
                settings.SECRET_KEY, 3600*24)
            dict_data = s.loads(token.encode())     # type: dict
        except SignatureExpired:
            # 激活链接已经过期
            return HttpResponse('激活链接已经过期')

        # 获取用id
        user_id = dict_data.get('confirm')

        # 激活用户，修改表字段is_active=True
        User.objects.filter(id=user_id).update(is_active=True)

        # 响应请求
        return redirect(reverse("users:login"))


class LoginView(View):

    def get(self, request):
        """进入登录界面"""
        return render(request, 'login.html')

    def post(self, request):
        """处理登录操作"""

        # 获取登录参数
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 校验参数合法性
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '请求参数不完整'})

        # 通过 django 提供的authenticate方法，
        # 验证用户名和密码是否正确, django2.0以上版本未激活的用户无法获取到
        user = authenticate(username=username, password=password)

        # 用户名或密码不正确
        if user is None:
            print(user)
            return render(request, 'login.html', {'errmsg': '用户名或密码不正确'})

        if not user.is_active:  # 注册账号未激活
            # 用户未激活
            return render(request, 'login.html', {'errmsg': '请先激活账号'})

        # 通过django的login方法，保存登录用户状态（使用session）
        login(request, user)

        # 获取是否勾选'记住用户名'
        remember = request.POST.get('remember')

        # 判断是否是否勾选'记住用户名'
        if remember != 'on':
            # 没有勾选，设置session数据有效期为关闭浏览器后失效
            request.session.set_expiry(0)
        else:
            # 已勾选，设置session数据有效期为两周
            request.session.set_expiry(None)

        # 登陆成功，根据next参数决定跳转方向
        next = request.GET.get('next')
        if next is None:
            # 如果是直接登陆成功，就重定向到首页
            return redirect(reverse('goods:index'))
        else:
            # 如果是用户中心重定向到登陆页面，就回到用户中心
            return redirect(next)


class LogoutView(View):
    """退出逻辑"""

    def get(self, request):
        # 由Django用户认证系统完成：会清理cookie和session,request参数中有user对象
        logout(request)
        return redirect(reverse('goods:index'))


class UserInfoView(View):
    """用户中心:个人信息界面"""

    def get(self, request):

        data = {'which_page': 1}
        return render(request, 'user_center_info.html', data)


class UserOrderView(View):
    """用户中心人--订单显示界面"""

    def get(self, request, page_no):

        # 查询当前登录用户所有的订单(降序排列)
        orders = OrderInfo.objects.filter(
            user=request.user).order_by('-create_time')
        for order in orders:
            # 查询某个订单下所有的商品
            order_skus = OrderGoods.objects.filter(order=order)
            for order_sku in order_skus:
                # 循环每一个订单商品，计算小计金额
                order_sku.amount = order_sku.price * order_sku.count

            # 新增三个实例属性
            # 订单状态
            order.status_desc = OrderInfo.ORDER_STATUS.get(order.status)
            # 实付金额
            order.total_pay = order.trans_cost + order.total_amount
            # 订单商品
            order.order_skus = order_skus

        # 创建分页对象
        # 参数2：每页显示两条
        paginator = Paginator(orders, 1)
        # 获取page对象
        try:
            page = paginator.page(page_no)
        except EmptyPage:  # 没有获取到分页
            page = paginator.page(1)

        context = {
            'which_page': 2,
            'page': page,
            'page_range': paginator.page_range,  # 页码列表[1,2,3,4]
        }

        return render(request, 'user_center_order.html', context)


class UserAddressView(LoginRequiredMixin, View):
    """用户中心--地址界面"""

    def get(self, request):
        data = {'which_page': 3}
        return render(request, 'user_center_site.html', data)


class UserAddressView(LoginRequiredMixin, View):

    def get(self, request):

        # 查询登录用户最新添加的地址，并显示出来
        try:
            # address = Address.objects.filter(
            #     user=request.user).order_by('-create_time')[0]
            address = request.user.address_set.latest('create_time')
        except Exception:
            address = None

        context = {
            'which_page': 3,
            'address': address,
        }
        return render(request, 'user_center_site.html', context)

    def post(self, request):
        # 获取post请求参数
        receiver = request.POST.get('receiver')
        detail = request.POST.get('detail')
        zip_code = request.POST.get('zip_code')
        mobile = request.POST.get('mobile')

        # del request.session['_auth_user_id']

        # 合法性校验
        if not all([receiver, detail, mobile]):
            return render(request, 'user_center_site.html',
                          {'errmsg': '参数不能为空'})

        # 新增一个地址
        Address.objects.create(
            receiver_name=receiver,
            receiver_mobile=mobile,
            detail_addr=detail,
            zip_code=zip_code,
            user=request.user,
        )

        # 添加地址成功，回到当前界面，刷新数据：/users/address
        return redirect(reverse('users:address'))


class UserInfoView(LoginRequiredMixin, View):

    def get(self, request):
        # 查询登录用户最新添加的地址，并显示出来
        try:
            address = request.user.address_set.latest('create_time')
        except Address.DoesNotExist:
            address = None

        # 从Redis数据库中查询出用户浏览过的商品记录
        strict_redis = get_redis_connection('default')
        key = 'history_%s' % request.user.id
        goods_ids = strict_redis.lrange(key, 0, 4)
        skus = []
        for id in goods_ids:
            try:
                sku = GoodsSKU.objects.get(id=id)
                # 添加一个商品到列表中,以便它能保持原有的顺序
                skus.append(sku)
            except GoodsSKU.DoesNotExist:
                pass

        # 定义模板数据
        data = {
            'which_page': 1,
            'address': address,
            'skus': skus,
        }

        # 响应请求,返回html界面
        return render(request, 'user_center_info.html', data)
