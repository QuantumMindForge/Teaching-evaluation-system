
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),  # 学生评价首页
    path('update_pingjia/<str:kecheng_id>', views.update_pingjia),  # 学生评价页
    path('cat_pingjia/<str:kecheng_id>', views.cat_pingjia),  # 查看学生评价页
    path('ok_pingjia/', views.ok_pingjia),  # 已评价
    path('update_password/', views.update_password),  # 登录页面

    # path('zhuce/', views.zhuce),  # 注册页面

 ]