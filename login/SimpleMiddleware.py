import re
from django.shortcuts import redirect
from django.urls import reverse

# 该中间件的作用是如果用户未登录就企图访问除登录以外界面，就会跳转到登录界面
class SimpleMiddleware:
    def __init__(self, get_response):
        # 将请求传递给中间件
        self.get_response = get_response

    # 每次有请求时都会调用__call__方法
    def __call__(self, request):
        path = request.path
        """
            1.判断是否登录
            2.判断是否访问pingjia开头
        """
        # 允许后台不登录情况下访问的路径
        urllist = ['/', '/logout/', '/login/']
        if re.match(r'^/students/', path) and (path not in urllist):
            # 重定向到登录页
            if 'student_id' not in request.session:
                return redirect(reverse("login"))
        if re.match(r'^/teachers/', path) and (path not in urllist):
            # 重定向到登录页
            if 'teacher_id' not in request.session:
                return redirect(reverse("login"))
        if re.match(r'^/myadmin/', path) and (path not in urllist):
            # 重定向到登录页
            if 'name' not in request.session:
                return redirect(reverse("login"))

        response = self.get_response(request)
        return response
