from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.teacher_index),  # 教师首页
    path('teacher_pingjia/<str:banji_id>', views.teacher_pingjia),  # 教师查看班级
    path('pswd_updatae', views.pswd_update, name="teacher_pswd_update"),  # 教师查看班级
]
