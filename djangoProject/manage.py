#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
"""
python manage.py makemigrations 根据模型类，生成迁移文件
python manage.py migrate 执行迁移文件生成数据库表
python manage.py createsuperuser 创建超级管理员
"""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
