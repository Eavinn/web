# Generated by Django 3.0.3 on 2020-08-19 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name_plural': '部门'},
        ),
        migrations.AlterModelTable(
            name='department',
            table='department',
        ),
    ]