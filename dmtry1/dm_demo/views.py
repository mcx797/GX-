from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render


from dm_demo.models import admin_tab, achievement_tab, achievement_brief_tab, keyword_tab
from dm_demo.models import achieve_keyword_tab, achievement_authen_tab, sch_ach_authen_tab
from dm_demo.models import scholar_achievement_tab, department_tab, scholar_tab, scholar_change_tab
from dm_demo.models import information_tab, person_inform_tab, scholar_brief_intro_tab
from dm_demo.models import scholar_department_tab, report_tab, user_tab, student_tab
from dm_demo.models import student_achievement_tab, student_department_tab, stuachievement_tab
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

from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password, check_password


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
def page_not_found(request, exception):
    return render(request, 'Dashio/404.html',status=404)


def page_not_found1(request):
    return render(request, 'Dashio/500.html',status=500)

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
release_year = ''
release_year2 = ''
author_name = ''
keyword = ''
ach_name = ''
release_year_type = ''
type1 = ''
type2 = ''
type3 = ''
type4 = ''
type5 = ''
search1 = ''
search2 = ''
search3 = ''
search4 = ''
search5 = ''
search1_text = ''
search2_text = ''
search3_text = ''
search4_text = ''
search5_text = ''
ach_keyword_type = ''
author_name_type = ''
ach_name_type = ''
search_err_msg = ''
scholar_err_msg = ''
ann_err_msg = ''
newach_err_msg = ''
student_err_msg = ''
check_scholar = ''
check_student = ''


def hello(request):
    return HttpResponse('Hello World')


def msg(request, name, age):
    return HttpResponse('My name is ' + name + ', i am ' + age + 'years old cl is my dad')


# @login_required
def homepage(request):
    # login_check(request)
    # if request.session.get('verfiy', None) != 'is_login':
    #     return redirect('/login')
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
    user_counter[month-1][1] = len(scholar_tab.objects.filter(flag=1))
    user_counter[month-1][2] = student_tab.objects.count()
    ach_counter[month-1] = achievement_tab.objects.count()
    user_sub[month-1][0] = user_counter[month-1][0] - last0
    user_sub[month-1][1] = user_counter[month-1][1] - last1
    user_sub[month-1][2] = user_counter[month-1][2] - last2
    ach_all[3] = max(ach_counter[0], ach_counter[1], ach_counter[2])
    ach_all[4] = max(ach_counter[3], ach_counter[4], ach_counter[5])
    ach_all[5] = max(ach_counter[6], ach_counter[7], ach_counter[8])
    ach_all[6] = max(ach_counter[9], ach_counter[10], ach_counter[11])
    ach_sub[month-1] = ach_counter[month-1] - last_ach
    # 用户认证消息
    user_authen = authen_tab.objects.filter()
    user_authen_count = authen_tab.objects.count()
    # 新成果认证消息
    ach_authen = achievement_authen_tab.objects.filter()
    ach_authen_count = achievement_authen_tab.objects.count()
    # 举报信息
    reports = report_tab.objects.filter(flag=0)
    report_count = len(reports)
    dict = {'admin_id': admin_id, 'user_counter': user_counter, 'user_sub': user_sub,
            'year': year, 'month': month, 'ach_sub': ach_sub, 'ach_all': ach_all,
            'user_authen': user_authen, 'user_authen_count': user_authen_count,
            'ach_authen': ach_authen, 'ach_authen_count': ach_authen_count,
            'reports': reports, 'report_count': report_count}
    path = []
    request.session['path'] = ""
    print(request.session['path'])
    return render(request, 'Dashio/index.html', {'dict': dict})


def login_dm(request):
    global admin_id
    if request.method == "GET":  # 如果提交方式为GET即显示login.html
        # request.sessions['verfiy'] = ''
        admin_id = ''
        return render(request, "Dashio/login.html")
    else:  # 如果提交方式为POST
        id = request.POST.get('adminid')
        pwd = request.POST.get('password') #make_password(,None,'pbkdf2_sha1'), password=pwd
        # admin_tab.objects.create_user(id=id,password=pwd,username=id,errors=0)
        if admin_tab.objects.filter(id=id).exists():
            password = admin_tab.objects.get(id=id).password
            print(password)
            print(pwd)
            if check_password(pwd,password):
                admin_id = id
                # response = HttpResponseRedirect('/server/')
                # response.set_cookie('username', admin_id, 3600)
                session = request.session
                session['verfiy'] = 'is_login'
                session['admin_id'] = admin_id
                session['path'] = ""
		# session['search_err_msg']= ""
                user_true = authenticate(id=id,password=pwd)
                print(user_true)
                login(request,user_true)
                # print(session['verfiy'])
                # print(session['path'])
                return redirect('/server/')
            else:
                return render(request, 'Dashio/login.html', {'script': "alert", 'wrong': '密码错误'})
        else:
            if id == '':
                return render(request, 'Dashio/login.html', {'script': "alert", 'wrong': '请填写登陆信息'})
            else:
                return render(request, 'Dashio/login.html', {'script': "alert", 'wrong': '该账号不存在'})


def logout_view(request):
    # request.session.flush()
    logout(request)
    return redirect('/login')



# def login(request):
#     global admin_id
#     if request.method == "GET":  # 如果提交方式为GET即显示login.html
#         # request.sessions['verfiy'] = ''
#         admin_id = ''
#         return render(request, "Dashio/login.html")
#     else:  # 如果提交方式为POST
#         id = request.POST.get('adminid')
#         pwd = request.POST.get('password')
#         if admin_tab.objects.filter(id=id).exists():
#             if admin_tab.objects.filter(id=id)[0].password == pwd:
#                 admin_id = id
#                 # response = HttpResponseRedirect('/server/')
#                 # response.set_cookie('username', admin_id, 3600)
#                 session = request.session
#                 print(session['verfiy'])
#                 session['verfiy'] = 'is_login'
#                 session['admin_id'] = admin_id
#                 print(session['verfiy'])
#                 return redirect('/server/')
#             else:
#                 return render(request, 'Dashio/login.html', {'script': "alert", 'wrong': '密码错误'})
#         else:
#             if id == '':
#                 return render(request, 'Dashio/login.html', {'script': "alert", 'wrong': '请填写登陆信息'})
#             else:
#                 return render(request, 'Dashio/login.html', {'script': "alert", 'wrong': '该账号不存在'})
#
#
# def logout(request):
#     # request.sessions['verfiy'] = ''
#     # request.sessions.flush()
#     return redirect('/login')


# 新加的内容
# 查看学者成果——对成果进行操作
# @login_required
def check_ach(request):
    # login_check(request)
    search = ''
    if request.method == "GET":  # 如果提交方式为GET即显示check_achiev.html
        size = ""
        all_ach = achievement_tab.objects.filter()
        dict = {'all_achievements': all_ach, 'admin_id': admin_id, 'size': size, 'search':search}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, 'Dashio/check_achiev.html', {'all_ach_dict': dict})
    else:  # 如果提交方式为POST
        all_ach = achievement_tab.objects.filter()
        return


# 删除某项学者成果
def delete_one_ach(request, id):
    achievement_tab.objects.filter(a_id=id).delete()
    # 同时删除brief
    achievement_brief_tab.objects.filter(a_id=id, flag=0).delete()
    return redirect('/checkachievement')


# 查看某项学者成果的详细信息
def check_one_ach(request, id):
    # login_check(request)
    err_msg = ''
    if request.method == "GET":
        ach_info = achievement_tab.objects.filter(a_id=id)[0]
        brief = ''
        if not achievement_brief_tab.objects.filter(a_id=id, flag=0).exists():
            brief = '暂无'
        else:
            briefs = achievement_brief_tab.objects.filter(a_id=id, flag=0).order_by('number')
            for b in briefs:
                brief = brief + b.brief
        # brief = ''
        # # 将brief组合起来
        # if ach_info.brief == 0:
        #     brief = '暂无'
        # else:
        #     # 去brief表中找
        #     brief1 = achievement_brief_tab.objects.filter(achbfId=ach_info.brief)[0]
        #     brief = brief1.brief
        #     while brief1.next_id != 0:
        #         last_next_id = brief1.next_id
        #         brief1 = achievement_brief_tab.objects.filter(achbfId=last_next_id)[0]
        #         brief = brief + brief1.brief
        dict = {'admin_id': admin_id, 'ach_info': ach_info, 'err_msg': err_msg, 'brief': brief}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, "Dashio/check_achiev_detail.html", {'check_ach': dict})
    else:
        return


# 查看学生的成果
def check_student_ach(request):
    search = ''
    if request.method == "GET":  # 如果提交方式为GET即显示check_achiev.html
        size = ""
        all_ach = stuachievement_tab.objects.filter()
        dict = {'all_achievements': all_ach, 'admin_id': admin_id, 'size': size, 'search':search}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, 'Dashio/check_stu_achiev.html', {'all_ach_dict': dict})
    else:  # 如果提交方式为POST
        all_ach = achievement_tab.objects.filter()
        return


# 删除某项成果
def delete_one_student_ach(request, id):
    stuachievement_tab.objects.filter(a_id=id).delete()
    # 同时删除brief
    achievement_brief_tab.objects.filter(a_id=id, flag=1).delete()
    return redirect('/checkstuachievement')


# 查看某项成果的详细信息
def check_one_student_ach(request, id):
    err_msg = ''
    if request.method == "GET":
        ach_info = stuachievement_tab.objects.filter(a_id=id)[0]
        brief = ''
        if not achievement_brief_tab.objects.filter(a_id=id, flag=1).exists():
            brief = '暂无'
        else:
            briefs = achievement_brief_tab.objects.filter(a_id=id, flag=1).order_by('number')
            for b in briefs:
                brief = brief + b.brief
        dict = {'admin_id': admin_id, 'ach_info': ach_info, 'err_msg': err_msg, 'brief': brief}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, "Dashio/check_stu_achiev_detail.html", {'check_ach': dict})
    else:
        return


# 修改某项成果
def edit_one_ach(request, id):
    # login_check(request)
    global ach_info
    err_msg = ""
    a_id = id
    if request.method == "GET":
        ach_info = achievement_tab.objects.filter(a_id=id)[0]
        brief = ''
        if not achievement_brief_tab.objects.filter(a_id=id, flag=0).exists():
            brief = '暂无'
        else:
            briefs = achievement_brief_tab.objects.filter(a_id=id, flag=0).order_by('number')
            for b in briefs:
                brief = brief + b.brief
        dict = {'admin_id': admin_id, 'ach_info': ach_info, 'err_msg': err_msg, 'brief': brief}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, "Dashio/edit_achievement.html", {'edit_ach': dict})
    else:  # 如果提交方式为POST
        name = request.POST.get('name')
        year = request.POST.get('year')
        author_name = request.POST.get('authors')
        citation = request.POST.get('cite')
        j_a_name = request.POST.get('journal')
        file = request.POST.get('file')
        link = request.POST.get('link')
        keyword = request.POST.get('keyword')
        kind = request.POST.get('kind')   # kind如何存？
        num_view = request.POST.get('num_view')
        brief_change = request.POST.get('brief')
        if not year.isdigit():
            err_msg = "请填写正确发表年份"
        elif not citation.isdigit():
            err_msg = "请填写正确引用数"
        elif not num_view.isdigit():
            err_msg = "请填写正确浏览次数"
        elif len(name) > 150:
            err_msg = "成果名过长，请再次检查"
        elif len(author_name) > 150:
            err_msg = "作者名过长，请再次检查"
        elif len(j_a_name) > 150:
            err_msg = "成果出处名称过长，请再次检查"
        elif len(kind) > 10:
            err_msg = "成果类型名称过长，请再次检查"
        elif achievement_tab.objects.filter(name=name).exists():
            err_msg = "该名称成果已存在，请再次检查"
        elif len(link) > 150:
            err_msg = "成果链接过长，请再次检查"
        else:
            # 这里file需要换成file的存储位置！！！！！！！！
            # file_site = "no"
            # 加入成果表
            achievement_tab.objects.filter(a_id=a_id).update(name=name, year=year, author_name=author_name,
                                                             citation=citation,
                                                             j_a_name=j_a_name, file=file, link=link, keyword=keyword,
                                                             kind=kind, num_view=num_view)
            ach_info = achievement_tab.objects.filter(a_id=id)[0]
            brief = ''
            if not achievement_brief_tab.objects.filter(a_id=id, flag=0).exists():
                brief = '暂无'
            else:
                briefs = achievement_brief_tab.objects.filter(a_id=id, flag=0).order_by('number')
                for b in briefs:
                    brief = brief + b.brief
            # 如果brief发生改变
            if brief != brief_change:
                # 将之前brief在brief表中的信息删除
                achievement_brief_tab.objects.filter(a_id=id, flag=0).delete()
                # 再将brief加入brief表中
                brief_left = brief_change
                count = 0  # brief的数目
                save_brief = 0  # 存入成果表的brief项
                this_brief = 0
                last_id = 0
                while len(brief_left) > 100:
                    if count > 0:
                        last_id = this_brief.achbfId
                    count = count + 1
                    brief_left = brief_left[100:]
                    this_brief = achievement_brief_tab.objects.create(a_id=a_id, brief=brief_left[:100],
                                                                      number=count)
                    # if count == 1:
                    #     save_brief = this_brief.achbfId
                    if count > 1:
                        achievement_brief_tab.objects.filter(achbfId=last_id).update(next_id=this_brief.achbfId)
                # 剩下的小于100字符的摘要
                if len(brief_left) > 0:
                    if count > 0:
                        last_id = this_brief.achbfId
                    count = count + 1
                    this_brief = achievement_brief_tab.objects.create(a_id=a_id, brief=brief_left, number=count)
                    # if count == 1:
                    #     save_brief = this_brief.achbfId
                    if count > 1:
                        achievement_brief_tab.objects.filter(achbfId=last_id).update(next_id=this_brief.achbfId)
                # # 更新新成果中的brief
                # achievement_tab.objects.filter(a_id=a_id).update(brief=save_brief)
            err_msg = "修改成果项成功"
            ach_info = achievement_tab.objects.filter(a_id=a_id)[0]
        dict = {'admin_id': admin_id, 'ach_info': ach_info, 'err_msg': err_msg}
        return render(request, 'Dashio/edit_achievement.html', {'edit_ach': dict})


# 添加成果
def add_achievement(request):
    # login_check(request)
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
        keyword = request.POST.get('keyword') # keyword如何存
        kind = request.POST.get('kind')  # kind如何存？
        num_view = request.POST.get('num_view')
        brief = request.POST.get('brief')
        if not year.isdigit():
            err_msg = "请填写正确发表年份"
        elif not citation.isdigit():
            err_msg = "请填写正确引用数"
        elif not num_view.isdigit():
            err_msg = "请填写正确浏览次数"
        elif len(name) > 150:
            err_msg = "成果名过长，请再次检查"
        elif len(author_name) > 150:
            err_msg = "作者名过长，请再次检查"
        elif len(j_a_name) > 150:
            err_msg = "成果出处名称过长，请再次检查"
        elif len(kind) > 10:
            err_msg = "成果类型名称过长，请再次检查"
        elif len(link) > 150:
            err_msg = "成果链接过长，请再次检查"
        else:
            if achievement_tab.objects.filter(name=name).exists():
                # 这里大概还需要检查作者？？？？
                err_msg = "该成果已存在"
            else:
                # 这里file需要换成file的存储位置！！！！！！！！
                file_site = "no"
                newach = achievement_tab.objects.create(name=name, year=year, author_name=author_name, citation=citation,
                                                        j_a_name=j_a_name, file=file_site, link=link, kind=kind,
                                                        num_view=num_view, keyword=keyword)
                brief_left = brief
                count = 0  # brief的数目
                this_brief = 0
                last_id = 0
                while len(brief_left) > 100:
                    if count > 0:
                        last_id = this_brief.achbfId
                    count = count + 1
                    brief = brief_left[:100]
                    brief_left = brief_left[100:]
                    this_brief = achievement_brief_tab.objects.create(a_id=newach.a_id, brief=brief_left[:100],
                                                                      number=count)
                    if count > 1:
                        achievement_brief_tab.objects.filter(achbfId=last_id).update(next_id=this_brief.achbfId)
                # 剩下的小于100字符的摘要
                if len(brief_left) > 0:
                    if count > 0:
                        last_id = this_brief.achbfId
                    count = count + 1
                    this_brief = achievement_brief_tab.objects.create(a_id=newach.a_id, brief=brief_left, number=count)
                    if count > 1:
                        achievement_brief_tab.objects.filter(achbfId=last_id).update(next_id=this_brief.achbfId)
                err_msg = "添加成果项成功"
            dict = {'admin_id': admin_id, 'err_msg': err_msg}
            return render(request, 'Dashio/add_achievement.html', {'add_ach': dict})


# 显示所有新的成果认证申请信息
def check_newach_authen(request):
    global newach_err_msg
    login_check(request)
    if request.method == "GET":  # 如果提交方式为GET即显示check_achiev.html
        all_authen1 = achievement_authen_tab.objects.filter()
        all_authen2 = sch_ach_authen_tab.objects.filter()
        newauth = []
        for auth in all_authen2:
            newauth.append(NewSchAchAuthen(auth))
        err_msg = newach_err_msg
        newach_err_msg = ''
        dict = {'all_authen1': all_authen1, 'all_authen2': newauth, 'admin_id': admin_id, 'err_msg': err_msg}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, 'Dashio/check_achiev_authen.html', {'ach_authen': dict})
    else:  # 如果提交方式为POST
        all_authen = achievement_tab.objects.filter()
        return


# 通过一条新成果认证
def check_one_newach_authen(request, id):
    # login_check(request)
    authen_id = id
    err_msg = ''
    auth_info = achievement_authen_tab.objects.filter(id=id)[0]
    scholar_id = auth_info.scholar_id
    scholar_name = scholar_tab.objects.filter(scholar_id=scholar_id)[0].name
    user_id = scholar_tab.objects.filter(scholar_id=scholar_id)[0].user_id
    if request.method == "GET":
        dict = {'admin_id': admin_id, 'auth_info': auth_info, 'scholar_name': scholar_name, 'err_msg': err_msg}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, "Dashio/check_newachiev_details.html", {'check_newauth': dict})
    else:
        # 驳回
        reject_info = request.POST.get('reject_info')
        if len(reject_info) > 400:
            err_msg = "反馈信息不能多于400字符"
            dict = {'admin_id': admin_id, 'auth_info': auth_info, 'scholar_name': scholar_name, 'err_msg': err_msg}
            return render(request, "Dashio/check_newachiev_details.html", {'check_newauth': dict})
        elif user_id is -1:
            err_msg = "该学者未被认领"
            dict = {'admin_id': admin_id, 'auth_info': auth_info, 'scholar_name': scholar_name, 'err_msg': err_msg}
            return render(request, "Dashio/check_newachiev_details.html", {'check_newauth': dict})
        person_inform_tab.objects.create(user_id=user_id, title="新成果申请未通过", information=reject_info)
        return redirect('/delete_newauthen/'+id)


def pass_one_newach_authen(request, id):
    global newach_err_msg
    newach_auth = achievement_authen_tab.objects.filter(id=id)[0]
    # 通过认证，加入成果表
    newach = achievement_tab.objects.create(name=newach_auth.a_name, year=newach_auth.year,
                                            author_name=newach_auth.author_name, citation=newach_auth.citation,
                                            j_a_name=newach_auth.j_a_name, file=newach_auth.file,
                                            link=newach_auth.link, kind=newach_auth.kind,
                                            num_view=newach_auth.num_view, keyword=newach_auth.keyword)
    # 考虑brief？？？
    # 先将brief加入brief表中
    brief_left = newach_auth.brief
    count = 0  # brief的数目
    this_brief = 0
    last_id = 0
    while len(brief_left) > 100:
        if count > 0:
            last_id = this_brief.achbfId
        count = count + 1
        brief = brief_left[:100]
        brief_left = brief_left[100:]
        this_brief = achievement_brief_tab.objects.create(a_id=newach.a_id, brief=brief_left[:100],
                                                          number=count)
        if count > 1:
            achievement_brief_tab.objects.filter(achbfId=last_id).update(next_id=this_brief.achbfId)
    # 剩下的小于100字符的摘要
    if len(brief_left) > 0:
        if count > 0:
            last_id = this_brief.achbfId
        count = count + 1
        this_brief = achievement_brief_tab.objects.create(a_id=newach.a_id, brief=brief_left, number=count)
        if count > 1:
            achievement_brief_tab.objects.filter(achbfId=last_id).update(next_id=this_brief.achbfId)
    # 将其中all_id均存入new_relation_tab中
    all_id = newach_auth.all_id
    if len(all_id) > 0:  # 说明有关联学者
        id_list = all_id.split(",")
        for id in id_list:
            new_relation_tab.objects.create(auth_id=id, ach_id=newach.a_id)
            scholar_tab.objects.filter(scholar_id=id).update(Has_Info=1)
    # 删除原认证信息，加入学者成果关联表
    achievement_authen_tab.objects.filter(id=newach_auth.id).delete()
    scholar_achievement_tab.objects.create(scholar_id=newach_auth.scholar_id, a_id=newach.a_id)
    # 将相同成果名的成果申请加入到关联申请表中
    auths = achievement_authen_tab.objects.filter(a_name=newach_auth.a_name)
    for auth in auths:
        sch_ach_authen_tab.objects.create(scholar_id=auth.scholar_id, a_id=newach.a_id)
        achievement_authen_tab.objects.filter(id=auth.id).delete()
    newach_err_msg = "成果认证成功"
    return redirect('/check_newach_authen')


def delete_one_newauthen(request, id):
    achievement_authen_tab.objects.filter(id=id).delete()
    return redirect('/check_newach_authen')


class NewSchAchAuthen():
    def __init__(self, auth):
        self.authen = auth
        self.a_name = achievement_tab.objects.filter(a_id=auth.a_id)[0].name
        self.scholar_name = scholar_tab.objects.filter(scholar_id=auth.scholar_id)[0].name


def check_one_sch_ach_authen(request, id):
    # login_check(request)
    global sch_ach_auth
    auth_info = sch_ach_authen_tab.objects.filter(id=id)[0]
    sch_ach_auth = auth_info
    scholar_id = auth_info.scholar_id
    a_id = auth_info.a_id
    scholar_name = scholar_tab.objects.filter(scholar_id=scholar_id)[0].name
    ach_info = achievement_tab.objects.filter(a_id=a_id)[0]
    a_name = ach_info.name
    year = ach_info.year
    author_name = ach_info.author_name
    citation = ach_info.citation
    j_a_name = ach_info.j_a_name
    file = ach_info.file
    link = ach_info.link
    kind = ach_info.kind
    num_view = ach_info.num_view
    keyword = ach_info.keyword
    user_id = scholar_tab.objects.filter(scholar_id=scholar_id)[0].user_id
    if request.method == "GET":
        err_msg = ""
        dict = {'admin_id': admin_id, 'auth_info': auth_info, 'scholar_name': scholar_name, 'a_name': a_name,
                'year': year, 'author_name': author_name, 'citation': citation, 'j_a_name':j_a_name,
                'file':file, 'link':link, 'keyword':keyword, 'kind':kind, 'num_view': num_view, 'err_msg': err_msg}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, "Dashio/check_schach_authen_details.html", {'check_schach_auth': dict})
    else:
        # 驳回
        reject_info = request.POST.get('reject_info')
        if len(reject_info) > 400:
            err_msg = "反馈信息不能多于400字符"
            dict = {'admin_id': admin_id, 'auth_info': auth_info, 'scholar_name': scholar_name, 'a_name': a_name,
                    'year': year, 'author_name': author_name, 'citation': citation, 'j_a_name': j_a_name,
                    'file': file, 'link': link, 'keyword': keyword, 'kind': kind, 'num_view': num_view,
                    'err_msg': err_msg}
            return render(request, "Dashio/check_schach_authen_details.html", {'check_schach_auth': dict})
        elif user_id is -1:
            err_msg = "该学者未被认领"
            dict = {'admin_id': admin_id, 'auth_info': auth_info, 'scholar_name': scholar_name, 'err_msg': err_msg}
            return render(request, "Dashio/check_newachiev_details.html", {'check_newauth': dict})
        person_inform_tab.objects.create(user_id=user_id, title="新成果申请未通过", information=reject_info)
        return redirect('/delete_schach_authen/'+id)


def pass_one_sch_ach_authen(request, id):
    global newach_err_msg
    sch_ach_auth = sch_ach_authen_tab.objects.filter(id=id)[0]
    scholar_achievement_tab.objects.create(scholar_id=sch_ach_auth.scholar_id, a_id=sch_ach_auth.a_id)
    sch_ach_authen_tab.objects.filter(id=id).delete()
    newach_err_msg = "成果关联认证成功"
    return redirect('/check_newach_authen')


def delete_one_schach_authen(request, id):
    sch_ach_authen_tab.objects.filter(id=id).delete()
    return redirect('/check_newach_authen')


# 查看院系信息——对院系信息进行操作
def check_department(request):
    if request.method == "GET":  # 如果提交方式为GET即显示login.html
        all_dep = department_tab.objects.filter()
        dict = {'all_departments': all_dep, 'admin_id': admin_id}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, 'Dashio/check_department.html', {'all_dep_dict': dict})
    else:  # 如果提交方式为POST
        return


# 删除某个院系
def delete_one_dep(request, id):
    department_tab.objects.filter(d_id=id).delete()
    scholar_department_tab.objects.filter(d_id=id).delete()
    student_department_tab.objects.filter(d_id=id).delete()
    return redirect('/checkdepartment')


# 查看某个院系的详细信息
def check_one_dep(request, id):
    err_msg = ''
    if request.method == "GET":
        dep_info = department_tab.objects.filter(d_id=id)[0]
        dict = {'admin_id': admin_id, 'dep_info': dep_info, 'err_msg': err_msg}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, "Dashio/check_dep_brief.html", {'check_dep': dict})
    else:
        return


# 修改某个院系
def edit_one_dep(request, id):
    global dep_info
    err_msg = ""
    d_id=id
    if request.method == "GET":
        dep_info = department_tab.objects.filter(d_id=id)[0]
        dict = {'admin_id': admin_id, 'dep_info': dep_info, 'err_msg': err_msg}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, "Dashio/edit_department.html", {'edit_dep': dict})
    else:  # 如果提交方式为POST
        number = request.POST.get('number')
        name = request.POST.get('d_name')
        brief = request.POST.get('brief_info')
        if not number.isdigit():
            err_msg = "院系编号需要由数字组成"
        elif len(number) != 2:
            err_msg = "院系编号需有2位数字"
        elif len(brief) > 600:
            err_msg = "院系简介需控制在600字符内"
        else:
            department_tab.objects.filter(d_id=id).update(number=number, name=name, brief=brief)
            err_msg = "院系信息修改成功"
            dep_info = department_tab.objects.filter(d_id=d_id)[0]
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
        elif len(brief) > 600:
            err_msg = "院系简介需控制在600字符内"
            dict = {'admin_id': admin_id, 'err_msg': err_msg}
            return render(request, 'Dashio/add_department.html', {'add_dep': dict})
        else:
            if department_tab.objects.filter(number=number).exists():
                err_msg = "该院系编号已存在"
                dict = {'admin_id': admin_id, 'err_msg': err_msg}
                return render(request, 'Dashio/add_department.html', {'add_dep': dict})
            elif department_tab.objects.filter(name=name).exists():
                err_msg = "该院系名称已存在"
                dict = {'admin_id': admin_id, 'err_msg': err_msg}
                return render(request, 'Dashio/add_department.html', {'add_dep': dict})
            else:
                department_tab.objects.create(number=number, name=name, brief=brief)
                err_msg = "添加院系成功"
                dict = {'admin_id': admin_id, 'err_msg': err_msg}
                return render(request, 'Dashio/add_department.html', {'add_dep': dict})


# 查看举报信息
def check_report(request):
    if request.method == "GET":
        all_report = report_tab.objects.filter(flag=0)
        dict = {'all_reports': all_report, 'admin_id': admin_id}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, 'Dashio/check_report.html', {'all_rep_dict': dict})
    else:  # 如果提交方式为POST
        return


# 删除某个举报信息
def delete_one_report(request, id):
    report_tab.objects.filter(r_id=id).delete()
    return redirect('/checkreport')


# 通过某个举报信息
def check_one_report(request, id):
    if request.method == "GET":
        report_tab.objects.filter(r_id=id).update(flag=1)
        return redirect('/checkreport')
    else:
        return


# 用户相关
# 查看学者用户
def scholar(request):
    global scholar_err_msg
    err_msg = scholar_err_msg
    scholar_err_msg = ''
    size = ''
    dep = ''
    # all_scholar = scholar_tab.objects.filter(flag=1)
    all_scholar = scholar_tab.objects.filter()
    dict = {'admin_id': admin_id, 'all_sch': all_scholar, 'size': size, 'dep': dep, 'err_msg': err_msg}
    if "img" not in request.path_info:
        path0 = request.session['path']
        request.session['path'] = path0 + "@" + request.path_info
        print(request.session['path'])
    return render(request, 'Dashio/check_scholar.html', {'all_scholar': dict})


# 删除学者用户
def del_scholar(request, id):
    global scholar_err_msg
    if id == -1:
        scholar_err_msg = '该学者信息尚未被认领，无法删除'
    else:
        scholar_id = scholar_tab.objects.filter(user_id=id)[0].scholar_id
        scholar_tab.objects.filter(user_id=id).delete()
        user_tab.objects.filter(user_id=id).delete()
        achievement_authen_tab.objects.filter(scholar_id=scholar_id).delete()
        scholar_achievement_tab.objects.filter(scholar_id=scholar_id).delete()    # 这里成果是否删除？
        scholar_change_tab.objects.filter(scholar_id=scholar_id).delete()
        person_inform_tab.objects.filter(user_id=id).delete()
        scholar_brief_intro_tab.objects.filter(scholar_id=scholar_id).delete()
        scholar_department_tab.objects.filter(scholar_id=scholar_id).delete()
        collect_scholar_tab.objects.filter(scholar_id=scholar_id).delete()
        scholar_direction_tab.objects.filter(scholar_id=scholar_id).delete()
    return redirect('/scholar')


# 查看学者信息详情   需加
def check_one_scholar(request, id):
    global scholar_err_msg
    err_msg = ''
    if request.method == "GET":
        # if id == -1:
        #     scholar_err_msg = '该学者信息尚未被认领，无法查看详情'
        #     return redirect('/scholar')
        # else:
        if scholar_department_tab.objects.filter(scholar_id=id).exists():
            d_id = scholar_department_tab.objects.filter(scholar_id=id)[0].d_id
            department = department_tab.objects.filter(d_id=d_id)[0].name
        else:
            department = -1
        # 找到所有有关brief
        brief = ''
        if not scholar_brief_intro_tab.objects.filter(scholar_id=id).exists():
            brief = '暂无简介'
        else:
            briefs = scholar_brief_intro_tab.objects.filter(scholar_id=id).order_by('number')
            for b in briefs:
                brief = brief + b.brief
        sch_info = scholar_tab.objects.filter(scholar_id=id)[0]
        dict = {'admin_id': admin_id, 'sch_info': sch_info, 'err_msg': err_msg, 'department': department, 'brief': brief}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, "Dashio/check_scholar_info.html", {'check_sch': dict})
    else:
        return


# 修改学者信息详情   需加
def edit_one_scholar(request, id):
    global sch_info
    err_msg = ""
    user_id=id
    if request.method == "GET":
        sch_info = scholar_tab.objects.filter(user_id=id)[0]
        dict = {'admin_id': admin_id, 'sch_info': sch_info, 'err_msg': err_msg}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, "Dashio/edit_scholar.html", {'edit_sch': dict})
    else:  # 如果提交方式为POST
        name = request.POST.get('name')
        school = request.POST.get('school')
        email = request.POST.get('email')
        p_title = request.POST.get('p_title')
        if len(email) <= 7 or re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is None:
            err_msg = "邮箱格式错误"
        elif len(school) > 30:
            err_msg = "学校名称过长，不应超过30个字符"
        else:
            scholar_tab.objects.filter(user_id = user_id).update(name=name, school=school, email=email, p_title=p_title)
            err_msg = "学者信息修改成功"
            sch_info = scholar_tab.objects.filter(user_id=user_id)[0]
        dict = {'admin_id': admin_id, 'sch_info': sch_info, 'err_msg': err_msg}
        return render(request, "Dashio/edit_scholar.html", {'edit_sch': dict})


# 查看学生用户
def student(request):
    all_student = student_tab.objects.all()
    size = ''
    dep = ''
    dict = {'admin_id': admin_id, 'all_student': all_student, 'size': size, 'dep': dep}
    if "img" not in request.path_info:
        path0 = request.session['path']
        request.session['path'] = path0 + "@" + request.path_info
        print(request.session['path'])
    return render(request, 'Dashio/student.html', {'all_student_dict': dict})


# 删除学生用户
def del_student(request,id):
    student_id = student_tab.objects.filter(user_id=id).student_id
    student_tab.objects.filter(user_id=id).delete()
    user_tab.objects.filter(user_id=id).delete()
    if student_achievement_tab.objects.filter(student_id=student_id).exists():
        for i in student_achievement_tab.objects.filter(student_id=student_id):
            a_id = i.a_id
            if len(student_achievement_tab.objects.filter(a_id=a_id)) == 1:
                stuachievement_tab.objects.filter(a_id=a_id).delete()
    student_achievement_tab.objects.filter(student_id=student_id).delete()  # 是否删学生成果？
    student_department_tab.objects.filter(student_id=student_id).delete()
    return redirect('/student')


# 查看学生信息详情   需加
def check_one_student(request, id):
    global student_err_msg
    err_msg = student_err_msg
    student_err_msg = ''
    if request.method == "GET":
        if student_department_tab.objects.filter(student_id=id).exists():
            d_id = student_department_tab.objects.filter(student_id=id)[0].d_id
            department = department_tab.objects.filter(d_id=d_id)[0].name
        else:
            department = -1
        stu_info = student_tab.objects.filter(user_id=id)[0]
        dict = {'admin_id': admin_id, 'stu_info': stu_info, 'err_msg': err_msg, 'department': department}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, "Dashio/check_student_info.html", {'check_student': dict})
    else:
        return


# 修改学生信息详情   需加
def edit_one_student(request, id):
    global stu_info
    err_msg = ""
    user_id=id
    if request.method == "GET":
        stu_info = student_tab.objects.filter(user_id=id)[0]
        dict = {'admin_id': admin_id, 'stu_info': stu_info, 'err_msg': err_msg}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
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
        if user_authen_tab.objects.filter(authen_id=authen.authen_id).exists():
            new_authen.append(NewAuthen(authen))
        #  new_authen.append(NewAuthen(authen))
    dict = {'admin_id': admin_id, 'all_authen': new_authen}
    if "img" not in request.path_info:
        path0 = request.session['path']
        request.session['path'] = path0 + "@" + request.path_info
        print(request.session['path'])
    return render(request, 'Dashio/authen_user.html', {'all_authen_dict': dict})


# 展示身份申请详情
def authen_user_detail(request,id):
    global sch_info
    err_msg = ""
    sch_info = authen_tab.objects.filter(authen_id=id)[0]
    user = user_authen_tab.objects.filter(authen_id =id)[0]
    if request.method == "GET":
        if department_tab.objects.filter(d_id=sch_info.department).exists():
            department = department_tab.objects.filter(d_id=sch_info.department)[0].name
        else:
            department = "暂无信息"
        # department = department_tab.objects.filter(d_id=sch_info.department)[0].name
        dict = {'auth_info': sch_info, 'err_msg': err_msg, 'department': department}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, "Dashio/check_authen_user_detail.html", {'auth_user': dict})
    else:  # 如果提交方式为POST
        if department_tab.objects.filter(d_id=sch_info.department).exists():
            department = department_tab.objects.filter(d_id=sch_info.department)[0].name
        else:
            department = "暂无信息"
        information = request.POST.get('reject_info')
        if len(information) > 400:
            err_msg = "反馈信息不能多于400字符"
            dict = {'auth_info': sch_info, 'err_msg': err_msg, 'department': department}
            return render(request, "Dashio/check_authen_user_detail.html", {'auth_user': dict})
        t1 = sch_info.identity
        tit = ""
        if t1 is 1:
            tit = "您申请成为：学者 的身份认证失败。"
        elif t1 is 2:
            tit = "您申请成为：学生 的身份认证失败。"
        person_inform_tab.objects.create(user_id=user.user_id, title=tit, information=information)
        return redirect('/del_authen/' + id)


# 展示学者修改身份信息
def check_auth_exist_user(request):  #只显示flag= 0的
    # 查看用户身份申请
    all_new_authen = scholar_change_tab.objects.all()
    dict = {'admin_id': admin_id, 'all_authen': all_new_authen}
    if "img" not in request.path_info:
        path0 = request.session['path']
        request.session['path'] = path0 + "@" + request.path_info
        print(request.session['path'])
    return render(request, 'Dashio/authen_exist_user.html', {'all_authen_dict': dict})


# 通过已有学者修改身份信息
def pass_exist_scholar_authen(request, authen_id):  # 通过后向学者表/用户表中添加对应表项
    authen_info = scholar_change_tab.objects.get(ScholarCid=authen_id)
    scholar_tab.objects.filter(user_id=authen_info.user_id).update(school=authen_info.school, name=authen_info.name, email=authen_info.email, p_title=authen_info.p_title)
    person_inform_tab.objects.create(user_id=authen_info.user_id,title="学者身份信息修改通过",information="您提交的学者身份信息修改已通过")
    # return redirect('/del_exist_scholar_authen/'+authen_id)
    scholar_change_tab.objects.filter(ScholarCid=authen_id).update(flag = 1)
    return redirect('/check_auth_exist_user')


# 查看认证信息详情
def exist_user_auth_detail(request,authen_id):
    auth_info = scholar_change_tab.objects.get(ScholarCid=authen_id)
    if request.method=="GET":
        err_msg = ""
        auth_user = {'auth_info':auth_info, 'err_msg': err_msg}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request,'Dashio/check_exist_user_authen_detail.html',{'auth_user':auth_user})
    if request.method == "POST":
        # 驳回
        reject_info = request.POST.get('reject_info')
        if len(reject_info) > 400:
            err_msg = "反馈信息不能多于400字符"
            auth_user = {'auth_info':auth_info, 'err_msg': err_msg}
            return render(request, 'Dashio/check_exist_user_authen_detail.html', {'auth_user': auth_user})
        person_inform_tab.objects.create(user_id=auth_info.user_id, title="学者身份信息修改未通过", information=reject_info)
        scholar_change_tab.objects.filter(ScholarCid=authen_id).update(flag=1)
        return redirect('/check_auth_exist_user')


def del_exist_scholar_authen(request, authen_id):
    scholar_change_tab.objects.filter(ScholarCid=authen_id).delete()
    return redirect('/check_auth_exist_user')


class NewAuthen():
    def __init__(self, auth):
        self.authen = auth
        if auth.identity is 1:
            self.idenstr = '学者'
        elif auth.identity is 2:
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
        scholar_info = scholar_tab.objects.create(user_id=user_info.user_id, school=authen_info.school,
                                                  name=authen_info.name, email=authen_info.email, p_title="default",
                                                  flag=1, Scholar_Number=authen_info.sno)
        user_tab.objects.filter(user_id=user_info.user_id).update(authority=1)
        if department_tab.objects.filter(d_id=authen_info.department).exists():
            scholar_department_tab.objects.create(scholar_id=scholar_info.scholar_id, d_id=authen_info.department)
        person_inform_tab.objects.create(user_id=user_info.user_id, title="学者身份认证通过", information="您提交的学者身份认证已通过")
    elif authen_info.identity == 2:  # 学生
        student_info = student_tab.objects.create(user_id=user_info.user_id,school=authen_info.school,
                                                  name=authen_info.name,email=authen_info.email, sno=authen_info.sno)
        user_tab.objects.filter(user_id=user_info.user_id).update(authority=2)
        if department_tab.objects.filter(d_id=authen_info.department).exists():
            student_department_tab.objects.create(student_id=student_info.student_id, d_id=authen_info.department)
        person_inform_tab.objects.create(user_id=user_info.user_id, title="学生身份认证通过", information="您提交的学生身份认证已通过")
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
    user = user_tab.objects.filter(user_id=id)[0]
    if user.authority == 1:
        scholar_id = scholar_tab.objectsfilter(user_id=id)[0].scholar_id
        scholar_tab.objectsfilter(user_id=id).delete()
        achievement_authen_tab.objects.filter(scholar_id=scholar_id).delete()
        scholar_achievement_tab.objects.filter(scholar_id=scholar_id).delete()  # 这里成果是否删除？
        scholar_change_tab.objects.filter(scholar_id=scholar_id).delete()
        person_inform_tab.objects.filter(user_id=id).delete()
        scholar_brief_intro_tab.objects.filter(scholar_id=scholar_id).delete()
        scholar_department_tab.objects.filter(scholar_id=scholar_id).delete()
        collect_scholar_tab.objects.filter(scholar_id=scholar_id).delete()
        scholar_direction_tab.objects.filter(scholar_id=scholar_id).delete()
    elif user.authority == 2:
        student_id = student_tab.objects.filter(user_id=id).student_id
        student_tab.objects.filter(user_id=id).delete()
        user_tab.objects.filter(user_id=id).delete()
        if student_achievement_tab.objects.filter(student_id=student_id).exists():
            for i in student_achievement_tab.objects.filter(student_id=student_id):
                a_id = i.a_id
                if len(student_achievement_tab.objects.filter(a_id=a_id)) == 1:
                    stuachievement_tab.objects.filter(a_id=a_id).delete()
        student_achievement_tab.objects.filter(student_id=student_id).delete()  # 是否删学生成果？
        student_department_tab.objects.filter(student_id=student_id).delete()
    user_tab.objects.filter(user_id=id).delete()
    return redirect('/checkuser')


# ++++++++++++++++++++++++++++++++++++++
# 查看某位学者相关的成果信息
def check_scholar_achievement(request, id):
    search = ''
    scholar_id = id
    # 存在关联信息
    if scholar_achievement_tab.objects.filter(scholar_id=scholar_id).exists():
        size = scholar_tab.objects.filter(scholar_id=scholar_id)[0]
        all_ach = []
        for i in scholar_achievement_tab.objects.filter(scholar_id=scholar_id):
            all_ach.append(achievement_tab.objects.filter(a_id=i.a_id)[0])
        dict = {'all_achievements': all_ach, 'admin_id': admin_id, 'size': size, 'search': search}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, 'Dashio/check_achiev.html', {'all_ach_dict': dict})
    else:
        if scholar_department_tab.objects.filter(scholar_id=id).exists():
            d_id = scholar_department_tab.objects.filter(scholar_id=id)[0].d_id
            department = department_tab.objects.filter(d_id=d_id)[0].name
        else:
            department = -1
        err_msg = "该学者暂无可查询成果"
        sch_info = scholar_tab.objects.filter(scholar_id=scholar_id)[0]
        dict = {'admin_id': admin_id, 'sch_info': sch_info, 'err_msg': err_msg, 'department': department}
        return render(request, "Dashio/check_scholar_info.html", {'check_sch': dict})


# 查看某位学生相关的成果信息
def check_student_achievement(request, id):
    search = ''
    student_id = id
    # 存在关联信息
    if student_achievement_tab.objects.filter(student_id=student_id).exists():
        size = student_tab.objects.filter(student_id=student_id)[0]
        all_ach = []
        for i in student_achievement_tab.objects.filter(student_id=student_id):
            all_ach.append(stuachievement_tab.objects.filter(a_id=i.a_id)[0])
        dict = {'all_achievements': all_ach, 'admin_id': admin_id, 'size': size, 'search': search}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, 'Dashio/check_stu_achiev.html', {'all_ach_dict': dict})
    else:
        if student_department_tab.objects.filter(student_id=id).exists():
            d_id = student_department_tab.objects.filter(student_id=id)[0].d_id
            department = department_tab.objects.filter(d_id=d_id)[0].name
        else:
            department = -1
        err_msg = "该学生暂无可查询成果"
        stu_info = student_tab.objects.filter(student_id=id)[0]
        dict = {'admin_id': admin_id, 'stu_info': stu_info, 'err_msg': err_msg, 'department': department}
        # if "img" not in request.path_info:
        #     path0 = request.session['path']
        #     request.session['path'] = path0 + "@" + request.path_info
        #     print(request.session['path'])
        return render(request, "Dashio/check_student_info.html", {'check_student': dict})


# 查看某一成果的相关学者
def check_achievement_scholar(request, id):
    a_id = id
    dep = ''
    # 存在关联信息
    if scholar_achievement_tab.objects.filter(a_id=a_id).exists():
        size = achievement_tab.objects.filter(a_id=a_id)[0]
        all_scholar = []
        for i in scholar_achievement_tab.objects.filter(a_id=a_id):
            all_scholar.append(scholar_tab.objects.filter(scholar_id=i.scholar_id)[0])
            # sch_info = scholar_tab.objects.filter(scholar_id=i.scholar_id)[0]
            # # 只展示已认证的学者
            # if sch_info.flag == 1:
            #     all_scholar.append(scholar_tab.objects.filter(scholar_id=i.scholar_id)[0])
        # if len(all_scholar) == 0:
        #     err_msg = "该成果暂无可查询相关学者信息"
        #     ach_info = achievement_tab.objects.filter(a_id=a_id)[0]
        #     dict = {'admin_id': admin_id, 'ach_info': ach_info, 'err_msg': err_msg}
        #     return render(request, "Dashio/check_achiev_detail.html", {'check_ach': dict})
        dict = {'admin_id': admin_id, 'all_sch': all_scholar, 'size': size, 'dep': dep}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, 'Dashio/check_scholar.html', {'all_scholar': dict})
    else:
        err_msg = "该成果暂无可查询相关学者信息"
        ach_info = achievement_tab.objects.filter(a_id=a_id)[0]
        dict = {'admin_id': admin_id, 'ach_info': ach_info, 'err_msg': err_msg}
        return render(request, "Dashio/check_achiev_detail.html", {'check_ach': dict})


# 查看某一成果的相关学者
def check_achievement_student(request, id):
    a_id = id
    dep = ''
    # 存在关联信息
    if student_achievement_tab.objects.filter(a_id=a_id).exists():
        size = stuachievement_tab.objects.filter(a_id=a_id)[0]
        all_student = []
        for i in student_achievement_tab.objects.filter(a_id=a_id):
            all_student.append(student_tab.objects.filter(student_id=i.student_id)[0])
        dict = {'admin_id': admin_id, 'all_student': all_student, 'size': size, 'dep': dep}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, 'Dashio/student.html', {'all_student_dict': dict})
    else:
        err_msg = "该成果暂无可查询相关学生信息"
        ach_info = stuachievement_tab.objects.filter(a_id=a_id)[0]
        dict = {'admin_id': admin_id, 'ach_info': ach_info, 'err_msg': err_msg}
        return render(request, "Dashio/check_stu_achiev_detail.html", {'check_ach': dict})


# 查看某一院系的相关学者
def check_department_scholar(request, id):
    d_id = id
    # 存在关联信息
    if scholar_department_tab.objects.filter(d_id=d_id).exists():
        dep = department_tab.objects.filter(d_id=d_id)[0]
        size = ''
        all_scholar = []
        for i in scholar_department_tab.objects.filter(d_id=d_id):
            all_scholar.append(scholar_tab.objects.filter(scholar_id=i.scholar_id)[0])
            # sch_info = scholar_tab.objects.filter(scholar_id=i.scholar_id)[0]
            # # 只展示已认证的学者
            # if sch_info.flag == 1:
            #     all_scholar.append(scholar_tab.objects.filter(scholar_id=i.scholar_id)[0])
        if len(all_scholar) == 0:
            err_msg = "该院系暂无可查询相关学者信息"
            dep_info = department_tab.objects.filter(d_id=d_id)[0]
            dict = {'admin_id': admin_id, 'dep_info': dep_info, 'err_msg': err_msg}
            return render(request, "Dashio/check_dep_brief.html", {'check_dep': dict})
        else:
            dict = {'admin_id': admin_id, 'all_sch': all_scholar, 'size': size, 'dep': dep}
            if "img" not in request.path_info:
                path0 = request.session['path']
                request.session['path'] = path0 + "@" + request.path_info
                print(request.session['path'])
            return render(request, 'Dashio/check_scholar.html', {'all_scholar': dict})
    else:
        err_msg = "该院系暂无可查询相关学者信息"
        dep_info = department_tab.objects.filter(d_id=d_id)[0]
        dict = {'admin_id': admin_id, 'dep_info': dep_info, 'err_msg': err_msg}
        return render(request, "Dashio/check_dep_brief.html", {'check_dep': dict})


# 查看某一院系的相关学生
def check_department_student(request, id):
    d_id = id
    # 存在关联信息
    if student_department_tab.objects.filter(d_id=d_id).exists():
        dep = department_tab.objects.filter(d_id=d_id)[0]
        size = ''
        all_student = []
        for i in student_department_tab.objects.filter(d_id=d_id):
            all_student.append(student_tab.objects.filter(student_id=i.student_id)[0])
        # if len(all_student) == 0:
        #     err_msg = "该院系暂无可查询相关学生信息"
        #     dep_info = department_tab.objects.filter(d_id=d_id)[0]
        #     dict = {'admin_id': admin_id, 'dep_info': dep_info, 'err_msg': err_msg}
        #     return render(request, "Dashio/check_dep_brief.html", {'check_dep': dict})
        # else:
        dict = {'admin_id': admin_id, 'all_student': all_student, 'size': size, 'dep': dep}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, 'Dashio/student.html', {'all_student_dict': dict})
    else:
        err_msg = "该院系暂无可查询相关学生信息"
        dep_info = department_tab.objects.filter(d_id=d_id)[0]
        dict = {'admin_id': admin_id, 'dep_info': dep_info, 'err_msg': err_msg}
        return render(request, "Dashio/check_dep_brief.html", {'check_dep': dict})


# 查看成果认证里的关联学者
def check_achauthen_scholar(request, id):
    # 拆分all_id 判断all_id是否为空
    all_id =  achievement_authen_tab.objects.filter(id=id)[0].all_id
    sch_id = achievement_authen_tab.objects.filter(id=id)[0].scholar_id
    if all_id == '' or all_id is None:
        err_msg = "该成果暂无可查询相关学者信息"
        auth_info = achievement_authen_tab.objects.filter(id=id)[0]
        # newach_auth = auth_info
        scholar_id = auth_info.scholar_id
        scholar_name = scholar_tab.objects.filter(scholar_id=scholar_id)[0].name
        dict = {'admin_id': admin_id, 'auth_info': auth_info, 'scholar_name': scholar_name, 'err_msg': err_msg}
        return render(request, "Dashio/check_newachiev_details.html", {'check_newauth': dict})
    else:
        #将关联的学者id转换为list
        id_list = all_id.split(",")
        size = ''
        dep = ''
        all_scholar = []   # 相关学者信息列表
        for i in id_list:
            sch_info = scholar_tab.objects.filter(scholar_id=int(i))[0]
            # 只展示已认证的学者
            if sch_info.flag == 1:
                all_scholar.append(sch_info)
        all_scholar.append(sch_id)
        if len(all_scholar) == 0:
            err_msg = "该成果暂无可查询相关学者信息"
            auth_info = achievement_authen_tab.objects.filter(id=id)[0]
            # newach_auth = auth_info
            scholar_id = auth_info.scholar_id
            scholar_name = scholar_tab.objects.filter(scholar_id=scholar_id)[0].name
            dict = {'admin_id': admin_id, 'auth_info': auth_info, 'scholar_name': scholar_name, 'err_msg': err_msg}
            return render(request, "Dashio/check_newachiev_details.html", {'check_newauth': dict})
        else:
            dict = {'admin_id': admin_id, 'all_sch': all_scholar, 'size': size, 'dep': dep}
            if "img" not in request.path_info:
                path0 = request.session['path']
                request.session['path'] = path0 + "@" + request.path_info
                print(request.session['path'])
            return render(request, 'Dashio/check_scholar.html', {'all_scholar': dict})


# 返回上一页
def to_last_page(request):
    path0 = request.session['path']
    path = path0.split('@')
    print(path)
    path.pop()
    last_path = path[-1]
    path.pop()
    path1 = ""
    for p in path:
        path1 = path1 + "@" + p
    request.session['path'] = path1
    return redirect(last_path)


# 搜索成果
def search_ach(request):
    global release_year
    global release_year2
    global author_name
    global keyword
    global ach_name
    global release_year_type
    global ach_keyword_type
    global author_name_type
    global ach_name_type
    global search1
    global search2
    global search3
    global search4
    global search5
    global type1
    global type2
    global type3
    global type4
    global type5
    global search1_text
    global search2_text
    global search3_text
    global search4_text
    global search5_text
    global search_err_msg
    global check_scholar
    global check_student
    if request.method == "GET":  # 如果提交方式为GET即显示check_achiev.html
        release_year = ''
        release_year2 = ''
        author_name = ''
        keyword = ''
        ach_name = ''
        release_year_type = ''
        ach_keyword_type = ''
        author_name_type = ''
        ach_name_type = ''
        type1 = ''
        type2 = ''
        type3 = ''
        type4 = ''
        type5 = ''
        search1 = ''
        search2 = ''
        search3 = ''
        search4 = ''
        search5 = ''
        search1_text = ''
        search2_text = ''
        search3_text = ''
        search4_text = ''
        search5_text = ''
	# err_msg = request.session['search_err_msg']
        err_msg = search_err_msg
        search_err_msg = ''
        check_scholar = ''
        check_student = ''
        year1 = achievement_tab.objects.values('year').distinct().order_by('year')
        year2 = stuachievement_tab.objects.values('year').distinct().order_by('year')
        # year = list(set(year1).union(set(year2)))
        year = []
        for y in year1:
            year.append(y)
        for y in year2:
            year.append(y)
        dict = {'admin_id': admin_id, 'year': year, 'release_year': release_year, 'release_year2': release_year2,
                'author_name': author_name, 'keyword': keyword, 'ach_name': ach_name,
                'release_year_type': release_year_type, 'ach_keyword_type': ach_keyword_type,
                'author_name_type': author_name_type, 'ach_name_type': ach_name_type,
                'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4, 'type5': type5,
                'search1': search1, 'search2': search2, 'search3': search3, 'search4': search4, 'search5': search5,
                'search1_text': search1_text, 'search2_text': search2_text, 'search3_text': search3_text,
                'search4_text': search4_text, 'search5_text': search5_text, 'err_msg': err_msg,
                'check_scholar': check_scholar, 'check_student': check_student}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, 'Dashio/search_ach.html', {'search_dict': dict})
    else:
        return


# 修改搜索规则
'''
def change_search_ach(request):
    global release_year
    global release_year2
    global author_name
    global keyword
    global ach_name
    global release_year_type
    global ach_keyword_type
    global author_name_type
    global ach_name_type
    global type1
    global type2
    global type3
    global type4
    global type5
    global search1_text
    global search2_text
    global search3_text
    global search4_text
    global search5_text
    global ach_keyword_type
    global author_name_type
    global ach_name_type
    global search_err_msg
    global check_scholar
    global check_student
    if request.method == "GET":
        err_msg = search_err_msg
        search_err_msg = ''
        year1 = achievement_tab.objects.values('year').distinct().order_by('year')
        year2 = stuachievement_tab.objects.values('year').distinct().order_by('year')
        year = []
        for y in year1:
            year.append(y)
        for y in year2:
            year.append(y)
        dict = {'admin_id': admin_id, 'year': year, 'release_year': release_year, 'release_year2': release_year2,
                'author_name': author_name, 'keyword': keyword, 'ach_name': ach_name,
                'release_year_type': release_year_type, 'ach_keyword_type': ach_keyword_type,
                'author_name_type': author_name_type, 'ach_name_type': ach_name_type,
                'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4, 'type5': type5,
                'search1': search1, 'search2': search2, 'search3': search3, 'search4': search4, 'search5': search5,
                'search1_text': search1_text, 'search2_text': search2_text, 'search3_text': search3_text,
                'search4_text': search4_text, 'search5_text': search5_text, 'err_msg': err_msg,
                'check_scholar': check_scholar, 'check_student': check_student}
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request, 'Dashio/search_ach.html', {'search_dict': dict})
    else:
        return
'''
def change_search_ach(request):
    if request.method == "GET":
        return search_ach_demo(request, 1)
    else:
        return


def search_ach_demo(request, type):
    global release_year
    global release_year2
    global author_name
    global keyword
    global ach_name
    global release_year_type
    global ach_keyword_type
    global author_name_type
    global ach_name_type
    global type1
    global type2
    global type3
    global type4
    global type5
    global search1_text
    global search2_text
    global search3_text
    global search4_text
    global search5_text
    global ach_keyword_type
    global author_name_type
    global ach_name_type
    global search_err_msg
    global check_scholar
    global check_student
    err_msg = search_err_msg
    search_err_msg = ''
    year1 = achievement_tab.objects.values('year').distinct().order_by('year')
    year2 = stuachievement_tab.objects.values('year').distinct().order_by('year')
    year = []
    for y in year1:
        year.append(y)
    for y in year2:
        year.append(y)
    dict = {'admin_id': admin_id, 'year': year, 'release_year': release_year, 'release_year2': release_year2,
            'author_name': author_name, 'keyword': keyword, 'ach_name': ach_name,
            'release_year_type': release_year_type, 'ach_keyword_type': ach_keyword_type,
            'author_name_type': author_name_type, 'ach_name_type': ach_name_type,
            'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4, 'type5': type5,
            'search1': search1, 'search2': search2, 'search3': search3, 'search4': search4, 'search5': search5,
            'search1_text': search1_text, 'search2_text': search2_text, 'search3_text': search3_text,
            'search4_text': search4_text, 'search5_text': search5_text, 'err_msg': err_msg,
            'check_scholar': check_scholar, 'check_student': check_student}
    if "img" not in request.path_info and type == 1:
        path0 = request.session['path']
        request.session['path'] = path0 + "@" + request.path_info
        print(request.session['path'])
    return render(request, 'Dashio/search_ach.html', {'search_dict': dict})


def cal_search_ach(op, ach0, ach1):
    if op == "AND":
        return set(ach0).intersection(set(ach1))
    elif op == "OR":
        return set(ach0).union(set(ach1))
    else:
        return set(ach0).difference(set(ach1))


def check_search_ach(request):
    global release_year
    global release_year2
    global author_name
    global keyword
    global ach_name
    global release_year_type
    global ach_keyword_type
    global author_name_type
    global ach_name_type
    global search1  # 对应的查询字段
    global search2
    global search3
    global search4
    global search5
    global type1  # 对应类型 and or not
    global type2
    global type3
    global type4
    global type5
    global search1_text  # 对应的查询内容
    global search2_text
    global search3_text
    global search4_text
    global search5_text
    global ach_keyword_type
    global author_name_type
    global ach_name_type
    global search_err_msg
    global check_scholar
    global check_student
    if request.method == "POST":
        release_year = request.POST.get('release_year')
        release_year2 = request.POST.get('release_year2')
        author_name = request.POST.get('author_name')
        keyword = request.POST.get('ach_keyword')
        ach_name = request.POST.get('ach_name')
        release_year_type = request.POST.get('release_year_type')
        ach_keyword_type = request.POST.get('ach_keyword_type')
        author_name_type = request.POST.get('author_name_type')
        ach_name_type = request.POST.get('ach_name_type')
        type1 = request.POST.get('type1')
        type2 = request.POST.get('type2')
        type3 = request.POST.get('type3')
        type4 = request.POST.get('type4')
        type5 = request.POST.get('type5')
        search1 = request.POST.get('search1')
        search2 = request.POST.get('search2')
        search3 = request.POST.get('search3')
        search4 = request.POST.get('search4')
        search5 = request.POST.get('search5')
        search1_text = request.POST.get('search1_text')
        search2_text = request.POST.get('search2_text')
        search3_text = request.POST.get('search3_text')
        search4_text = request.POST.get('search4_text')
        search5_text = request.POST.get('search5_text')
        check_scholar = request.POST.get('checkbox_scholar')
        check_student = request.POST.get('checkbox_student')
        all_ach_type = 0  # 成果搜索范围
        if check_scholar is None:
            check_scholar = "0"
            if check_student is None:
                # 出错
		# request.session['search_err_msg']="test err"
                search_err_msg = "需至少在学者成果和学生成果中选择一项"
                # path0 = request.session['path']
                # path = path0.split('@')
                # last_path = path[-1]
                # path.pop()
                # return redirect(last_path)
                return search_ach_demo(request, 0)
            else:
                all_ach_type = 1  # 只学生
        elif check_student is None:
            all_ach_type = 0  # 只学者
        else:
            all_ach_type = 2  # 学者+学生
        # if check_student is None:
        #     check_student = "0"
        # all_ach = AchievementTab.objects.filter(
        #     Q(name__icontains=ach_name) | Q(author_name__icontains=author) | Q(keyword__icontains=keyword))
        if release_year == 'all':
            if release_year2 != 'all':
                search_err_msg = "成果发表年份需要同时选择all"
                # path0 = request.session['path']
                # path = path0.split('@')
                # last_path = path[-1]
                # path.pop()
                # return redirect(last_path)
                return search_ach_demo(request, 0)
        elif release_year2 == 'all':
            if release_year != 'all':
                search_err_msg = "成果发表年份需要同时选择all"
                # path0 = request.session['path']
                # path = path0.split('@')
                # last_path = path[-1]
                # path.pop()
                # return redirect(last_path)
                return search_ach_demo(request, 0)
        elif int(release_year2) < int(release_year):
            search_err_msg = "成果发表年份起始时间选择错误"
            # path0 = request.session['path']
            # path = path0.split('@')
            # last_path = path[-1]
            # path.pop()
            # return redirect(last_path)
            return search_ach_demo(request, 0)
        else:
            search_err_msg = ''
    if release_year == 'all':
        if all_ach_type == 0:
            all_ach_year = achievement_tab.objects.filter()
        elif all_ach_type == 1:
            all_stu_ach_year = stuachievement_tab.objects.filter()
        else:
            all_ach_year = achievement_tab.objects.filter()
            all_stu_ach_year = stuachievement_tab.objects.filter()
    else:
        years1 = []
        for i in achievement_tab.objects.values('year').distinct().order_by('year'):
            for y in i.values():
                if int(release_year) <= int(y) <= int(release_year2):
                    years1.append(y)
            # if int(release_year) <= int(i.year) <= int(release_year2):
            #     years.append(i.year)
        years2 = []
        for i in stuachievement_tab.objects.values('year').distinct().order_by('year'):
            for y in i.values():
                if int(release_year) <= int(y) <= int(release_year2):
                    years2.append(y)
        if all_ach_type == 0:
            all_ach_year = achievement_tab.objects.filter(year__in=years1)
        elif all_ach_type == 1:
            all_stu_ach_year = stuachievement_tab.objects.filter(year__in=years2)
        else:
            all_ach_year = achievement_tab.objects.filter(year__in=years1)
            all_stu_ach_year = stuachievement_tab.objects.filter(year__in=years2)
    if ach_name == '':
        all_ach2 = []
        all_stu_ach2 = []
    else:
        if all_ach_type == 0:
            all_ach2 = achievement_tab.objects.filter(name__icontains=ach_name)
        elif all_ach_type == 1:
            all_stu_ach2 = stuachievement_tab.objects.filter(name__icontains=ach_name)
        else:
            all_ach2 = achievement_tab.objects.filter(name__icontains=ach_name)
            all_stu_ach2 = stuachievement_tab.objects.filter(name__icontains=ach_name)
    if author_name == '':
        all_ach3 = []
        all_stu_ach3 = []
    else:
        if all_ach_type == 0:
            all_ach3 = achievement_tab.objects.filter(author_name__icontains=author_name)
        elif all_ach_type == 1:
            all_stu_ach3 = stuachievement_tab.objects.filter(author_name__icontains=author_name)
        else:
            all_ach3 = achievement_tab.objects.filter(author_name__icontains=author_name)
            all_stu_ach3 = stuachievement_tab.objects.filter(author_name__icontains=author_name)
    if keyword == '':
        all_ach4 = []
        all_stu_ach4 = []
    else:
        if all_ach_type == 0:
            all_ach4 = achievement_tab.objects.filter(keyword__icontains=keyword)
        elif all_ach_type == 1:
            all_stu_ach4 = stuachievement_tab.objects.filter(keyword__icontains=keyword)
        else:
            all_ach4 = achievement_tab.objects.filter(keyword__icontains=keyword)
            all_stu_ach4 = stuachievement_tab.objects.filter(keyword__icontains=keyword)
    if all_ach_type == 0:
        all_ach = achievement_tab.objects.filter()
        all_ach = cal_search_ach(release_year_type, all_ach, all_ach_year)
        all_ach = cal_search_ach(ach_name_type, all_ach, all_ach2)
        all_ach = cal_search_ach(author_name_type, all_ach, all_ach3)
        all_ach = cal_search_ach(ach_keyword_type, all_ach, all_ach4)
        all_ach = cal_search_ach(type1, all_ach, find_ach(search1, search1_text, all_ach_type))
        all_ach = cal_search_ach(type2, all_ach, find_ach(search2, search2_text, all_ach_type))
        all_ach = cal_search_ach(type3, all_ach, find_ach(search3, search3_text, all_ach_type))
        all_ach = cal_search_ach(type4, all_ach, find_ach(search4, search4_text, all_ach_type))
        all_ach = cal_search_ach(type5, all_ach, find_ach(search5, search5_text, all_ach_type))
        all_stu_ach = []
    elif all_ach_type == 1:
        all_stu_ach = stuachievement_tab.objects.filter()
        all_stu_ach = cal_search_ach(release_year_type, all_stu_ach, all_stu_ach_year)
        all_stu_ach = cal_search_ach(ach_name_type, all_stu_ach, all_stu_ach2)
        all_stu_ach = cal_search_ach(author_name_type, all_stu_ach, all_stu_ach3)
        all_stu_ach = cal_search_ach(ach_keyword_type, all_stu_ach, all_stu_ach4)
        all_stu_ach = cal_search_ach(type1, all_stu_ach, find_ach(search1, search1_text, all_ach_type))
        all_stu_ach = cal_search_ach(type2, all_stu_ach, find_ach(search2, search2_text, all_ach_type))
        all_stu_ach = cal_search_ach(type3, all_stu_ach, find_ach(search3, search3_text, all_ach_type))
        all_stu_ach = cal_search_ach(type4, all_stu_ach, find_ach(search4, search4_text, all_ach_type))
        all_stu_ach = cal_search_ach(type5, all_stu_ach, find_ach(search5, search5_text, all_ach_type))
        all_ach = []
    else:
        all_ach = achievement_tab.objects.filter()
        all_ach = cal_search_ach(release_year_type, all_ach, all_ach_year)
        all_ach = cal_search_ach(ach_name_type, all_ach, all_ach2)
        all_ach = cal_search_ach(author_name_type, all_ach, all_ach3)
        all_ach = cal_search_ach(ach_keyword_type, all_ach, all_ach4)
        all_ach = cal_search_ach(type1, all_ach, find_ach(search1, search1_text, 0))
        all_ach = cal_search_ach(type2, all_ach, find_ach(search2, search2_text, 0))
        all_ach = cal_search_ach(type3, all_ach, find_ach(search3, search3_text, 0))
        all_ach = cal_search_ach(type4, all_ach, find_ach(search4, search4_text, 0))
        all_ach = cal_search_ach(type5, all_ach, find_ach(search5, search5_text, 0))
        all_stu_ach = stuachievement_tab.objects.filter()
        all_stu_ach = cal_search_ach(release_year_type, all_stu_ach, all_stu_ach_year)
        all_stu_ach = cal_search_ach(ach_name_type, all_stu_ach, all_stu_ach2)
        all_stu_ach = cal_search_ach(author_name_type, all_stu_ach, all_stu_ach3)
        all_stu_ach = cal_search_ach(ach_keyword_type, all_stu_ach, all_stu_ach4)
        all_stu_ach = cal_search_ach(type1, all_stu_ach, find_ach(search1, search1_text, 1))
        all_stu_ach = cal_search_ach(type2, all_stu_ach, find_ach(search2, search2_text, 1))
        all_stu_ach = cal_search_ach(type3, all_stu_ach, find_ach(search3, search3_text, 1))
        all_stu_ach = cal_search_ach(type4, all_stu_ach, find_ach(search4, search4_text, 1))
        all_stu_ach = cal_search_ach(type5, all_stu_ach, find_ach(search5, search5_text, 1))
    # for i in all_ach:
    #     print(i.name)
    size = ""
    search = "搜索结果"
    dict = {'all_achievements': all_ach, 'all_stu_ach': all_stu_ach, 'admin_id': admin_id, 'size': size, 'search': search}
    if "img" not in request.path_info:
        path0 = request.session['path']
        request.session['path'] = path0 + "@" + request.path_info
        print(request.session['path'])
    return render(request, 'Dashio/check_achiev.html', {'all_ach_dict': dict})


def find_ach(search, search_text, all_ach_type):
    if search_text == '':
        ach = []
        return ach
    if search == '无':
        ach = []
        return ach
    elif search == 'keyword':
        if all_ach_type == 0:
            return achievement_tab.objects.filter(keyword__icontains=search_text)
        elif all_ach_type == 1:
            return stuachievement_tab.objects.filter(keyword__icontains=search_text)
    elif search == 'author':
        if all_ach_type == 0:
            return achievement_tab.objects.filter(author_name__icontains=search_text)
        elif all_ach_type == 1:
            return stuachievement_tab.objects.filter(author_name__icontains=search_text)
    elif search == 'name':
        if all_ach_type == 0:
            return achievement_tab.objects.filter(name__icontains=search_text)
        elif all_ach_type == 1:
            return stuachievement_tab.objects.filter(name__icontains=search_text)
    else:
        ach = []
        return ach


# 管理端管理员发布公告
def release_announce(request):
    global ann_err_msg
    if request.method == "POST":
        title = request.POST.get('ann_title')
        content = request.POST.get('ann_content')
        if len(title) > 100:
            ann_err_msg = "公告标题长度不能超过100个字符"
        elif len(content) > 400:
            ann_err_msg = "公告内容不应超过400个字符"
        else:
            information_tab.objects.create(title=title, information=content)
            ann_err_msg = "公告发布成功"
        return redirect('/check_announce')
    if request.method == "GET":
        all_ann = information_tab.objects.all()
        dict = {'admin_id': admin_id,'all_ann':all_ann, 'err_msg': ann_err_msg}
        ann_err_msg = ''
        return render(request,'Dashio/release_announce.html',{'all_ann_dict':dict})


def del_announce(request, id):
    information_tab.objects.filter(infoId=id).delete()
    return redirect('/check_announce')


# 举报信息详情
def show_report_detail(request, id):
    report_info = report_tab.objects.filter(r_id=id)
    all_re_dict = {'report_info': report_info[0], 'admin_id': admin_id}
    if request.method == "GET":
        if "img" not in request.path_info:
            path0 = request.session['path']
            request.session['path'] = path0 + "@" + request.path_info
            print(request.session['path'])
        return render(request,'Dashio/report_detail.html',{'all_re_dict':all_re_dict})
    if request.method == "POST":
        information = request.POST.get('reject_info')
        report = report_tab.objects.get(r_id=id)
        print(request.POST.get('reject_info'))
        user_id = report.id
        title = ""
        info_last = ""
        if report.typeR == 0:
            title = "您举报学者信息未成功"
            info_last = "被举报学者名：" + report_info[0].user_name + " 举报未成功原因：" + information
        if report.typeR == 1:
            ach = achievement_tab.objects.get(a_id=id)
            title = "您举报成果信息未成功"
            info_last = "被举报成果名：" + ach.name + " 举报未成功原因：" + information
        person_inform_tab.objects.create(user_id=user_id, title=title, information=info_last)
        # return redirect('/delete_one_report/'+id)
        report_tab.objects.filter(r_id=id).update(flag=1)
        return redirect('/checkreport')


# 管理员通过举报 添加反馈
def add_pass_report(request,id):
    report = report_tab.objects.get(r_id=id)
    information = report.information
    if report.typeR == 0:
        user_id = report.a_id
        title="您的学者信息被举报"
        person_inform_tab.objects.create(user_id=user_id, title=title,information=information)
        re_info="您发布的举报学者：" + report.user_name +"信息已经通过"
        person_inform_tab.objects.create(user_id=report.id, title="您的举报信息已经通过", information=re_info)
    if report.typeR == 1:
        all_sch = scholar_achievement_tab.objects.filter(a_id=report.a_id)
        ach = achievement_tab.objects.get(a_id=id)
        info_last = "被举报成果名：" + ach.name + " 举报原因：" + information
        re_info = "您发布的举报成果：" + ach.name +"信息已经通过"
        titlt="您的成果信息被举报"
        for i in all_sch:
            user_id = i.scholar_id
            person_inform_tab.objects.create(user_id=user_id,title=titlt,information=info_last)
        person_inform_tab.objects.create(user_id=report.id, title="您的举报信息已经通过", information=re_info)
    report_tab.objects.filter(r_id=id).update(flag=1)
    return redirect('/checkreport')


def login_check(request):
    if request.session.get('verfiy', None) != 'is_login':
        print('no')
        return redirect('/login')
    else:
        print()







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
返回公告信息
'''
def getnoticeList():
    retData = []
    infor = information_tab.objects.all()
    for i in infor:
        a = {}
        a['infoId'] = i.infoId
        a['title'] = i.title
        retData.append(a)
    return retData


'''
返回院系信息
'''
def getdepartment():
    retData = []
    depart = department_tab.objects.all()
    for i in depart:
        a = {}
        a['name'] = i.name
        a['d_id'] = i.d_id
        a['number'] = i.number
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
    retData['noticeList'] = getnoticeList()
    retData['department'] = getdepartment()
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
    retData['author'] = achieve.author_name
    brief = achievement_brief_tab.objects.filter(a_id = a_id).order_by('-number').reverse()
    retData['brief'] = ''
    for i in brief:
        retData['brief'] += i.brief
    retData['Scholar'] = []
    sa1 = scholar_achievement_tab.objects.filter(a_id = a_id)
    for i in sa1:
        scholar_id = i.scholar_id
        scholar = scholar_tab.objects.filter(scholar_id = scholar_id)
        a = {}
        a['scholar_id'] = scholar[0].scholar_id
        a['get_id'] = scholar[0].get_id
        a['name'] = scholar[0].name
        a['position'] = scholar[0].p_title
        a['school'] = scholar[0].school
        retData['Scholar'].append(a)
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
    d_id = request.GET['id']
    sdt = scholar_department_tab.objects.filter(d_id = d_id)
    for i in sdt:
        a = {}
        a1s1 = scholar_tab.objects.filter(scholar_id = i.scholar_id)
        if len(a1s1) == 0:
            continue
        s1 = scholar_tab.objects.get(scholar_id = i.scholar_id)
        a['name'] = s1.name
        a['p_title'] = s1.p_title
        a['get_id'] = s1.get_id
        a['email'] = s1.email
        a['id'] = s1.scholar_id
        retData.append(a)
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
    s1 = scholar_brief_intro_tab.objects.filter(scholar_id = s_id).order_by('-number').reverse()
    retData['brief'] = ''
    if len(s1) == 0:
        retData['brief'] = '暂无简介'
    else:
        for i in s1:
            retData['brief'] += i.brief
    retData['Achievement'] = []
    sat1 = scholar_achievement_tab.objects.filter(scholar_id = s_id)
    for i in sat1:
        a_id = i.a_id
        achieve = achievement_tab.objects.filter(a_id = a_id)
        a = {}
        a['name'] = achieve[0].name
        a['a_id'] = a_id
        a['year'] = achieve[0].year
        a['num_view'] = achieve[0].num_view
        retData['Achievement'].append(a)
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
    user_id = request.GET['user_id']
    print(request.GET['user_id'])
    user = user_tab.objects.get(user_id = user_id)
    print(user.user_name)
    retData['user_name'] = user.user_name
    if user.authority == 0:
        retData['studentNumber'] = '请先进行认证'
        retData['school'] = '请先进行认证'
        retData['department'] = '请先进行认证'
        retData['mail'] = '请先进行认证'
    if user.authority == 1:
        scholar = scholar_tab.objects.filter(user_id = user_id)
        retData['name'] = scholar[0].name
        retData['studentNumber'] = scholar[0].Scholar_Number
        retData['school'] = scholar[0].school
        retData['mail'] = scholar[0].email
        scholar_id = scholar[0].scholar_id
        sdt = scholar_department_tab.objects.filter(scholar_id = scholar_id)
        d_id = sdt[0].d_id
        retData['department'] = department_tab.objects.get(d_id = d_id).name
    if user.authority == 2:
        stu = student_tab.objects.filter(user_id = user_id)
        retData['name'] = stu[0].name
        retData['studentNumber'] = stu[0].sno
        retData['school'] = stu[0].school
        retData['mail'] = stu[0].email
        student_id = stu[0].student_id
        sdt = student_department_tab.objects.filter(student_id = student_id)
        d_id = sdt[0].d_id
        retData['department'] = department_tab.objects.get(d_id = d_id).name
    return HttpResponse(json.dumps(retData), content_type = 'application/json')



'''
学生认证
'''
def StudentCerti(request):
    retData = {}
    name = request.GET['name']
    print(name)
    department = request.GET['department']
    print(department)
    studentNumber = request.GET['studentNumber']
    print(studentNumber)
    mail = request.GET['mail']
    print(mail)
    user_id = request.GET['user_id']
    print(user_id)
    school = request.GET['school']
    print(school)
    authen_tab(email = mail, name = name, sno = studentNumber, department = department, identity = 2, school = school).save()
    a1 = authen_tab.objects.filter(name = name, email = mail, department = department, identity = 2)
    print(a1[0].authen_id)
    user_authen_tab(authen_id = a1[0].authen_id, user_id = user_id).save()
    return HttpResponse(json.dumps(retData), content_type = 'application/json')
'''
学者认证
'''
def ScholarCerti(request):
    retData = {}
    name = request.GET['name']
    print(name)
    department = request.GET['department']
    print(department)
    studentNumber = request.GET['studentNumber']
    print(studentNumber)
    mail = request.GET['mail']
    print(mail)
    user_id = request.GET['user_id']
    print(user_id)
    school = request.GET['school']
    print(school)
    authen_tab(email = mail, name = name, sno = studentNumber, department = department, identity = 1, school = school).save()
    a1 = authen_tab.objects.filter(name = name, email = mail, department = department, identity = 1)
    print(a1[0].authen_id)
    user_authen_tab(authen_id = a1[0].authen_id, user_id = user_id).save()
    return HttpResponse(json.dumps(retData), content_type = 'application/json')
    





'''
展示图片
'''
def show_log(request):
    get_id = request.GET['get_id']
    path = '../image/' + get_id + '.jpg'
    module_dir = os.path.dirname(__file__)
    path = os.path.join(module_dir, path)
    file_one = open(path, "rb")
    return HttpResponse(file_one.read(), content_type = 'image/jpg')



'''
展示院系图片
'''
def show_department_image(request):
    d_id = request.GET['d_id']
    path = '../image-department/' + d_id + '.png'
    module_dir = os.path.dirname(__file__)
    path = os.path.join(module_dir, path)
    file_one = open(path, 'rb')
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
    
      
'''
根据检索的信息提供学院数据
'''  
def GetDepartment(request):
    retData = []
    search = request.GET['search']
    d1 = department_tab.objects.all()
    for i in d1:
        if search in i.name:
            a = {}
            a['name'] = i.name
            a['d_id'] = i.d_id
            retData.append(a)
    if len(retData) != 0:
        return HttpResponse(json.dumps(retData), content_type = 'application/json')
    
    for i in d1:
        a = {}
        a['name'] = i.name
        a['d_id'] = i.d_id
        retData.append(a)
    return HttpResponse(json.dumps(retData), content_type = 'application/json')

def getNotice(request):
    infoId = request.GET['infoId']
    info = information_tab.objects.get(infoId = infoId)
    retData = {}
    retData['title'] = info.title
    retData['information'] = info.information
    return HttpResponse(json.dumps(retData), content_type = 'application/json')



def getAllNotice(request):
    retData = getnoticeList()
    return HttpResponse(json.dumps(retData), content_type = 'application/json')



def achievePost(request):
    retData = {}
    name = request.GET['name'] #成果名
    type1 = request.GET['type'] #成果类型
    year = request.GET['link']  #成果年份
    fabiao = request.GET['fabiao']#成果发表
    keyword = request.GET['keyword'] #成果关键词
    brief = request.GET['brief'] #成果摘要
    author1 = request.GET['author1'] #作者1
    author2 = request.GET['author2'] #作者2
    author3 = request.GET['author3'] #作者3
    author_o = request.GET['author_o'] #作者其他
    authority = request.GET['authority'] #提交者身份
    user_id = request.GET['user_id']
    if authority == '0':
        return HttpResponse(json.dumps(retData), content_type = 'application/json')
    if authority == '1':
        scholar = scholar_tab.objects.filter(user_id = user_id)
        scholar_id = scholar[0].scholar_id
        author = []
        if author1 != '':
            author.append(author1)
        if author2 != '':
            author.append(author2)
        if author3 != '':
            author.append(author3)
        if author_o != '':
            author_o = author_o.split(';' or '；' or ',' or '，' or ' ')
        for i in author_o:
            author.append(i)
        id_show = ''
        author_show = ''
        for i in author:
            author_show += (i + ',')
            scho1 = scholar_tab.objects.filter(name = i)
            if len(scho1) != 0:
                id_show += (str(scho1[0].scholar_id) + ',')
        author_show = author_show[0: len(author_show) - 1]
        if len(id_show) != 0:
            id_show = id_show[0:len(id_show) - 1]
        achievement_authen_tab(scholar_id = scholar_id,
        all_id = id_show, a_name = name, year = year, author_name = author_show, 
        citation = 0, j_a_name = fabiao, file = '暂无', link = '暂无', 
        kind = type1, num_view = 0, keyword = keyword, brief = brief).save()
        return HttpResponse(json.dumps(retData), content_type = 'application/json') 
    
    stu1 = student_tab.objects.filter(user_id = user_id)
    author_name = stu1[0].name
    student_id = stu1[0].student_id
    stuachievement_tab(name = name, year = year, author_name = author_name, 
     citation = 0, j_a_name = '暂无', file = '暂无', link = '暂无', 
     kind = type1, num_view = 0, brief = 0, keyword = keyword).save()
    achi = stuachievement_tab.objects.filter(name = name, author_name = author_name)
    a_id = achi[0].a_id
    student_achievement_tab(student_id = student_id, a_id = a_id).save()
    return HttpResponse(json.dumps(retData), content_type = 'application/json') 


def getVerify(request):
    retData = []
    user_id = request.GET['user_id']
    scholar  = scholar_tab.objects.filter(user_id = user_id)
    if len(scholar) == 0:
        return HttpResponse(json.dumps(retData), content_type = 'application/json')
    scholar_name = scholar[0].name
    achieve_authen = achievement_authen_tab.objects.all()
    for i in achieve_authen:
        if scholar_name in i.author_name:
            a = {}
            a['name'] = i.a_name
            a['author'] = i.author_name
            a['type'] = i.kind
            a['state'] = "审核中"
            retData.append(a)
    return HttpResponse(json.dumps(retData), content_type = 'application/json')
            

def myachieve(request):
    retData = []
    user_id = request.GET['user_id']
    scholar = scholar_tab.objects.filter(user_id = user_id)
    scholar_id = scholar[0].scholar_id
    print(scholar_id)
    achieve_tab = scholar_achievement_tab.objects.filter(scholar_id = scholar_id)
    if len(achieve_tab) == 0:
        return HttpResponse(json.dumps(retData), content_type = 'application/json')
    for i in achieve_tab:
        a_id = i.a_id
        achievement = achievement_tab.objects.get(a_id = a_id)
        a = {}
        a['name'] = achievement.name
        a['author'] = achievement.author_name
        a['a_id'] = achievement.a_id
        a['year'] = achievement.year
        retData.append(a)
    return HttpResponse(json.dumps(retData), content_type = 'application/json')
    
    
def achieveClaim(request):
    retData = []
    return HttpResponse(json.dumps(retData), content_type = 'application/json') 
    
    
    
def ShouldCerty(request):
    retData = {}
    user_id = request.GET['user_id']
    retData['ShouldCerty'] = 0
    user = user_tab.objects.filter(user_id = user_id)
    if len(user) != 0:
        authority = user[0].authority
        if authority == 0:
            author = user_authen_tab.objects.filter(user_id = user_id)
            if len(author) == 0:
                retData['ShouldCerty'] = 1
    return HttpResponse(json.dumps(retData), content_type = 'application/json')
