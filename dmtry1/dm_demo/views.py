from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render


from dm_demo.models import admin_tab, achievement_tab, achievement_brief_tab, keyword_tab
from dm_demo.models import achieve_keyword_tab, achievement_authen_tab, sch_ach_authen_tab
from dm_demo.models import scholar_achievement_tab, department_tab, scholar_tab, scholar_change_tab
from dm_demo.models import information_tab, person_inform_tab, scholar_brief_intro_tab
from dm_demo.models import scholar_department_tab, report_tab, user_tab, student_tab
from dm_demo.models import student_achievement_tab, student_department_tab
from dm_demo.models import authen_tab, user_authen_tab, collect_achievement_tab
from dm_demo.models import collect_scholar_tab, reserch_direction_tab
from dm_demo.models import scholar_direction_tab, new_relation_tab

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
    if scholar_department_tab.objects.filter(d_id=d_id).exists():
        dep = department_tab.objects.filter(d_id=d_id)[0]
        size = ''
        all_scholar = []
        for i in scholar_department_tab.objects.filter(d_id=d_id):
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



'''
为用户生成首页的学者信息, 被code2key引用
'''
def getIndexScholarInfo(UserWechatId):
    retData = []
    scholars = scholar_tab.objects.all()
    for i in range(10):
        a = {}
        a['id'] = i
        a['get_id'] = scholars[i].get_id
        a['scholar_id'] = scholars[i].scholar_id
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
    appid = "wx7aaa067fdee5e983"
    secret = "f0e21a2bfd97b8381a24f0205979b2e7"
    wechaturl = "https://api.weixin.qq.com/sns/jscode2session?appid=" + appid +"&secret=" + secret + "&js_code=" + js_code + "&grant_type=authorization_code"
    js1 = requests.get(wechaturl).json()
    if len(user_tab.objects.filter(wechatid = js1['openid'])) == 0:
        user_tab(user_name = "访客用户", wechatid = js1['openid'], authority = 0).save()
    t1 = user_tab.objects.get(wechatid = js1['openid'])
    retData['name'] = t1.user_name
    retData['user_id'] = t1.user_id
    retData['authority'] = t1.authority
    retData['scholarData'] = getIndexScholarInfo(t1.user_id)
    return HttpResponse(json.dumps(retData), content_type = "application/json")


'''
得到成果展示的列表,当前版本按年份整理，之后希望可以调整为关键词

'''
def paperyears(request):
    retData = []
    for i in range(2000, 2020):
        a = {}
        a['id'] = i - 2000
        a['name'] = i
        retData.append(a)
    return HttpResponse(json.dumps(retData), content_type = "application/json")



'''
给出对应年份的8组成果数据
'''
def findPaperS(number, year):
    retData = []
    achieves = achievement_tab.objects.all()
    times = 0
    for i in achieves:
        if i.year == year:
            a = {}
            a['id'] = times
            a['name'] = i.name
            a['kind'] = i.kind
            a['num_view'] = i.num_view
            a['a_id'] = i.a_id
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
    year = request.GET['Thisyear']
    print(year)
    retData = findPaperS(10, year)
    return HttpResponse(json.dumps(retData), content_type = "application/json")




'''
根据paper的a_id得到具体的paper信息
'''
def AchievementDetail(request):
    retData = {}
    a_id = request.GET['a_id']
    achieve = achievement_tab.objects.get(a_id = a_id)
    user = user_tab.objects.get(user_id = request.GET['user_id'])
    user_id = user.user_id
    if len(collect_achievement_tab.objects.filter(user_id = user_id, a_id = a_id)) == 0:
        retData['faved'] = 0
    else:
        retData['faved'] = 1
    retData['name'] = achieve.name
    retData['type'] = achieve.kind
    retData['author'] =""
    retData['year'] = achieve.year
    retData['link_text'] = achieve.link
    retData['keyword'] = achieve.keyword
    sa1 = scholar_achievement_tab.objects.filter(a_id = a_id)
    print(len(sa1))
    if len(sa1) == 1:
        s1 = scholar_tab.objects.get(scholar_id = sa1[0].scholar_id)
        retData['author'] += s1.name
    else:
        for i in sa1:
            s1 = scholar_tab.objects.get(scholar_id = i.scholar_id)
            retData['author'] += ' '
            retData['author'] += s1.name 
    return HttpResponse(json.dumps(retData), content_type = "application/json")

'''
获取学者展示界面的学院信息
'''

def ScholarDepartment(request):
    retData = []
    depart = department_tab.objects.all()
    for i in depart:
        a = {}
        a['id'] = i.d_id
        a['name'] = i.name
        a['level'] = 1
        retData.append(a)
    return HttpResponse(json.dumps(retData), content_type = "application/json")
'''
根据学院id获取学院中所有的学者
'''

def scholarGet(request):
    retData = []
    num = 0
    d_id = request.GET['id']
    sdt = scholar_department_tab.objects.filter(d_id = d_id)
    for i in sdt:
        a = {}
        s1 = scholar_tab.objects.get(scholar_id = i.scholar_id)
        a['name'] = s1.name
        a['p_title'] = s1.p_title
        a['get_id'] = s1.get_id
        a['email'] = s1.email
        a['id'] = s1.scholar_id
        retData.append(a)
        num += 1
        if (num == 10):
            break
    return HttpResponse(json.dumps(retData), content_type = "application/json")

'''
根据学者id获取相应的学者
'''         
def ScholarDetail(request):
    retData = {} 
    s_id = request.GET['s_id']
    print(s_id)
    user_id = request.GET['user_id']
    scholar = scholar_tab.objects.get(scholar_id = s_id)
    user = user_tab.objects.get(user_id = user_id)
    user_id = user.user_id
    if len(collect_scholar_tab.objects.filter(user_id = user_id, scholar_id = s_id)) == 0:
        retData['faved'] = 0
    else:
        retData['faved'] = 1
    retData['name'] = scholar.name
    st1 = scholar_department_tab.objects.get(scholar_id = s_id)
    depart = department_tab.objects.get(d_id = st1.d_id)
    retData['department'] = depart.name
    retData['position'] = scholar.p_title
    retData['mail'] = scholar.email
    return HttpResponse(json.dumps(retData), content_type = "application/json")



'''
学生认证
'''
def StudentCerti(request):
    retData = {}
    openId = request.GET['openId']
    Name = request.GET['name']
    department = request.GET['department']
    studentNumber = request.GET['studentNumber']
    mail = request.GET['mail']
    authen_tab(email = mail, name = Name, sno = studentNumber, identity = 2).save()
    user_tab.objects.filter(wechatid = openId).update(user_name = Name)
    t1 = user_tab.objects.get(wechatid = openId)
    t2 = authen_tab.objects.get(name = Name)
    user_authen_tab(user_id = t1.user_id, authen_id = t2.authen_id).save()
    return HttpResponse(json.dumps(retData), content_type = "application/json")


'''
成果的收藏与取消收藏
'''
def faveAchievement(request):
    retData = {}
    paperid = request.GET['paperid']
    faved = request.GET['faved']
    user_id = request.GET['user_id']
    a1 = achievement_tab.objects.get(a_id = paperid)
    user = user_tab.objects.get(user_id = user_id)
    if (faved == '1'):
        collect_achievement_tab.objects.get(user_id = user.user_id, a_id = paperid).delete()
        retData['faved'] = 0
    else:
        collect_achievement_tab(user_id = user.user_id, a_id = a1.a_id).save()
        retData['faved'] = 1 
    return HttpResponse(json.dumps(retData), content_type = "application/json")


'''
学者的收藏与取消收藏
'''
def faveScholar(request):
    retData = {}
    s_id = request.GET['s_id']
    faved = request.GET['faved']
    user_id = request.GET['user_id']
    print(s_id)
    s1 = scholar_tab.objects.get(scholar_id = s_id)
    user = user_tab.objects.get(user_id = user_id)
    if (faved == '1'):
        collect_scholar_tab.objects.get(user_id = user.user_id, scholar_id = s_id).delete()
        retData['faved'] = 0
    else:
        collect_scholar_tab(user_id = user.user_id, scholar_id = s_id).save()
        retData['faved'] = 1
    return HttpResponse(json.dumps(retData), content_type = 'application/json')


'''
根据user_id获取用户其他信息
'''
def getUserInfo(request):
    retData = {}
    print(request.GET['user_id'])
    user = user_tab.objects.get(user_id = request.GET['user_id'])
    print(user.user_name)
    retData['user_name'] = user.user_name
    if user.authority == 0:
        retData['studentNumber'] = '请先进行认证'
        retData['school'] = '请先进行认证'
        retData['department'] = '请先进行认证'
        retData['mail'] = '请先进行认证'
    return HttpResponse(json.dumps(retData), content_type = 'application/json')



'''
学生认证
'''
def StudentCerti(request):
    retData = {}
    name = request.GET['name']
    department = request.GET['department']
    studentNumber = request.GET['studentNumber']
    mail = request.GET['mail']
    user_id = request.GET['user_id']
    school = request.GET['school']
    d1 = department_tab.objects.get(name = department)
    authen_tab(email = mail, name = name, sno = studentNumber, department = d1.d_id, identity = 2, school = school)
    return HttpResponse(json.dumps(retData), content_type = 'application/json')

'''
学者认证
'''
def ScholarCerti(request):
    retData = {}
    name = request.GET['name']
    department = request.GET['department']
    studentNumber = request.GET['studentNumber']
    mail = request.GET['mail']
    user_id = request.GET['user_id']
    school = request.GET['school']
    d1 = department_tab.objects.get(name = department)
    authen_tab(email = mail, name = name, sno = studentNumber, department = d1.d_id, identity = 1, school = school)
    return HttpResponse(json.dumps(retData), content_type = 'application/json')
    





'''
展示图片
'''
def show_log(request):
    get_id = request.GET['get_id']
    path = '../image/' + get_id + '.jpg'
    module_dir = os.path.dirname(__file__)
    path = os.path.join(module_dir, path)
    print(path)
    file_one = open(path, "rb")
    return HttpResponse(file_one.read(), content_type = 'image/jpg')



'''
返回用户收藏的学者
'''
def getFavScholar(request):
    retData = []
    user_id = request.GET['user_id']
    collects = collect_scholar_tab.objects.filter(user_id = user_id)
    i = 0
    for collect in collects:
        a = {}
        scholar_id = collect.scholar_id
        scholar = scholar_tab.objects.get(scholar_id = scholar_id)
        a['name'] = scholar.name
        a['position'] = scholar.p_title
        a['get_id'] = scholar.get_id
        a['scholar_id'] = scholar_id
        d_id = scholar_department_tab.objects.get(scholar_id = scholar_id).d_id
        a['department'] = department_tab.objects.get(d_id = d_id).name
        retData.append(a)
    return HttpResponse(json.dumps(retData), content_type = 'application/json')
       

'''
返还用户收藏的成果
'''
def getFavAchievement(request):
    retData = []
    user_id = request.GET['user_id']
    collects = collect_achievement_tab.objects.filter(user_id = user_id)
    i = 0
    for collect in collects:
        a = {}
        a_id = collect.a_id
        achieve = achievement_tab.objects.get(a_id = a_id)
        a['name'] = achieve.name
        a['author'] = achieve.author_name
        a['year'] = achieve.year
        a['a_id'] = achieve.a_id
        retData.append(a)
    return HttpResponse(json.dumps(retData), content_type = 'application/json')
    
    

'''
成果搜索
'''
def AchievementSearch(request):
    retData = []
    search = request.GET['search']
    a1 = achievement_tab.objects.order_by('num_view').reverse()
    for i in a1:
        if search in i.name:
            a = {}
            a['name'] = i.name
            a['author'] = i.author_name
            a['year'] = i.year
            a['a_id'] = i.a_id
            retData.append(a)
    return HttpResponse(json.dumps(retData), content_type = 'application/json')
    



'''
学者搜索
'''
def ScholarSearch(request):
    retData = []
    search = request.GET['search']
    scholars = scholar_tab.objects.all()
    for i in scholars:
        if search in i.name:
            a = {}
            a['name'] = i.name
            a['p_title'] = i.p_title
            sd1 = scholar_department_tab.objects.filter(scholar_id = i.scholar_id)
            if len(sd1) > 0:
                sd1 = sd1[0]
                d1 = department_tab.objects.get(d_id = sd1.d_id)
                a['department'] = d1.name
            else:
                a['department'] = '暂无'
            a['scholar_id'] = i.scholar_id
            a['get_id'] = i.get_id
            retData.append(a)
    return HttpResponse(json.dumps(retData), content_type = 'application/json')
    
        
        
'''
用户举报
''' 
def WxReport(request):
    retData = {}
    user_id = request.GET['user_id']
    typein = request.GET['type']
    id_in = request.GET['id']
    title = request.GET['title']
    brief = request.GET['brief']
    if typein == "1":
        report_tab(typeR = 0, id = user_id, a_id = id_in, information = brief)
    else:
        report_tab(typeR = 1, id = user_id, a_id = id_in, information = brief)
    retData['code'] = 0
    return HttpResponse(json.dumps(retData), content_type = 'application/json')
    
        
