from django.contrib import admin

# Register your models here.

from app.models import *


class DepartmentAdmin(admin.ModelAdmin):
    # 指定后台网页要显示的字段
    list_display = ["name", "create_date"]


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["name", "age", "sex", "salary", "comment", "department_id"]


class AreaStackedInline(admin.StackedInline):
    model = Area  # 关联子对象（多类对象）


class AreaAdmin(admin.ModelAdmin):
    # 定义列表中要显示哪些字段(也可以指定方法名)
    list_display = ['id', 'title', "parent_area"]
    # 限制每页长度
    list_per_page = 10
    # 显示顶部的选项
    actions_on_top = True
    # 显示底部的选项
    actions_on_bottom = True
    # 右侧栏过滤器
    list_filter = ['title']
    # 要搜索的列的值
    search_fields = ['title']
    # 表单中字段显示的顺序
    # fields = ['parent', 'title']
    # 字段分组显示
    fieldsets = (
        ('基本', {'fields': ('title',)}),
        ('基本', {'fields': ('parent',)})
    )
    # 编辑关联对象
    inlines = [AreaStackedInline]


# 注册Model类
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(User)
