from django.urls import path, re_path
from apps.users import views


urlpatterns = [
    # path('register', views.register, name='register'),
    # path('do_register', views.do_register, name='do_register'),
    # 类视图
    path('register', views.RegisterView.as_view(), name='register'),
    re_path(r'^active/(.+)$', views.ActiveView.as_view(), name='active'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('address', views.UserAddressView.as_view(), name='address'),  # 用户中心:地址
    re_path(r'^orders/(\d+)$', views.UserOrderView.as_view(), name='orders'),  # 用户中心:订单
    path('', views.UserInfoView.as_view(), name='info'),  # 用户中心:个人信息
]