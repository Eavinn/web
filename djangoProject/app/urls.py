from django.urls import path, re_path
from app import views

urlpatterns = [path('', views.index),
               path('show_deps', views.show_deps, name='show_departments'),
               path('add_dep', views.add_dep),
               path('get', views.get),
               path('post', views.post),
               path('do_post', views.do_post),
               path('json', views.json),
               path('get_employee', views.get_employee),
               path('set_cookie', views.set_cookie),
               path('get_cookie', views.get_cookie),
               path('set_session', views.set_session),
               path('get_session', views.get_session),
               path('inherit', views.inherit),
               re_path(r'del_dep/(\d+)', views.del_dep, name='del_department'),
               re_path(r'show_dep/(\d+)', views.show_dep),

               # f2可以快速跳转到代码出错的地方，演示csrf
               path('login', views.login),
               path('do_login', views.do_login),

               # 验证码验证
               path('create_verify_code', views.create_verify_code),
               path('show_verify_code', views.show_verify_code),
               path('do_verify', views.do_verify),

               # 上传文件
               path('add_user', views.add_user),
               path('do_add_user', views.do_add_user),
               path('show_images', views.show_images),

               # 分页展示
               re_path(r'show_page/(\d+)', views.show_page),

               # 区域选择
               path('show_areas', views.show_areas),
               re_path(r'get_children/(\d+)', views.get_children),


]
