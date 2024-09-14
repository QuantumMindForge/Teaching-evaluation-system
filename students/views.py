import hashlib

from django.shortcuts import render, HttpResponse, HttpResponseRedirect

from login.models import *


# Create your views here.
# 系统首页
# @check_login
def index(request):
    # get请求返回页面
    if request.method == "GET":
        xuehao = request.session['student_id']
        # tiku = TiKu_1.objects.filter(is_active=True)
        book = KeCheng.objects.filter(student_id=xuehao, is_active=True, is_ping='no').order_by('id')  #
        book1 = KeCheng.objects.filter(student_id=xuehao, is_active=True, is_ping='ok')
        return render(request, 'students/index.html', locals())

def update_pingjia(request, kecheng_id):
    student_id = request.session['student_id']  # 获取当前学生ID
    try:
        # 获取课程信息
        kecheng = KeCheng.objects.get(id=kecheng_id, is_active=True)
        tiku_list = TiKu.objects.filter(is_active=True).order_by('id')  # 获取所有激活的题目
    except KeCheng.DoesNotExist:
        return HttpResponse('--The kecheng does not exist!')

    if request.method == 'GET':
        # 返回评价页面
        return render(request, 'students/pingjia_id.html', {'kecheng': kecheng, 'tiku_list': tiku_list})

    elif request.method == 'POST':
        try:
            # 学生的留言
            stu_liuyan = request.POST['liuyan']

            total_score = 0
            num_questions = 0  # 题目数量

            # 遍历题库，获取学生对每道题的回答
            for tiku in tiku_list:
                student_answer = request.POST.get(str(tiku.id))  # 获取学生的答案
                if student_answer:
                    # 创建评价记录
                    pingjia = PingJia.objects.create(
                        kecheng=kecheng,
                        student_id=student_id,
                        question=tiku,
                        student_answer=student_answer,
                        s_liuyan=stu_liuyan
                    )
                    # 累加得分
                    total_score += pingjia.score
                    num_questions += 1

            # 计算平均分
            if num_questions > 0:
                avg_score = total_score / num_questions
            else:
                avg_score = 0

            # 更新课程表中的是否评价标志
            kecheng.is_ping = 'ok'
            kecheng.save()

            return HttpResponseRedirect('/students/')  # 评价完成后重定向
        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse('An error occurred during the evaluation.')


# 学生已评价
# @check_login
def ok_pingjia(request):
    xuehao = request.session['student_id']
    tiku = TiKu.objects.filter(is_active=True)
    book = KeCheng.objects.filter(student_id=xuehao, is_active=True, is_ping='no')  #
    book1 = KeCheng.objects.filter(student_id=xuehao, is_active=True, is_ping='ok').order_by('id')  #
    return render(request, 'students/ok_pingjia.html', locals())

def cat_pingjia(request, kecheng_id):
    # 获取当前学生的学号
    xuehao = request.session.get('student_id')

    # 查询该学生已评价和未评价的课程
    # 未评价的课程
    book = KeCheng.objects.filter(student_id=xuehao, is_active=True, is_ping='no')
    # 已评价的课程
    book1 = KeCheng.objects.filter(student_id=xuehao, is_active=True, is_ping='ok').order_by('id')

    # 获取课程的详细信息
    kecheng = KeCheng.objects.filter(id=str(kecheng_id), is_active=True).values(
        'id', 'kecheng', 'teacher_id__name', 'teacher_id__phone'
    ).first()

    # 获取题库中所有题目（如果需要筛选特定题目，可以根据需求修改过滤条件）
    tiku = TiKu.objects.filter(is_active=True)

    # 查询当前学生在该课程中的评价记录
    pingjia_list = PingJia.objects.filter(kecheng_id=kecheng_id, student_id=xuehao, is_active=True)

    # 构建数据列表，包含课程、题目、学生答案和得分
    data_list = []
    for pj in pingjia_list:
        data = {
            'question': pj.question.timu,
            'student_answer': pj.student_answer,
            'score': pj.score,
        }
        liuyan = pj.s_liuyan
        data_list.append(data)

    # 渲染模板并传递所有相关数据
    return render(request, 'students/cat_pingjia.html', {
        'book': book,
        'book1': book1,
        'kecheng': kecheng,
        'tiku': tiku,
        'data_list': data_list,
        'liuyan': liuyan,
    })

# 学生密码修改
def update_password(request):
    if request.method == 'GET':

        return render(request, 'students/update_password.html')
    elif request.method == 'POST':
        xuehao = request.session['student_id']
        pswd = request.POST['password']
        pswd_1 = request.POST['password_1']
        pswd_2 = request.POST['password_2']

        # 新密码是否相同
        if pswd_1 != pswd_2:
            msg = '密码不一致！！！'
            return render(request, "students/update_password.html", locals())
        try:
            s = Students.objects.filter(student_id=xuehao, password=pswd)
        except Exception as e:
            return HttpResponse('students_update_pswd:', e)

        if s:
            # 如果是修改密码
            s.update(password=pswd_1)
            # 免登录一天
            request.session['student_id'] = xuehao

            msg = '修改密码成功！'

            return HttpResponseRedirect('/students/', locals())
        else:
            msg = '原密码错误！'
            return render(request, 'students/update_password.html', locals())
