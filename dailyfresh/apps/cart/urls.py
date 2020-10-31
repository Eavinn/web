from django.urls import path, re_path
from apps.cart import views


urlpatterns = [

    path('add', views.AddCartView.as_view(), name='add'),  # 添加商品到购物车
    path('update', views.CartUpdateView.as_view(), name='update'),  # 更新购物车商品数量
    path('', views.CartInfoView.as_view(), name='info'),  # 进入购物车界面
    path('delete', views.CartDeleteView.as_view(), name='delete'),
]