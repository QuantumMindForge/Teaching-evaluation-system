# Generated by Django 4.1.7 on 2024-09-08 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pingjia',
            name='s_liuyan',
            field=models.TextField(default='', max_length=210, null=True, verbose_name='学生留言'),
        ),
    ]
