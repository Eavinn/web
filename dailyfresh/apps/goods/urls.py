from django.urls import path, re_path
from apps.goods import views


urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    re_path(r'^detail/(\d+)$', views.DetailView.as_view(), name='detail'),
    re_path(r'^list/(\d+)/(\d+)$', views.ListView.as_view(), name='list'),
]