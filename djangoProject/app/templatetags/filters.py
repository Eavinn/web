from django.template import Library

# 名字不能修改
register = Library()


@register.filter
def odd(value):
    return value % 2 == 1
