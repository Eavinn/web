"""
关于orm映射的sql语法总结：
1. 动作词 all, filter, exclude, order_by, aggregate，count, delete, update
2. 条件 属性__exact, 属性__contains, 属性__endswith, 属性__startswith, 属性_isnull, 属性__in, 属性__gt, 属性__lt, 属性__gt, 属性__lte
    Count('属性'), Avg(‘属性’)等与aggregate联合使用。条件并列Q()
3. 匹配值 date(), F('属性')
4. 关联查询用法   一类对象.多类名小写_set.all()，
                多类对象.关联属性，
                一类名.objects.filter(多类名小写__多类属性名__条件名=值)，
                多类名.objects.filter(关联属性__一类属性名__条件名=值).
"""

from django.db import models

# Create your models here.


class DepartmentManager(models.Manager):
    """创建自定义模型管理器，重写object原有方法或新增封装方法"""

    def all(self):
        return super().all().filter(is_delete=False)

    @staticmethod
    def create_dep(name, create_date):
        dep = Department()
        dep.name = name
        dep.create_date = create_date
        dep.save()
        return dep


class Department(models.Model):
    """ department """
    name = models.CharField(max_length=20)
    create_date = models.DateField()
    is_delete = models.BooleanField(default=False)

    class Meta:
        # 实际表名修改
        db_table = "department"
        # 管理后台表名修改
        # verbose_name = '部门'
        verbose_name_plural = '部门'

    # 自定义模型管理器
    objects = DepartmentManager()


class Employee(models.Model):
    """ employee """
    SEX_CHOICES = ((0, '男'), (1, '女'))

    name = models.CharField(max_length=20)
    age = models.IntegerField()
    sex = models.IntegerField(default=0, choices=SEX_CHOICES)
    salary = models.DecimalField(max_digits=8, decimal_places=2)
    comment = models.CharField(max_length=500, null=True, blank=True)
    # CASCADE：级联删除。
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    hire_date = models.DateField(auto_now_add=True)


class Area(models.Model):
    """area,save Provinces, cities, districts"""
    # 设置verbose_name属性
    title = models.CharField(verbose_name='地名', max_length=30)
    # 关联属性，自关联
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        # 修改对象显示的字符串
        return self.title

    def parent_area(self):
        if self.parent:
            return self.parent.title

    # 指定方法列显示的名称
    parent_area.short_description = '父级区域'
    # 指定方法列按id进行排序
    parent_area.admin_order_field = 'id'


class User(models.Model):
    """用户模型类"""

    # 用户名称
    name = models.CharField(max_length=20)
    # 用户头像
    avatar = models.ImageField(upload_to='app')

