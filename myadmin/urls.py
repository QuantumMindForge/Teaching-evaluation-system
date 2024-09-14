from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.myadmin, name='myadmin'),  # 管理员首页
    path('pswd_update', views.pswd_update, name='myadmin_pswd_update'),  # 管理员首页
    # ————————————————学生管理————————————————
    path('stu/<int:pIndex>', views.myadmin_stu, name='myadmin_stu'),  # 学生管理
    path('stu_add/', views.stu_add),  # 添加学生
    path('stu_edit/<str:student_id>', views.stu_edit),  # 编辑学生
    path('stu_del/<str:student_id>', views.stu_del, name='myadmin_stu_del'),  # 删除学生
    path('stu_upload/', views.stu_upload, name='myadmin_stu_upload'),  # 上传学生信息
    path('stu_toupload/', views.stu_toupload, name='myadmin_stu_toupload'),  # 查看上传的学生信息

    # ———————————————教师管理—————————————————
    path('teachers/<int:pIndex>', views.myadmin_teachers, name='myadmin_teachers'),  # 教师管理
    path('teachers_add/', views.teachers_add, name='myadmin_teachers_add'),  # 添加教师
    path('teachers_edit/<str:teacher_id>', views.teachers_edit, name='myadmin_teachers_edit'),  # 编辑教师
    path('teachers_del/<str:teacher_id>', views.teachers_del, name='myadmin_teachers_del'),  # 删除教师
    path('teachers_upload/', views.teachers_upload, name='myadmin_teacher_upload'),  # 上传教师信息
    path('teachers_toupload/', views.teachers_toupload, name='myadmin_teacher_toupload'),  # 查看上传的教师信息

    # —————————————————课程管理———————————————————————
    path('kecheng/<int:pIndex>', views.myadmin_kecheng, name='myadmin_kecheng'),  # 课程管理
    path('kecheng_add/', views.myadmin_kecheng_add, name='myadmin_kecheng_add'),  # 添加课程
    path('kecheng_edit/<str:kecheng_id>', views.myadmin_kecheng_edit, name='myadmin_kecheng_edit'),  # 编辑课程
    path('kecheng_del/<str:kecheng_id>', views.myadmin_kecheng_del, name='myadmin_kecheng_del'),  # 删除课程
    path('kecheng_upload/', views.kecheng_upload, name='myadmin_kecheng_upload'),  # 上传课程
    path('kecheng_toupload/', views.kecheng_toupload, name='myadmin_kecheng_toupload'),  # 查看上传课程

    # —————————————————题库管理———————————————————————
    path('tiku/', views.myadmin_tiku, name='myadmin_tiku'),  # 评价题库管理
    path('tiku_add/', views.myadmin_tiku_add, name='myadmin_tiku_add'),  # 添加评价题
    path('tiku_edit/<int:id>', views.myadmin_tiku_edit, name='myadmin_tiku_edit'),  # 编辑题库
    path('tiku_del/<int:id>', views.myadmin_tiku_del, name='myadmin_tiku_del'),  # 删除评价题

    # —————————————————————评价管理———————————————————————————————————
    path('pingjia/', views.myadmin_pingjia, name='myadmin_pingjia'),  # 评价排行榜
    path('pingjia_show/', views.myadmin_pingjia_show, name='myadmin_pingjia_show'),  # 查看评价信息
    path('pingjia_pjl/', views.myadmin_pingjia_pjl, name='myadmin_pingjia_pjl'),  # 班级评价率
    path('pingjia_not/', views.myadmin_pingjia_not, name='myadmin_pingjia_not'),  # 未评价

    # —————————————————————管理员管理———————————————————————————————————
    path('admin/', views.myadmin_admin, name='myadmin_admin'),  # 管理员首页
    path('admin_add/', views.myadmin_admin_add, name='myadmin_admin_add'),  # 添加管理员
    path('admin_edit/<str:name>', views.myadmin_admin_edit, name='myadmin_admin_edit'),  # 编辑管理员
    path('admin_del/<str:name>', views.myadmin_admin_del, name='myadmin_admin_del'),  # 删除管理员
]
