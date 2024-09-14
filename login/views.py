from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from login.models import *  # 将模型全部导入
import hashlib  # 后续使用哈希算法处理转化密码的存储和数据的存储都要用到

# 登录界面
def login(request):
    if request.method == "POST":
        student_id = request.POST['student_id']
        password = request.POST['password']

        msg = "请您输入正确的用户名和密码，注意区分大小写"

        # -------------------------------------------------------------------------------------------------------------------------
        # 从Students数据库表中查找符合条件的记录
        try:
            ans1 = Students.objects.filter(student_id=student_id, password=password)
            print(student_id, password)
        except Exception as e:
            print(f"登录出错了{e}")

        if ans1:
            # 将用户的学号存储到会话session中
            request.session['student_id'] = str(student_id)
            # 创建一个HTTP重定向响应，将用户重定向到 / students / 路径，即学生页面或学生主界面。
            # HttpResponseRedirect是Django提供的用于重定向的响应类型，通常用于在处理完某个操作后引导用户访问新的URL。
            response = HttpResponseRedirect('/students/')

            return response

        # -------------------------------------------------------------------------------------------------------------------------
        # 从Teachers数据库表中查找符合条件的记录
        try:
            ans2 = Teachers.objects.filter(teacher_id=student_id, password=password)
            print(student_id, password)
        except Exception as e:
            print(f"登录出错了{e}")

        if ans2:
            # 将用户的学号存储到会话session中
            request.session['teacher_id'] = str(student_id)
            # 创建一个HTTP重定向响应，将用户重定向到 / teachers / 路径，即学生页面或学生主界面。
            # HttpResponseRedirect是Django提供的用于重定向的响应类型，通常用于在处理完某个操作后引导用户访问新的URL。
            response = HttpResponseRedirect('/teachers/')

            return response

        # -------------------------------------------------------------------------------------------------------------------------
        # 从GuanLiYuan数据库表中查找符合条件的记录
        try:
            ans3 = GuanLiYuan.objects.filter(name=student_id, password=password)
            print(student_id, password)
        except Exception as e:
            print(f"登录出错了{e}")

        if ans3:
            request.session['name'] = str(student_id)
            response = HttpResponseRedirect('/myadmin/')
            return response

        # -------------------------------------------------------------------------------------------------------------------------
        # 这表示登录成功后跳转到index.html页面，并使用字典传入msg参数
        return render(request, 'index.html', {"msg": msg})

    elif request.method == "GET":
        """如果是GET信息，就可能是用户失误或者是恶意信息或数据，直接返回登录页面即可"""
        return HttpResponseRedirect('/')

# 登出界面
def logout(request):
    # 因为在登录界面进行数据匹配的过程中，将id存入到了session会话中，所以在登出时要删除session信息
    if "student_id" in request.session:
        del request.session['student_id']
    if "name" in request.session:
        del request.session['name']
    if "teacher_id" in request.session:
        del request.session['teacher_id']

    # 为了保证账号的安全，也要删除cookie信息，因为盗取信息是通过获取cookie来实现的
    response = HttpResponseRedirect('/')

    if "student_id" in request.COOKIES:
        response.delete_cookie("student_id")
    if "teacher_id" in request.COOKIES:
        response.delete_cookie("teacher_id")

    return response

# 默认首页
def index(request):
    return render(request, "index.html")

# 学生注册(默认注册)
def zhuce(request):
    # 注册要需要判断访问发送的HTTP信息类型
    if request.method == "POST":
        student_id = request.POST['student_id']
        password = request.POST['password']
        # 注册需要二次确认密码是否一致
        password_as = request.POST['password_as']

        if password != password_as:
            msg = "密码不一致，请确保两次密码保持一致！"
            # locals()用于将视图函数中的所有局部变量以字典形式传递给模板引擎，以便在渲染HTML模板时使用这些变量
            return render(request, "pingjiaxitong/zhuce.html", locals())

        # 函数没有return，就代表两次密码一致，再进行下一步，碰到当前信息是否被注册，确保正常使用
        ans1 = Students.objects.filter(student_id=student_id)
        if ans1:
            msg = "该学号已注册，请输入新正确的学号尝试！"
            # locals()用于将视图函数中的所有局部变量以字典形式传递给模板引擎，以便在渲染HTML模板时使用这些变量
            return render(request, "pingjiaxitong/zhuce.html", locals())

        # 函数到这里没有return，表示信息未被注册过，就处理信息并插入信息

        try:
            # 这里create是直接在Students数据库表中通过映射添加一条新数据，括号里的就是 字段：数据 的映射
            student = Students.objects.create(student_id=student_id, password=password)
        except Exception as e:
            # 可能存在索引并发问题
            print(f"注册失败{e}")
            msg = "该学号已注册，请输入新的学号尝试！"
            # locals()用于将视图函数中的所有局部变量以字典形式传递给模板引擎，以便在渲染HTML模板时使用这些变量
            return render(request, "pingjiaxitong/zhuce.html", locals())

        # 将数据存储到session会话中
        request.session['student_id'] = str(student.student_id)
        resp = HttpResponse('记住我🆗')
        if 'remember' in request.POST:
            # 设置一个时长为3天的cookie，在三天内不需要重新登录
            resp.set_cookie('student_id', student_id, 3600 * 24 * 3)

        return resp

        return HttpResponse('注册成功！')
    # 如果是GET信息就切换到注册界面
    elif request.method == "GET":
        return render(request, "pingjiaxitong/zhuce.html")

# 老师注册
def teacher_zhuce(request):
    # 注册要需要判断访问发送的HTTP信息类型
    if request.method == "POST":
        teacher_id = request.POST['teacher_id']
        password = request.POST['password']
        # 注册需要二次确认密码是否一致
        password_as = request.POST['password_as']

        if password != password_as:
            msg = "密码不一致，请确保两次密码保持一致！"
            # locals()用于将视图函数中的所有局部变量以字典形式传递给模板引擎，以便在渲染HTML模板时使用这些变量
            return render(request, "teachers/zhuce.html", locals())

        # 函数没有return，就代表两次密码一致，再进行下一步，碰到当前信息是否被注册，确保正常使用
        ans2 = Teachers.objects.filter(teacher_id=teacher_id)
        if ans2:
            msg = "该教工号已注册，请输入正确的教工号尝试！"
            # locals()用于将视图函数中的所有局部变量以字典形式传递给模板引擎，以便在渲染HTML模板时使用这些变量
            return render(request, "teachers/zhuce.html", locals())

        # 函数到这里没有return，表示信息未被注册过，就处理信息并插入信息

        try:
            # 这里create是直接在Students数据库表中通过映射添加一条新数据，括号里的就是 字段：数据 的映射
            teacher = Teachers.objects.create(teacher_id=teacher_id, password=password)
        except Exception as e:
            # 可能存在索引并发问题
            print(f"注册失败{e}")
            msg = "该教工号已注册，请输入正确的教工号尝试！"
            # locals()用于将视图函数中的所有局部变量以字典形式传递给模板引擎，以便在渲染HTML模板时使用这些变量
            return render(request, "teachers/zhuce.html", locals())

        # 将数据存储到session会话中
        request.session['teacher_id'] = str(teacher.teacher_id)
        resp = HttpResponse('记住我🆗')
        if 'remember' in request.POST:
            # 设置一个时长为3天的cookie，在三天内不需要重新登录
            resp.set_cookie('teacher_id', teacher_id, 3600 * 24 * 3)

        return resp

        return HttpResponse('注册成功！')
    # 如果是GET信息就切换到注册界面
    elif request.method == "GET":
        return render(request, "teachers/zhuce.html")
