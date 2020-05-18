from django.db import models
import django.utils.timezone as timezone
# Create your models here.
# class alluser(models.Model):

class AdminTab(models.Model):
    id = models.CharField(max_length=7, primary_key=True)
    password = models.CharField(max_length=16)
    errors = models.IntegerField()

    class Meta:
        # managed = False
        db_table = 'admin_tab'


class AchievementTab(models.Model):
    a_id = models.AutoField(primary_key=True)  # 成果名
    name = models.CharField(max_length=150)  # ???????字节如何换算成位数
    year = models.CharField(max_length=5)
    author_name = models.CharField(max_length=150)
    citation = models.IntegerField()    # 被引数
    j_a_name = models.CharField(max_length=150)   #成果所在期刊/会议
    file = models.CharField(max_length=150)
    link = models.CharField(max_length=150)
    kind = models.CharField(max_length =10) #文献类型
    num_view = models.IntegerField(default=0)#浏览次数
    get_id = models.IntegerField(default=0)

    keyword = models.CharField(max_length=200, default="NULL")

    class Meta:
        # managed = False
        db_table = 'achievement_tab'


class AchievementAuthenTab(models.Model):
    id = models.AutoField(primary_key=True)
    scholar_id = models.IntegerField()
    a_name = models.CharField(max_length=150)
    year = models.CharField(max_length=5)
    author_name = models.CharField(max_length=150)
    citation = models.IntegerField()
    j_a_name = models.CharField(max_length=150)
    file = models.CharField(max_length=150)
    link = models.CharField(max_length=150)
    #keyword = models.CharField(max_length=200, default="NULL")

    class Meta:
        # managed = False
        db_table = 'achievement_authen_tab'


class Department(models.Model):
    d_id = models.AutoField(primary_key=True) #学院id
    number = models.CharField(max_length=2)   #学院号
    name = models.CharField(max_length=30)    #学院名称
    brief = models.CharField(max_length=600)  #学院简介

    class Meta:
        # managed = False
        db_table = 'department_tab'


class ScholarTab(models.Model):
    user_id = models.IntegerField()#学者对应的用户id, 未认领时为-1
    scholar_id = models.AutoField(primary_key=True)#学者在我们系统中的id，唯一标识
    school = models.CharField(max_length=30)#学者学校
    name = models.CharField(max_length=30)#学者姓名
    email = models.CharField(max_length=30)#学者邮箱
    p_title = models.CharField(max_length=30)#职称
    flag = models.IntegerField()              #标志位
    Scholar_Number = models.CharField(max_length = 30) #学者的工号    

    get_id = models.IntegerField(default=0)
    class Meta:
        # managed = False
        db_table = 'scholar_tab'


class ScholarAchievementTab(models.Model):
    id = models.AutoField(primary_key=True)
    scholar_id = models.IntegerField()
    a_id = models.IntegerField()

    class Meta:
        # managed = False
        db_table = 'scholar_achievement_tab'


class SchAchAuthenTab(models.Model):
    id = models.AutoField(primary_key=True)
    scholar_id = models.IntegerField()
    a_id = models.IntegerField()

    class Meta:
        # managed = False
        db_table = 'sch_ach_authen_tab'


class scholar_department_tab(models.Model):
    id = models.AutoField(primary_key=True)
    scholar_id = models.IntegerField()      #学者id
    d_id = models.IntegerField()            #学院id

    class Meta:
        db_table = 'scholar_department_tab'

class ReportTab(models.Model):
    r_id = models.AutoField(primary_key=True)
    id = models.IntegerField()
    user_name = models.CharField(max_length=30)
    information = models.CharField(max_length=300)
    flag = models.IntegerField()

    class Meta:
        # managed = False
        db_table = 'report_tab'


class user_tab(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    wechatid = models.CharField(max_length=30)
    authority_choice = (
        (0, "普通用户"),
        (1, "学者用户"),
        (2, "学生用户")
    )
    authority = models.SmallIntegerField(choices=authority_choice,default=0)
    class Meta:
        # managed = False
        db_table = 'user_tab'


class student_tab(models.Model):
    user_id = models.IntegerField()
    student_id = models.AutoField(primary_key=True)
    school = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    class Meta:
        # managed = False
        db_table = 'student_tab'


class student_achievement_tab(models.Model):
    student_id = models.IntegerField()
    a_id = models.IntegerField()
    class Meta:
        # managed = False
        db_table = 'student_achievement_tab'


class student_department_tab(models.Model):
    student_id = models.IntegerField()
    d_id = models.IntegerField()
    class Meta:
        db_table = 'student_department_tab'


class authen_tab(models.Model):
    authen_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=30)
    name = models.CharField(max_length=30)
    sno = models.CharField(max_length=30)
    identity_choice = (
        (0, "普通用户"),
        (1, "学者用户"),
        (2, "学生用户")
    )
    identity = models.SmallIntegerField(choices=identity_choice)
    class Meta:
        # managed = False
        db_table = 'authen_tab'


class user_authen_tab(models.Model):
#    u_id = models.AutoField(primary_key=True)
    authen_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()

    class Meta:
        # unique_together = ("authen_id","user_id")
        db_table = 'user_authen_tab'


# 爬取成果添加
class add_achievement_tab(models.Model):
    temp_id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(default=timezone.now)  # 创建时间
    title = models.TextField(max_length=150)  # 成果名字
    author = models.TextField(max_length=300)  # 作者名字
    get_ach_id = models.IntegerField(default=0)  # 爬虫成果id
    get_auth_id = models.IntegerField(default=0)  # 爬虫作者id
    class Meta:
        db_table = 'add_achievement_tab'


class new_achievement_tab(models.Model):
    a_id = models.AutoField(primary_key=True)  # 成果名
    name = models.CharField(max_length=150)  # ???????字节如何换算成位数
    year = models.CharField(max_length=5)
    user_name = models.CharField(max_length=150)
    citation = models.IntegerField()    # 被引数
    j_a_name = models.CharField(max_length=150)   #
    file = models.CharField(max_length=150)
    link = models.CharField(max_length=150)
    create_time = models.DateTimeField(default=timezone.now)  # 创建时间

    get_id = models.IntegerField(default=0)

    keyword = models.CharField(max_length=200, default="NULL")

    class Meta:
        # managed = False
        db_table = 'new_achievement_tab'


class new_relation_tab(models.Model):
    a_id = models.AutoField(primary_key=True)
    auth_id = models.IntegerField(default=0)
    ach_id = models.IntegerField(default=0)

    class Meta:
        # managed = False
        db_table = 'new_relation_tab'



class collect_achievement_tab(models.Model):
    id = models.AutoField(primary_key = True)
    user_id = models.IntegerField()
    a_id = models.IntegerField()
   
    class Meta:
        # managed = False
        db_table = 'collect_achievement_tab' 

class collect_scholar_tab(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    scholar_id = models.IntegerField()

    class Meta:
        # managed = False
        db_table = 'collect_scholar_tab'
