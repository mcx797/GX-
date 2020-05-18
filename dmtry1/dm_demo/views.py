from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from dm_demo.models import AdminTab
from dm_demo.models import AchievementTab
from dm_demo.models import Department
from dm_demo.models import AchievementAuthenTab
from dm_demo.models import ScholarTab
from dm_demo.models import ScholarAchievementTab, scholar_department_tab
from dm_demo.models import SchAchAuthenTab
from dm_demo.models import ReportTab
from dm_demo.models import user_tab, student_tab
from dm_demo.models import authen_tab,user_authen_tab
from dm_demo.models import new_achievement_tab, new_relation_tab
from dm_demo.models import collect_achievement_tab, collect_scholar_tab

from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail
import datetime
import requests
from django.conf import settings

from collections import defaultdict
import csv
import json
import re
import xlrd
import os




"""
 django.http模块中定义了HttpResponse 对象的API
 作用：不需要调用模板直接返回数据
 HttpResponse属性：
    content: 返回内容,字符串类型
    charset: 响应的编码字符集
    status_code: HTTP响应的状态码
"""



"""
hello 为一个视图函数，每个视图函数必须第一个参数为request。哪怕用不到request。
request是django.http.HttpRequest的一个实例
"""

admin_id = ''
dep_info = ''
ach_info = ''
newach_auth = ''
sch_ach_auth = ''
user_counter = [[0, 0, 0] for i in range(12)]
user_sub = [[0, 0, 0] for i in range(12)]
# if datetime.datetime.now().month == 5:
#     print("yes")
ach_all = [-1]*7
ach_counter = [0]*12
ach_sub = [0]*12
sch_info = ''
stu_info = ''
path=[]


def hello(request):
    return HttpResponse('Hello World')


def msg(request, name, age):
    return HttpResponse('My name is ' + name + ', i am ' + age + 'years old cl is my dad')


def homepage(request):
    # id = admin_id
    global user_counter
    global ach_all
    global user_sub
    global ach_counter
    global ach_sub
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    last0 = 0
    last1 = 0
    last2 = 0
    last_ach = 0
    if month == 1:
        last0 = user_counter[11][0]
        last1 = user_counter[11][1]
        last2 = user_counter[11][2]
        last_ach = ach_counter[11]
        user_counter = [[0, 0, 0] for i in range(12)]
        ach_all[0] = ach_all[2]
        ach_all[1] = ach_all[4]
        ach_all[2] = ach_all[6]
    else:
        last0 = user_counter[month-2][0]
        last1 = user_counter[month-2][1]
        last2 = user_counter[month-2][2]
        last_ach = ach_counter[month-2]
    user_counter[month-1][0] = user_tab.objects.count()
    user_counter[month-1][1] = len(ScholarTab.objects.filter(flag=1))
    user_counter[month-1][2] = student_tab.objects.count()
    ach_counter[month-1] = AchievementTab.objects.count()
    user_sub[month-1][0] = user_counter[month-1][0] - last0
    user_sub[month-1][1] = user_counter[month-1][1] - last1
    user_sub[month-1][2] = user_counter[month-1][2] - last2
    ach_all[3] = max(ach_counter[0], ach_counter[1], ach_counter[2])
    ach_all[4] = max(ach_counter[3], ach_counter[4], ach_counter[5])
    ach_all[5] = max(ach_counter[6], ach_counter[7], ach_counter[8])
    ach_all[6] = max(ach_counter[9], ach_counter[10], ach_counter[11])
    ach_sub[month-1] = ach_counter[month-1] - last_ach
    dict = {'admin_id': admin_id, 'user_counter': user_counter, 'user_sub': user_sub, 'year': year, 'month': month, 'ach_sub': ach_sub, 'ach_all': ach_all}
    return render(request, 'Dashio/index.html', {'dict': dict})


def login(request):
    if request.method == "GET":  # 如果提交方式为GET即显示login.html
        return render(request, "Dashio/login.html")
    else:  # 如果提交方式为POST
        id = request.POST.get('adminid')
        pwd = request.POST.get('password')
        if AdminTab.objects.filter(id=id).exists():
            if AdminTab.objects.filter(id=id)[0].password == pwd:
                global admin_id
                admin_id = id
                return redirect('/server/')
            else:
                return render(request, 'Dashio/login.html', {'script': "alert", 'wrong': '密码错误'})
        else:
            if id == '':
                return render(request, 'Dashio/login.html', {'script': "alert", 'wrong': '请填写登陆信息'})
            else:
                return render(request, 'Dashio/login.html', {'script': "alert", 'wrong': '该账号不存在'})


# 新加的内容
# 查看成果——对成果进行操作
def check_ach(request):
    if request.method == "GET":  # 如果提交方式为GET即显示check_achiev.html
        size = ""
        all_ach = AchievementTab.objects.filter()
        dict = {'all_achievements': all_ach, 'admin_id': admin_id, 'size': size}
        if "img" not in request.path_info:
            path.append(request.path_info)
        return render(request, 'Dashio/check_achiev.html', {'all_ach_dict': dict})
    else:  # 如果提交方式为POST
        all_ach = AchievementTab.objects.filter()
        return


# 删除某项成果
def delete_one_ach(request, id):
    AchievementTab.objects.filter(a_id=id).delete()
    return redirect('/checkachievement')


# 查看某项成果的详细信息
def check_one_ach(request, id):
    err_msg = ''
    if request.method == "GET":
        ach_info = AchievementTab.objects.filter(a_id=id)[0]
        dict = {'admin_id': admin_id, 'ach_info': ach_info, 'err_msg': err_msg}
        if "img" not in request.path_info:
            path.append(request.path_info)
            # print(request.path_info)
        return render(request, "Dashio/check_achiev_detail.html", {'check_ach': dict})
    else:
        return


# 修改某项成果
def edit_one_ach(request, id):
    global ach_info
    err_msg = ""
    a_id = id
    if request.method == "GET":
        ach_info = AchievementTab.objects.filter(a_id=id)[0]
        dict = {'admin_id': admin_id, 'ach_info': ach_info, 'err_msg': err_msg}
        return render(request, "Dashio/edit_achievement.html", {'edit_ach': dict})
    else:  # 如果提交方式为POST
        name = request.POST.get('name')
        year = request.POST.get('year')
        author_name = request.POST.get('authors')
        citation = request.POST.get('cite')
        j_a_name = request.POST.get('journal')
        file = request.POST.get('file')
        link = request.POST.get('link')
        if not year.isdigit():
            err_msg = "请填写正确发表年份"
            dict = {'admin_id': admin_id, 'ach_info': ach_info, 'err_msg': err_msg}
            return render(request, 'Dashio/edit_achievement.html', {'edit_ach': dict})
        elif not citation.isdigit():
            err_msg = "请填写正确引用数"
            dict = {'admin_id': admin_id, 'ach_info': ach_info, 'err_msg': err_msg}
            return render(request, 'Dashio/edit_achievement.html', {'edit_ach': dict})
        else:
            # 这里file需要换成file的存储位置！！！！！！！！
            # file_site = "no"
            AchievementTab.objects.filter(a_id=a_id).update(name=name, year=year, author_name=author_name, citation=citation,
                                      j_a_name=j_a_name, file=file, link=link)
            err_msg = "修改成果项成功"
            ach_info = AchievementTab.objects.filter(a_id=a_id)[0]
            dict = {'admin_id': admin_id, 'ach_info': ach_info, 'err_msg': err_msg}
            return render(request, 'Dashio/edit_achievement.html', {'edit_ach': dict})


# 添加成果
def add_achievement(request):
    err_msg = ""
    if request.method == "GET":
        dict = {'admin_id': admin_id, 'err_msg': err_msg}
        return render(request, "Dashio/add_achievement.html", {'add_ach': dict})
    else:  # 如果提交方式为POST
        name = request.POST.get('name')
        year = request.POST.get('year')
        author_name = request.POST.get('authors')
        citation = request.POST.get('cite')
        j_a_name = request.POST.get('journal')
        file = request.POST.get('file')
        link = request.POST.get('link')
        if not year.isdigit():
            err_msg = "请填写正确发表年份"
            dict = {'admin_id': admin_id, 'err_msg': err_msg}
            return render(request, 'Dashio/add_achievement.html', {'add_ach': dict})
        elif not citation.isdigit():
            err_msg = "请填写正确引用数"
            dict = {'admin_id': admin_id, 'err_msg': err_msg}
            return render(request, 'Dashio/add_achievement.html', {'add_ach': dict})
        else:
            if AchievementTab.objects.filter(name=name).exists():
                # 这里大概还需要检查作者？？？？
                err_msg = "该成果已存在"
                dict = {'admin_id': admin_id, 'err_msg': err_msg}
                return render(request, 'Dashio/add_achievement.html', {'add_ach': dict})
            else:
                # 这里file需要换成file的存储位置！！！！！！！！
                file_site = "no"
                AchievementTab.objects.create(name=name, year=year, author_name=author_name, citation=citation, j_a_name=j_a_name, file=file_site, link=link)
                err_msg = "添加成果项成功"
                dict = {'admin_id': admin_id, 'err_msg': err_msg}
                return render(request, 'Dashio/add_achievement.html', {'add_ach': dict})


# 显示所有新的成果认证申请信息
def check_newach_authen(request):
    if request.method == "GET":  # 如果提交方式为GET即显示check_achiev.html
        all_authen1 = AchievementAuthenTab.objects.filter()
        all_authen2 = SchAchAuthenTab.objects.filter()
        newauth = []
        for auth in all_authen2:
            newauth.append(NewSchAchAuthen(auth))
        dict = {'all_authen1': all_authen1, 'all_authen2': newauth, 'admin_id': admin_id}
        return render(request, 'Dashio/check_achiev_authen.html', {'ach_authen': dict})
    else:  # 如果提交方式为POST
        all_authen = AchievementTab.objects.filter()
        return


# 查看新添成果认证详情
def check_one_newach_authen(request, id):
    authen_id = id
    if request.method == "GET":
        auth_info = AchievementAuthenTab.objects.filter(id=id)[0]
        # newach_auth = auth_info
        scholar_id = auth_info.scholar_id
        scholar_name = ScholarTab.objects.filter(scholar_id=scholar_id)[0].name
        dict = {'admin_id': admin_id, 'auth_info': auth_info, 'scholar_name': scholar_name}
        return render(request, "Dashio/check_newachiev_details.html", {'check_newauth': dict})
    else:
        newach_auth = AchievementAuthenTab.objects.filter(id=authen_id)[0]
        # 通过认证，加入成果表
        AchievementTab.objects.create(name=newach_auth.a_name, year=newach_auth.year,
                                      author_name=newach_auth.author_name, citation=newach_auth.citation,
                                      j_a_name=newach_auth.j_a_name, file=newach_auth.file, link=newach_auth.link)
        AchievementAuthenTab.objects.filter(id=newach_auth.id).delete()
        a_id = AchievementTab.objects.filter(name = newach_auth.a_name)[0].a_id
        # newach_auth = AchievementAuthenTab.objects.filter(id=id)[0]
        ScholarAchievementTab.objects.create(scholar_id=newach_auth.scholar_id, a_id = a_id)
        # 将相同成果名的成果申请加入到关联申请表中
        auths = AchievementAuthenTab.objects.filter(a_name = newach_auth.a_name)
        for auth in auths:
            SchAchAuthenTab.objects.create(scholar_id=auth.scholar_id, a_id = a_id)
            AchievementAuthenTab.objects.filter(id = auth.id).delete()
        all_authen1 = AchievementAuthenTab.objects.filter()
        all_authen2 = SchAchAuthenTab.objects.filter()
        newauth = []
        for auth in all_authen2:
            newauth.append(NewSchAchAuthen(auth))
        err_msg = "成果认证成功"
        dict = {'all_authen1': all_authen1, 'all_authen2': newauth, 'admin_id': admin_id, 'err_msg': err_msg}
        return render(request, 'Dashio/check_achiev_authen.html', {'ach_authen': dict})


# 删除成果认证信息
def delete_one_newauthen(request, id):
    AchievementAuthenTab.objects.filter(id=id).delete()
    return redirect('/check_newach_authen')


class NewSchAchAuthen():
    def __init__(self, auth):
        self.authen = auth
        self.a_name = AchievementTab.objects.filter(a_id=auth.a_id)[0].name
        self.scholar_name = ScholarTab.objects.filter(scholar_id=auth.scholar_id)[0].name


# 查看成果关联认证详情
def check_one_sch_ach_authen(request, id):
    global sch_ach_auth
    if request.method == "GET":
        auth_info = SchAchAuthenTab.objects.filter(id=id)[0]
        sch_ach_auth = auth_info
        scholar_id = auth_info.scholar_id
        a_id = auth_info.a_id
        scholar_name = ScholarTab.objects.filter(scholar_id=scholar_id)[0].name
        ach_info = AchievementTab.objects.filter(a_id=a_id)[0]
        a_name = ach_info.name
        year = ach_info.year
        author_name = ach_info.author_name
        citation = ach_info.citation
        j_a_name = ach_info.j_a_name
        file = ach_info.file
        link = ach_info.link
        dict = {'admin_id': admin_id, 'auth_info': auth_info, 'scholar_name': scholar_name, 'a_name': a_name,
                'year': year, 'author_name': author_name, 'citation': citation, 'j_a_name':j_a_name,
                'file':file, 'link':link}
        return render(request, "Dashio/check_schach_authen_details.html", {'check_schach_auth': dict})
    else:
        sch_ach_auth = SchAchAuthenTab.objects.filter(id=id)[0]
        ScholarAchievementTab.objects.create(scholar_id=sch_ach_auth.scholar_id, a_id=sch_ach_auth.a_id)
        SchAchAuthenTab.objects.filter(id=id).delete()
        all_authen1 = AchievementAuthenTab.objects.filter()
        all_authen2 = SchAchAuthenTab.objects.filter()
        newauth = []
        for auth in all_authen2:
            newauth.append(NewSchAchAuthen(auth))
        err_msg = "成果关联认证成功"
        dict = {'all_authen1': all_authen1, 'all_authen2': newauth, 'admin_id': admin_id, 'err_msg':err_msg}
        return render(request, 'Dashio/check_achiev_authen.html', {'ach_authen': dict})


# 删除成果关联认证
def delete_one_schach_authen(request, id):
    SchAchAuthenTab.objects.filter(id=id).delete()
    return redirect('/check_newach_authen')


# 查看院系信息——对院系信息进行操作
def check_department(request):
    if request.method == "GET":  # 如果提交方式为GET即显示login.html
        all_dep = Department.objects.filter()
        dict = {'all_departments': all_dep, 'admin_id': admin_id}
        if "img" not in request.path_info:
            path.append(request.path_info)
        return render(request, 'Dashio/check_department.html', {'all_dep_dict': dict})
    else:  # 如果提交方式为POST
        return


# 删除某个院系
def delete_one_dep(request, id):
    Department.objects.filter(d_id=id).delete()
    return redirect('/checkdepartment')


# 查看某个院系的详细信息
def check_one_dep(request, id):
    err_msg = ''
    if request.method == "GET":
        dep_info = Department.objects.filter(d_id=id)[0]
        dict = {'admin_id': admin_id, 'dep_info': dep_info, 'err_msg': err_msg}
        if "img" not in request.path_info:
            path.append(request.path_info)
        return render(request, "Dashio/check_dep_brief.html", {'check_dep': dict})
    else:
        return


# 修改某个院系
def edit_one_dep(request, id):
    global dep_info
    err_msg = ""
    d_id=id
    if request.method == "GET":
        dep_info = Department.objects.filter(d_id=id)[0]
        dict = {'admin_id': admin_id, 'dep_info': dep_info, 'err_msg': err_msg}
        return render(request, "Dashio/edit_department.html", {'edit_dep': dict})
    else:  # 如果提交方式为POST
        number = request.POST.get('number')
        name = request.POST.get('d_name')
        brief = request.POST.get('brief_info')
        if not number.isdigit():
            err_msg = "院系编号需要由数字组成"
            dict = {'admin_id': admin_id, 'dep_info': dep_info, 'err_msg': err_msg}
            return render(request, 'Dashio/edit_department.html', {'edit_dep': dict})
        elif len(number) != 2:
            err_msg = "院系编号需有2位数字"
            dict = {'admin_id': admin_id, 'dep_info': dep_info, 'err_msg': err_msg}
            return render(request, 'Dashio/add_department.html', {'edit_dep': dict})
        else:
            Department.objects.filter(d_id=id).update(number=number, name=name, brief=brief)
            err_msg = "院系信息修改成功"
            dep_info = Department.objects.filter(d_id=d_id)[0]
            dict = {'admin_id': admin_id, 'dep_info': dep_info, 'err_msg': err_msg}
            return render(request, 'Dashio/edit_department.html', {'edit_dep': dict})


# 添加某个院系
def add_department(request):
    err_msg = ""
    if request.method == "GET":
        dict = {'admin_id': admin_id, 'err_msg': err_msg}
        return render(request, "Dashio/add_department.html", {'add_dep': dict})
    else:  # 如果提交方式为POST
        number = request.POST.get('number')
        name = request.POST.get('d_name')
        brief = request.POST.get('brief_info')
        if not number.isdigit():
            err_msg = "院系编号需要由数字组成"
            dict = {'admin_id': admin_id, 'err_msg': err_msg}
            # return render(request, "Dashio/add_department.html", {'add_dep': dict})
            return render(request, 'Dashio/add_department.html', {'add_dep': dict})
        elif len(number) != 2:
            err_msg = "院系编号需有2位数字"
            dict = {'admin_id': admin_id, 'err_msg': err_msg}
            return render(request, 'Dashio/add_department.html', {'add_dep': dict})
        else:
            if Department.objects.filter(number=number).exists():
                err_msg = "该院系编号已存在"
                dict = {'admin_id': admin_id, 'err_msg': err_msg}
                return render(request, 'Dashio/add_department.html', {'add_dep': dict})
            elif Department.objects.filter(name=name).exists():
                err_msg = "该院系名称已存在"
                dict = {'admin_id': admin_id, 'err_msg': err_msg}
                return render(request, 'Dashio/add_department.html', {'add_dep': dict})
            else:
                Department.objects.create(number=number, name=name, brief=brief)
                err_msg = "添加院系成功"
                dict = {'admin_id': admin_id, 'err_msg': err_msg}
                return render(request, 'Dashio/add_department.html', {'add_dep': dict})


# 查看举报信息
def check_report(request):
    if request.method == "GET":  # 如果提交方式为GET即显示login.html
        all_report = ReportTab.objects.filter(flag=0)
        dict = {'all_reports': all_report, 'admin_id': admin_id}
        return render(request, 'Dashio/check_report.html', {'all_rep_dict': dict})
    else:  # 如果提交方式为POST
        return


# 删除某个举报信息
def delete_one_report(request, id):
    ReportTab.objects.filter(r_id=id).delete()
    return redirect('/checkreport')


# 通过某个举报信息
def check_one_report(request, id):
    if request.method == "GET":
        ReportTab.objects.filter(r_id=id).update(flag=1)
        return redirect('/checkreport')
    else:
        return


# 用户相关
# 查看学者用户
def scholar(request):
    size = ''
    dep = ''
    all_scholar = ScholarTab.objects.all(flag=1)
    dict = {'admin_id': admin_id, 'all_sch': all_scholar, 'size': size, 'dep': dep}
    if "img" not in request.path_info:
        path.append(request.path_info)
    return render(request, 'Dashio/scholar.html', {'all_scholar': dict})


# 删除学者用户
def del_scholar(request, id):
    ScholarTab.objects.filter(user_id=id).delete()
    user_tab.objects.filter(user_id=id).delete()
    return redirect('/scholar')


# 查看学者信息详情
def check_one_scholar(request, id):
    if request.method == "GET":
        sch_info = ScholarTab.objects.filter(user_id=id)[0]
        dict = {'admin_id': admin_id, 'sch_info': sch_info}
        return render(request, "Dashio/check_scholar_info.html", {'check_sch': dict})
    else:
        return


# 修改学者信息详情
def edit_one_scholar(request, id):
    global sch_info
    err_msg = ""
    user_id=id
    if request.method == "GET":
        sch_info = ScholarTab.objects.filter(user_id=id)[0]
        dict = {'admin_id': admin_id, 'sch_info': sch_info, 'err_msg': err_msg}
        return render(request, "Dashio/edit_scholar.html", {'edit_sch': dict})
    else:  # 如果提交方式为POST
        name = request.POST.get('name')
        school = request.POST.get('school')
        email = request.POST.get('email')
        p_title = request.POST.get('p_title')
        if len(email) <= 7 or re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is None:
            err_msg = "邮箱格式错误"
            dict = {'admin_id': admin_id, 'sch_info': sch_info, 'err_msg': err_msg}
            return render(request, 'Dashio/edit_scholar.html', {'edit_sch': dict})
        else:
            ScholarTab.objects.filter(user_id = user_id).update(name=name, school=school, email=email, p_title=p_title)
            err_msg = "学者信息修改成功"
            sch_info = ScholarTab.objects.filter(user_id=user_id)[0]
            dict = {'admin_id': admin_id, 'sch_info': sch_info, 'err_msg': err_msg}
            return render(request, "Dashio/edit_scholar.html", {'edit_sch': dict})


# 查看学生用户
def student(request):
    all_student = student_tab.objects.all()
    dict = {'admin_id': admin_id, 'all_student': all_student}
    return render(request, 'Dashio/student.html', {'all_student_dict': dict})


# 删除学生用户
def del_student(request,id):
    student_tab.objects.filter(user_id=id).delete()
    user_tab.objects.filter(user_id=id).delete()
    return redirect('/student')


# 查看学生信息详情
def check_one_student(request, id):
    if request.method == "GET":
        stu_info = student_tab.objects.filter(user_id=id)[0]
        dict = {'admin_id': admin_id, 'stu_info': stu_info}
        return render(request, "Dashio/check_student_info.html", {'check_student': dict})
    else:
        return


# 修改学生信息详情
def edit_one_student(request, id):
    global stu_info
    err_msg = ""
    user_id=id
    if request.method == "GET":
        stu_info = student_tab.objects.filter(user_id=id)[0]
        dict = {'admin_id': admin_id, 'stu_info': stu_info, 'err_msg': err_msg}
        return render(request, "Dashio/edit_student.html", {'edit_student': dict})
    else:  # 如果提交方式为POST
        name = request.POST.get('name')
        school = request.POST.get('school')
        email = request.POST.get('email')
        if len(email) <= 7 or re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is None:
            err_msg = "邮箱格式错误"
            dict = {'admin_id': admin_id, 'stu_info': stu_info, 'err_msg': err_msg}
            return render(request, "Dashio/edit_student.html", {'edit_student': dict})
        else:
            student_tab.objects.filter(user_id = user_id).update(name=name, school=school, email=email)
            err_msg = "学生信息修改成功"
            stu_info = student_tab.objects.filter(user_id=user_id)[0]
            dict = {'admin_id': admin_id, 'stu_info': stu_info, 'err_msg': err_msg}
            return render(request, "Dashio/edit_student.html", {'edit_student': dict})


# 查看用户身份申请
def authen_user(request):
    all_authen = authen_tab.objects.all()
    new_authen = []
    for authen in all_authen:
        new_authen.append(NewAuthen(authen))
    dict = {'admin_id': admin_id, 'all_authen': new_authen}
    return render(request, 'Dashio/authen_user.html', {'all_authen_dict': dict})


class NewAuthen():
    def __init__(self, auth):
        self.authen = auth
        if auth.identity is 1:
            self.idenstr = '学者'
        else:
            self.idenstr = '学生'


# 删除身份申请
def del_authen(request, authen_id):
    # user_id = request.GET.get('id')
    authen_tab.objects.filter(authen_id=authen_id).delete()
    user_authen_tab.objects.filter(authen_id=authen_id).delete()
    return redirect('/authen_user')


# 通过用户的身份申请
def pass_authen(request, authen_id):  # 通过后向学者表/用户表中添加对应表项
    authen_info = authen_tab.objects.get(authen_id=authen_id)
    user = user_authen_tab.objects.get(authen_id=authen_id)
    user_info = user_tab.objects.get(user_id=user.user_id)
    if authen_info.identity == 1:  # 学者
        ScholarTab.objects.create(user_id=user_info.user_id, school="buaa", name=user_info.user_name, email=authen_info.email, p_title="default")
        user_tab.objects.filter(user_id=user_info.user_id).update(authority=1)
    elif authen_info.identity == 2:  # 学生
        student_tab.objects.create(user_id=user_info.user_id,school="buaa", name=user_info.user_name,email=authen_info.email)
        user_tab.objects.filter(user_id=user_info.user_id).update(authority=2)
    return redirect('/del_authen/'+authen_id)


# 查看所有用户信息
def check_all_user(request):
    if request.method == "GET":  # 如果提交方式为GET即显示login.html
        all_user = user_tab.objects.filter()
        dict = {'all_users': all_user, 'admin_id': admin_id}
        return render(request, 'Dashio/check_all_user.html', {'user_dict': dict})
    else:  # 如果提交方式为POST
        return


# 删除用户信息
def delete_user(request, id):
    user = user_tab.objects.get(user_id=id)
    if user.authority == 1:  #学者
        ScholarTab.objects.filter(user_id=id).delete()
    if user.authority == 2:  #学生
        student_tab.objects.filter(user_id=id).delete() 
    user_tab.objects.filter(user_id=id).delete()
    return redirect('/checkuser')


# 新爬取成果管理员确认
def add_get_achievement(request):
    # 将待确认成果展示
    item = new_achievement_tab.objects.all()
    dict = {'item': item, 'admin_id': admin_id}
    # print(item)
    return render(request, 'Dashio/add_get_achievement.html', {'dict': dict})


# 新爬取成果通过
def pass_new_achievement(request, id):
    ach = new_achievement_tab.objects.get(a_id=id)
    # 将成果加入成果表中
    new_a = AchievementTab.objects.create(name=ach.name, year=ach.year, author_name=ach.user_name,
                                          citation=ach.citation, j_a_name=ach.j_a_name, file=ach.file,
                                          link=ach.link, get_id=ach.get_id, keyword=ach.keyword)
    # 将对应关系加入待认领表中
    with open(relation_all_file, 'r', encoding='utf-8') as relation_csv:
        reader = csv.DictReader(relation_csv)
        data = []
        for line in reader:
            if int(line[1]) == ach.get_id:
                data.append(line['au_id'])
        for i in data:
            new_rel = new_relation_tab.objects.create(auth_id=i,ach_id=ach.get_id)
    return redirect('/del_new_achievement'+'/'+id)


def del_new_achievement(request, id):
    new_achievement_tab.objects.filter(a_id=id).delete()
    return redirect('/add_get_achievement')


# ++++++++++++++++++++++++++++++++++++++
# 查看某位学者相关的成果信息
def check_scholar_achievement(request, id):
    scholar_id = id
    # 存在关联信息
    if ScholarAchievementTab.objects.filter(scholar_id=scholar_id).exists():
        size = ScholarTab.objects.filter(scholar_id=scholar_id)[0]
        all_ach = []
        for i in ScholarAchievementTab.objects.filter(scholar_id=scholar_id):
            all_ach.append(AchievementTab.objects.filter(a_id=i.a_id)[0])
        dict = {'all_achievements': all_ach, 'admin_id': admin_id, 'size': size}
        if "img" not in request.path_info:
            path.append(request.path_info)
            print(request.path_info)
        return render(request, 'Dashio/check_achiev.html', {'all_ach_dict': dict})
    else:
        err_msg = "该学者暂无可查询成果"
        sch_info = ScholarTab.objects.filter(scholar_id=scholar_id)[0]
        dict = {'admin_id': admin_id, 'sch_info': sch_info, 'err_msg': err_msg}
        return render(request, "Dashio/check_scholar_info.html", {'check_sch': dict})


# 查看某一成果的相关学者
def check_achievement_scholar(request, id):
    a_id = id
    dep = ''
    # 存在关联信息
    if scholar_department_tab.objects.filter(a_id=a_id).exists():
        size = AchievementTab.objects.filter(a_id=a_id)[0]
        all_scholar = []
        for i in scholar_department_tab.objects.filter(a_id=a_id):
            all_scholar.append(ScholarTab.objects.filter(scholar_id=i.scholar_id)[0])
        dict = {'admin_id': admin_id, 'all_sch': all_scholar, 'size': size, 'dep': dep}
        if "img" not in request.path_info:
            path.append(request.path_info)
            print(request.path_info)
        return render(request, 'Dashio/scholar.html', {'all_scholar': dict})
    else:
        err_msg = "该成果暂无可查询相关学者信息"
        ach_info = AchievementTab.objects.filter(a_id=a_id)[0]
        dict = {'admin_id': admin_id, 'ach_info': ach_info, 'err_msg': err_msg}
        return render(request, "Dashio/check_achiev_detail.html", {'check_ach': dict})


# 查看某一院系的相关学者
def check_department_scholar(request, id):
    d_id = id
    # 存在关联信息
    if ScholarDepartmentTab.objects.filter(d_id=d_id).exists():
        dep = Department.objects.filter(d_id=d_id)[0]
        size = ''
        all_scholar = []
        for i in ScholarDepartmentTab.objects.filter(d_id=d_id):
            all_scholar.append(ScholarTab.objects.filter(scholar_id=i.scholar_id)[0])
        dict = {'admin_id': admin_id, 'all_sch': all_scholar, 'size': size, 'dep': dep}
        if "img" not in request.path_info:
            path.append(request.path_info)
            print(request.path_info)
        return render(request, 'Dashio/scholar.html', {'all_scholar': dict})
    else:
        err_msg = "该成果暂无可查询相关学者信息"
        dep_info = Department.objects.filter(d_id=d_id)[0]
        dict = {'admin_id': admin_id, 'dep_info': dep_info, 'err_msg': err_msg}
        return render(request, "Dashio/check_dep_brief.html", {'check_dep': dict})


# 返回上一页
def to_last_page(request):
    path.pop()
    last_path = path[-1]
    path.pop()
    return redirect(last_path)





def user_id_get(request):
    ScholarIn()
    retData = {}
    return HttpResponse(json.dumps(retData), content_type = "application/json")

'''
#	user = {}
#	if len(user_tab.objects.filter(wechatid = request.GET['wxNickName'])) == 0:
#		user_tab(user_name = request.GET['wxNickName'], wechatid = request.GET['wxNickName'], authority = 0).save()
#	else:
#		user = user_tab.objects.get(wechatid = request.GET['wxNickName'])
#		if user.authority == 1:
#			scholar = ScholarTab.objects.get(user_id = user.user_id)
			retData['school'] = scholar.school
			retData['name'] = scholar.name
			retData['email'] = scholar.email
			retData['sno'] = scholar.scholar_id
		if user.authority == 2:
			student = student_tab.objects.get(user_id = user.user_id)
			retData['school'] = student.school
			retData['name'] = student.name
			retData['email'] = student.email
	retData['id'] = user.user_id
	retData['authority'] = user.authorityi'''
#        return HttpResponse(json.dumps(retData), content_type = "application/json")


def wx_register(request):
	autho = 0
	if (request.GET['authority'] == "学生用户"):
		autho = 2
	if (request.GET['authority'] == "学者用户"):
		autho = 1
	if (autho == 1 or autho == 2):
		print(request.GET['mail'])
		authen_tab(email = request.GET['mail'], name = request.GET['name'], sno = request.GET['schoolid'], identity = autho).save()
		user_tab.objects.filter(wechatid = request.GET['wechatid']).update(user_name = request.GET['name'])
		retData = {}
		retData['b'] = 'b'
		t1 = user_tab.objects.get(wechatid = request.GET['wechatid'])
		t2 = authen_tab.objects.get(name = request.GET['name'])
		print(t1.user_id)
		user_authen_tab(user_id = t1.user_id, authen_id = t2.authen_id).save()
		return HttpResponse(json.dumps(retData), content_type = "application/json")
	retData = {}
	retData['a'] = 'a'
	return HttpResponse(json.dumps(retData), content_type = "application/json")


def hasconnect_A(paper_id, wxid):
	t1 = user_tab.objects.get(wechatid = wxid)
	if len(collect_achievement_tab.objects.filter(user_id = t1.user_id, a_id = paper_id)) == 0:
		return 1
	return 0



def hasconnect_B(paper_id, wxid):
	t1 = user_tab.objects.get(wechatid = wxid)
	if len(collect_scholar_tab.objects.filter(user_id = t1.user_id, scholar_id = paper_id)) == 0:
		return 1
	return 0

def paperInitial(request):
        number = 1
        retData = []
        achieves = AchievementTab.objects.all()
        for i in achieves:
                if number <= 6:
                        a = {}
                        a["id"] = number
                        a["paper_id"] = i.a_id
                        a["useDate"] = i.name
                        a["cx"] = i.author_name
                        a["time"] = i.year
                        a["isShow"] = hasconnect_A(i.a_id, request.GET['WXID'])
                        a["feiyong"] = i.citation
                        number = number + 1
                        retData.append(a)
        return HttpResponse(json.dumps(retData), content_type = "application/json")


def searchTeacher(request):
	text = request.GET['text']
	number = 1
	retData = []
	scholars = ScholarTab.objects.all()
	for i in scholars:
		if text in i.name:
			a = {}
			a["id"] = number
			a["usseData"] = i.name
			a["cx"] = i.school
			a["time"] = i.email
			#a["isShow"] = hasconnect_B(i.scholar_id, request.GET['WXID'])
			number = number + 1
			retData.append(a)
	return HttpResponse(json.dumps(retData), content_type = "application/json") 




def searchPaper(request):
	text = request.GET['text']
	number = 1
	retData = []
	achieves = AchievementTab.objects.all()
	for i in achieves:
		if text in i.name:
			a = {}
			a["id"] = number
			a["paper_id"] = i.a_id
			a["useDate"] = i.name
			a["cx"] = i.author_name
			a["time"] = i.year
			a["isShow"] = hasconnect_A(i.a_id, request.GET['WXID'])
			a["feiyong"] = i.citation
			number = number + 1
			retData.append(a)
	return HttpResponse(json.dumps(retData), content_type = "application/json")


def teacherInitial(request):
        number = 1
        retData = []
        scholars = ScholarTab.objects.all()
        for i in scholars:
                if number <= 6:
                        a = {}
                        a["id"] = number
                        a["usseData"] = i.name
                        a["cx"] = i.school
                        a["time"] = i.email
			#a['isShow'] = hasconnect_B(i.scholar_id, request.GET['WXID'])
                        number = number + 1
                        retData.append(a)
        return HttpResponse(json.dumps(retData), content_type = "application/json")


'''
def collectScholar(request):
	retData = {}
	ScholarName = request.GET['scholarName']
	isCollect = request.GET['isCollect']
	WXID = request.GET['WXID']
	print(ScholarName)
	print(isCollect)
	print(WXID)
	t1 = user_tab.objects.get(wechatid = WXID)
	t2 = scholarTab.objects.get(name = ScholarName)
		if (isCollect == '1'):
			print("hahaha")
			collect_scholar_tab(user_id = t1.user_id, scholar_id = t2.scholar_id).save()
		else:
			print("xixixi")
			collect_scholar_tab(user_id = t1.user_id, scholar_id = t2.scholar_id).delete()
	return HttpResponse(json.dumps(retData), content_type = "application/json")

'''

def collectPaper(request):
	retData = {}
	paperId = request.GET['paperId']
	isCollect = request.GET['isCollect']
	WXID = request.GET['WXID']
	print(paperId)
	print(isCollect)
	print(WXID)
	t1 = user_tab.objects.get(wechatid = WXID)
	if (isCollect == '1'):
		print("hahaha")
		collect_achievement_tab(user_id = t1.user_id, a_id = paperId).save()
	else:
		print("xixixi")
		collect_achievement_tab.objects.filter(user_id = t1.user_id, a_id = paperId).delete()
	return HttpResponse(json.dumps(retData), content_type = "application/json")

def chengguoup(request):
	retData = {}
	print("kkkkk")
	t1 = user_tab.objects.get(wechatid = request.GET['WXID'])
	scholar = ScholarTab.objects.get(user_id = t1.user_id)
	AchievementAuthenTab(a_name = request.GET['name'], scholar_id = scholar.scholar_id, citation = request.GET['citation'], year = request.GET['year']).save()
	print("hahaha")
	retData['a'] = 'a'
	return HttpResponse(json.dumps(retData), content_type = "application/json")


def getCollection(request):
	retData = []
	number = 1
	wxid = request.GET['WXID']
	collection = collect_achievement_tab.objects.all()
	user =  user_tab.objects.get(wechatid = wxid)
	for i in collection:
		if (user.user_id == i.user_id):
			k = AchievementTab.objects.get(a_id = i.a_id)
			a = {}
			a["id"] = number
			a["paper_id"] = k.a_id
			a["useDate"] = k.name
			a["cx"] = k.author_name
			a["time"] = k.year
			a["feiyong"] = k.citation
			number = number + 1
			retData.append(a)
	return HttpResponse(json.dumps(retData), content_type = "application/json")	
	

def Identification(request):
	retData = {}
	brief = request.GET['brief']
	wxid = request.GET['WXID']
	user = user_tab.objects.get(wechatid = wxid)
	#Achie = AchievementTab.objects.get(name = brief)
	#if len (Achie > 1) :
	#	Achie = Achie[0]
	ReportTab(id = user.user_id, user_name = wxid, information = brief + "论文信息存在异常", flag = 0).save()
	return HttpResponse(json.dumps(retData), content_type = "application/json")


def TeacherIdentification(request):
	retData = {}
	name = request.GET['brief']
	wxid = request.GET['WXID']
	print(name)
	print(name)
	print(name)
	user = user_tab.objects.get(wechatid = wxid)
	print(wxid)
	user1 = user_tab.objects.get(user_name = name)
	ReportTab(id = user.user_id, user_name = name, information = "身份信息存在异常", flag = 0).save()
	return HttpResponse(json.dumps(retData), content_type = "application/json")




'''
为用户生成首页的学者信息, 被code2key引用
'''
def getIndexScholarInfo(UserWechatId):
    retData = []
    scholars = ScholarTab.objects.all()
    for i in range(10):
        a = {}
        a['id'] = i
        a['name'] = scholars[i].name
        a['job'] = scholars[i].p_title
        retData.append(a)
    return retData
        


'''
微信用户登录系统时提交自己的code， 管理端转化为openID并进行登录，若是初次使用
则自动为用户注册为访客用户,同时返回首页需要的学者信息，并返回。
'''
def code2key(request):
    retData = {}
    js_code = request.GET['code']
    print("js_code:  %s" %(js_code))
    appid = "wx7aaa067fdee5e983"
    secret = "f0e21a2bfd97b8381a24f0205979b2e7"
    print("appid:  %s" %(appid))
    print("secret:   %s" %(secret))
    wechaturl = "https://api.weixin.qq.com/sns/jscode2session?appid=" + appid +"&secret=" + secret + "&js_code=" + js_code + "&grant_type=authorization_code"
    print(wechaturl)
    js1 = requests.get(wechaturl).json()
    print(js1['openid'])
    retData['openid'] = js1['openid']
    if len(user_tab.objects.filter(wechatid = js1['openid'])) == 0:
        user_tab(user_name = "访客用户", password = '无', wechatid = js1['openid'], authority = 0).save()
    t1 = user_tab.objects.get(wechatid = js1['openid'])
    retData['name'] = t1.user_name
    retData['authority'] = t1.authority
    retData['scholarData'] = getIndexScholarInfo(t1.wechatid)
    return HttpResponse(json.dumps(retData), content_type = "application/json")


'''
得到成果展示的列表

'''
def paperyears(request):
    retData = []
    for i in range(2000, 2020):
        a = {}
        a['id'] = i - 2000
        a['name'] = i
        retData.append(a)
    return HttpResponse(json.dumps(retData), content_type = "application/json")


def findPaperS(number, year):
    retData = []
    achieves = AchievementTab.objects.all()
    times = 0
    for i in achieves:
        if i.year == year:
            a = {}
            a['id'] = times
            a['name'] = i.name
            a['kind'] = i.kind
            a['num_view'] = i.num_view
            times = times + 1
            retData.append(a)
            if times == year:
                return retData
    return retData
            




'''
得到对应年份的成果信息
'''	
def paperInitial(request):
    retData = []
    year = request.GET['year']
    retData = findPaperS(10, year)
    return HttpResponse(json.dumps(retData), content_type = "application/json")
