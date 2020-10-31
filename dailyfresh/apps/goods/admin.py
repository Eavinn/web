from django.contrib import admin
from django_redis import cache

from apps.goods.models import *
from apps.celery_tasks.tasks import generate_static_index_page


class BaseAdmin(admin.ModelAdmin):

    # list_display = ['id', 'name']
    def save_model(self, request, obj, form, change):
        """在管理后台新增或修改了模型数据后调用"""
        super().save_model(request, obj, form, change)
        print('save_model: %s ' % obj)
        # 通过celery异步生成静态的首页
        # generate_static_index_page.delay()
        cache.delete('index_page_data')

    def delete_model(self, request, obj):
        """在管理后台删除一条数据时调用"""
        super().delete_model(request, obj)
        print('delete_model: %s ' % obj)
        # 通过celery异步生成静态的首页
        # generate_static_index_page.delay()
        cache.delete('index_page_data')


class GoodsCategoryAdmin(BaseAdmin):
    pass


admin.site.register(IndexSlideGoods)
admin.site.register(IndexPromotion)
admin.site.register(GoodsCategory, GoodsCategoryAdmin)
admin.site.register(GoodsSKU)
