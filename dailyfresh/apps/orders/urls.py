from django.urls import path, re_path
from apps.orders import views


urlpatterns = [
    # /orders/place 确认订单界面
    path('place', views.PlaceOrderView.as_view(), name='place'),
    # 订单提交 /orders/commit
    path('commitcommit', views.CommitOrderView.as_view(), name='commit'),
    # 支付: /orders/pay
    path('pay', views.OrderPayView.as_view(), name='pay'),
    # 查询支付结果: /orders/check
    path('check', views.OrderCheckView.as_view(), name='check'),
]