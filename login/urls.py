from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name="login"),  # 评价系统首页

    path('login/', views.login),  # 登录页面

    path('zhuce/', views.zhuce),  # 注册界面

    path('logout/', views.logout),  # 退出页面

    path('teacher_zhuce', views.teacher_zhuce), # 老师注册
]

