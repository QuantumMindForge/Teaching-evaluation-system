import hashlib

from django.shortcuts import render

from login.models import *


# Create your views here.
# @check_login
def teacher_index(request):
    '''

        1.教师id
        2.班级过滤器
        3.跳转到班级评价


    '''
    teacher_id = request.session['teacher_id']
    a = KeCheng.objects.filter(teacher_id=teacher_id, is_active=True).values('student_id__banji', 'student_id', 'id')  # 学生班级
    return render(request, 'teachers/index.html', locals())


# @check_login
"""
    1.班级过滤器
    2.学生评价了
    3.学生评价平均值
    4.总评价
    from django.db.models import Avg,Max,Min,Count,Sum

"""


def teacher_pingjia(request, banji_id):
    from django.db.models import Avg
    # 获取教师id
    teacher_id = request.session.get('teacher_id')

    # 过滤当前教师、班级的评价数据
    pingjiabaio = PingJia.objects.filter(
        is_active=True,
        kecheng__student_id__banji=banji_id,
        kecheng__teacher_id=teacher_id
    )  # 评价记录

    # 获取所有题库中的题目
    tiku = TiKu.objects.filter(is_active=True)

    # 获取该教师相关课程的学生信息
    kecheng_data = KeCheng.objects.filter(
        teacher_id=teacher_id,
        is_active=True
    ).values(
        'student_id__banji', 'student_id', 'id', 'is_ping'
    )  # 班级过滤器

    # 过滤该班级的课程
    kecheng_banji = KeCheng.objects.filter(
        teacher_id=teacher_id,
        is_active=True,
        student_id__banji=banji_id
    )

    # 计算评价率
    pingjia_sum = PingJia.objects.filter(
        kecheng__student_id__banji=banji_id,
        kecheng__is_ping='ok'
    ).count() / 20  # 学生评价数

    stu_sum = Students.objects.filter(
        is_active=True,
        banji=banji_id
    ).count()  # 班级学生总数
    print(stu_sum)
    # 评价率 = 学生评价数 / 总学生数
    PJL = float('%.2f' % (pingjia_sum / stu_sum * 100)) if stu_sum != 0 else 0

    # 聚合查询，计算各个问题的平均得分
    avg_scores = pingjiabaio.aggregate(
        avg_score=Avg('score')  # 直接基于评分字段计算平均分
    )
    sum_score1 = 0
    sum_score2 = 0
    sum_score3 = 0
    sum_score4 = 0
    sum_score5 = 0
    sum_score6 = 0
    sum_score7 = 0
    sum_score8 = 0
    sum_score9 = 0
    sum_score10 = 0
    for timu in pingjiabaio.values():
        if int(timu['id']) % 10 == 1:
            sum_score1 += timu['score']
        if int(timu['id']) % 10 == 2:
            sum_score2 += timu['score']
        if int(timu['id']) % 10 == 3:
            sum_score3 += timu['score']
        if int(timu['id']) % 10 == 4:
            sum_score4 += timu['score']
        if int(timu['id']) % 10 == 5:
            sum_score5 += timu['score']
        if int(timu['id']) % 10 == 6:
            sum_score6 += timu['score']
        if int(timu['id']) % 10 == 7:
            sum_score7 += timu['score']
        if int(timu['id']) % 10 == 8:
            sum_score8 += timu['score']
        if int(timu['id']) % 10 == 9:
            sum_score9 += timu['score']
        if int(timu['id']) % 10 == 0:
            sum_score10 += timu['score']
    if pingjia_sum != 0:
        avg_score1 = sum_score1 / pingjia_sum
        avg_score2 = sum_score2 / pingjia_sum
        avg_score3 = sum_score3 / pingjia_sum
        avg_score4 = sum_score4 / pingjia_sum
        avg_score5 = sum_score5 / pingjia_sum
        avg_score6 = sum_score6 / pingjia_sum
        avg_score7 = sum_score7 / pingjia_sum
        avg_score8 = sum_score8 / pingjia_sum
        avg_score9 = sum_score9 / pingjia_sum
        avg_score10 = sum_score10 / pingjia_sum
    else:
        avg_score1 = 0
        avg_score2 = 0
        avg_score3 = 0
        avg_score4 = 0
        avg_score5 = 0
        avg_score6 = 0
        avg_score7 = 0
        avg_score8 = 0
        avg_score9 = 0
        avg_score10 = 0
    avg = [avg_score1*10, avg_score2*10, avg_score3*10, avg_score4*10, avg_score5*10, avg_score6*10, avg_score7*10,
           avg_score8*10, avg_score9*10, avg_score10*10]
    print(avg)
    # 综合评价平均分
    try:
        avg_score = float('%.2f' % avg_scores['avg_score']) if avg_scores['avg_score'] else 0.0
    except Exception as e:
        avg_score = 0.0
        print('Error calculating average score:', e)

    kecheng = kecheng_banji.first()  # 因为一个老师对应这个班级很多学生，但一个老师也只教一门课，所以取第一个获取其课程即可
    # 渲染模板并传递数据
    return render(request, 'teachers/pingjia_ok.html', {
        'pingjiabaio': pingjiabaio,
        'tiku': tiku,
        'kecheng_data': kecheng_data,
        'kecheng_banji': kecheng_banji,
        'PJL': PJL,
        'avg_score': avg_score * 10,
        'kecheng': kecheng,
        'stu_sum': stu_sum,
        'pingjia_sum': int(pingjia_sum),
        'avg': avg,
    })


def pswd_update(request):
    if request.method == 'GET':
        return render(request, 'teachers/pswd_updat.html')
    if request.method == 'POST':
        name = request.session.get('teacher_id')
        pswd = request.POST['pswd']
        pswd_1 = request.POST['pswd_1']
        pswd_2 = request.POST['pswd_2']

        if pswd_1 != pswd_2:
            msg = "新密码不一致！！！"
            return render(request, 'teachers/pswd_updat.html', {"msg": msg})
        try:
            ss = Teachers.objects.filter(teacher_id=name, password=pswd, is_active=True)
            sm = Teachers.objects.get(teacher_id=name, is_active=True)
        except Exception as e:
            print("teacher_update_pswd:", e)
        if ss:
            sm.password = pswd_1
            sm.save()
            msg = "密码修改成功！！"
            return render(request, 'index.html', {"msg": msg})
        else:
            msg = "原密码错误！"
            return render(request, 'teachers/pswd_updat.html', {"msg": msg})
