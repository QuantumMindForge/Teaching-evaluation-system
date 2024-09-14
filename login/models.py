from django.db import models

# Create your models here.

# is_active是对数据进行一个逻辑删除的作用

# 管理员数量很少，以名字为主键即可
class GuanLiYuan(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=50, primary_key=True)
    password = models.CharField(verbose_name="密码", max_length=50)
    email = models.EmailField(verbose_name="邮箱", default="") # 邮箱选填
    phone = models.CharField(verbose_name="电话号码", max_length=11)
    touxiang = models.ImageField(verbose_name="头像", upload_to="admin/", default='')
    is_active = models.BooleanField(verbose_name="是否活跃", default=True)

    def __str__(self):
        return f"{self.name}({self.phone})"

    class Meta:
        # 数据库列表名
        db_table = 'GuanLiYuan'
        # admin后台管理名
        verbose_name_plural = "管理员列表"

class Teachers(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=50, default='')
    password = models.CharField(verbose_name="密码", max_length=50, default='')
    teacher_id = models.CharField(verbose_name="教师id", max_length=50, primary_key=True, default='')
    sex = models.CharField(verbose_name="性别", max_length=50, choices=(('male', '男'), ('female', '女')), default='male')
    email = models.EmailField(verbose_name="邮箱", default='')
    phone = models.CharField(verbose_name="电话号码", max_length=11)
    touxiang = models.ImageField(verbose_name="头像", upload_to="teachers/", default='')
    is_active = models.BooleanField(verbose_name="是否活跃", default=True)

    def __str__(self):
        return f"{self.teacher_id}-{self.name}-{self.sex}-{self.phone}"

    class Meta:
        db_table = 'Teachers'
        verbose_name_plural = "老师列表"

class Students(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=50, default='')
    password = models.CharField(verbose_name="密码", max_length=50, default='')
    xueyuan = models.CharField(verbose_name="学院", max_length=50, default='')
    banji = models.CharField(verbose_name="班级", max_length=50, default='')
    student_id = models.CharField(verbose_name="学生id", max_length=50, primary_key=True, default='')
    sex = models.CharField(verbose_name="性别", max_length=50, choices=(('male', '男'), ('female', '女')), default='male')
    email = models.EmailField(verbose_name="邮箱", default='')
    phone = models.CharField(verbose_name="电话号码", max_length=11)
    touxiang = models.ImageField(verbose_name="头像", upload_to="students/", default='')
    is_active = models.BooleanField(verbose_name="是否活跃", default=True)

    def __str__(self):
        return f"{self.student_id}-{self.name}-{self.sex}-{self.phone}"

    class Meta:
        db_table = 'Students'
        verbose_name_plural = "学生列表"

class KeCheng(models.Model):
    id = models.CharField(verbose_name="id", max_length=50, primary_key=True, default='')
    kecheng = models.CharField(verbose_name="课程", max_length=150, default='')
    # 建立外键通常to就足够用了，
    student_id = models.ForeignKey(to='Students', on_delete=models.CASCADE, verbose_name="学生id", default='')
    teacher_id = models.ForeignKey(to='Teachers', on_delete=models.CASCADE, verbose_name="老师id", default='')
    is_ping = models.CharField(verbose_name="是否已经评价", max_length=6, choices=(('ok', '是'), ('no', '否')), default='no')
    is_active = models.BooleanField(verbose_name="是否活跃", default=True)

    def __str__(self):
        return self.kecheng

    class Meta:
        db_table = 'KeCheng'
        verbose_name_plural = "选课表"

class TiKu(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)  # id
    timu = models.TextField(verbose_name="题目", max_length=210, default='')  # 题目
    option_a = models.CharField(verbose_name="选项A", max_length=100, default='')
    score_a = models.IntegerField(verbose_name="选项A得分", default=0)  # 选项A对应的得分

    option_b = models.CharField(verbose_name="选项B", max_length=100, default='')
    score_b = models.IntegerField(verbose_name="选项B得分", default=0)  # 选项B对应的得分

    option_c = models.CharField(verbose_name="选项C", max_length=100, default='')
    score_c = models.IntegerField(verbose_name="选项C得分", default=0)  # 选项C对应的得分

    option_d = models.CharField(verbose_name="选项D", max_length=100, default='')
    score_d = models.IntegerField(verbose_name="选项D得分", default=0)  # 选项D对应的得分

    is_active = models.BooleanField('是否活跃', default=True)

    def __str__(self):
        return self.timu

    class Meta:
        db_table = 'tiku'
        verbose_name_plural = '题库'

# 学生评价模型
class PingJia(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)  # id
    kecheng = models.ForeignKey(to="KeCheng", on_delete=models.CASCADE, verbose_name="课程")
    student = models.ForeignKey(to="Students", on_delete=models.CASCADE, verbose_name="学生")

    question = models.ForeignKey(TiKu, on_delete=models.CASCADE, verbose_name="题目")
    student_answer = models.CharField(verbose_name="学生答案", max_length=1, choices=(('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')), default='A')

    score = models.IntegerField(verbose_name="得分", default=0)  # 存储学生在该题目的得分
    s_liuyan = models.TextField(verbose_name="学生留言", default='', max_length=210, null=True)

    is_active = models.BooleanField('是否活跃', default=True)

    def save(self, *args, **kwargs):
        # 根据学生选择的答案设置得分
        if self.student_answer == 'A':
            self.score = self.question.score_a
        elif self.student_answer == 'B':
            self.score = self.question.score_b
        elif self.student_answer == 'C':
            self.score = self.question.score_c
        elif self.student_answer == 'D':
            self.score = self.question.score_d
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'pingjia'
        verbose_name_plural = '评价'
