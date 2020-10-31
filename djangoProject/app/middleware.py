"""
自定义中间键
"""
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class MyMiddleware(MiddlewareMixin):
    """自定义中间件"""
    exclude_ips = ['127.0.0.8']

    def __init__(self, get_response):
        # One-time configuration and initialization.
        super().__init__(get_response)
        print("--init--")

    @classmethod
    def process_request(cls, request):
        print('--process_request--')
        if request.META.get('REMOTE_ADDR') in cls.exclude_ips:
            return HttpResponse("禁止访问")

    def process_view(self, request, view_func, view_args, view_kwargs):
        print('--process_view--')

    def process_response(self, request, response):
        print('--process_response--')
        return response

    def process_exception(self, request, exception):
        # 中间件异常处理
        print('-----process_exception')
        return HttpResponse('运行出错了：%s' % exception)
