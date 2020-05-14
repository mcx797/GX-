"""dmtry1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from dm_demo import views as dview

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', dview.login),
    url(r'^hello/$', dview.hello),
    url(r'^msg/(?P<name>\w+)/(?P<age>\d+)$', dview.msg),
    url(r'^server/', dview.homepage),
    url(r'^login/', dview.login),
    url(r'^home/', dview.homepage),
    # 新加的
    url(r'^checkachievement/', dview.check_ach),
    url(r'^delete_one_ach/(?P<id>\d+)$', dview.delete_one_ach),
    url(r'^edit_one_ach/(?P<id>\d+)$', dview.edit_one_ach),
    url(r'^check_one_ach/(?P<id>\d+)$', dview.check_one_ach),
    url(r'^addachievement/', dview.add_achievement),

    url(r'^check_newach_authen/', dview.check_newach_authen),
    url(r'^check_newauthen_details/(?P<id>\d+)$', dview.check_one_newach_authen),
    # url(r'^check_sch_ach_authen/', dview.check_sch_ach_authen),
    url(r'^check_schach_authen_details/(?P<id>\d+)$', dview.check_one_sch_ach_authen),

    url(r'^checkdepartment/', dview.check_department),
    url(r'^delete_one_dep/(?P<id>\d+)$', dview.delete_one_dep),
    url(r'^edit_one_dep/(?P<id>\d+)$', dview.edit_one_dep),
    url(r'^check_one_dep/(?P<id>\d+)$', dview.check_one_dep),
    url(r'^adddepartment/', dview.add_department),

    url(r'^checkreport/', dview.check_report),
    url(r'^delete_one_report/(?P<id>\d+)$', dview.delete_one_report),
    url(r'^check_one_report/(?P<id>\d+)$', dview.check_one_report),

    # 用户相关
    url(r'^scholar/$', dview.scholar),
    url(r'^delete_scholar/(?P<id>\d+)$', dview.del_scholar),
    url(r'^student/$', dview.student),
    url(r'^delete_student/(?P<id>\d+)$', dview.del_student),
    url(r'^checkuser/$', dview.check_all_user),
    url(r'^delete_user/(?P<id>\d+)$', dview.delete_user),

    # 用户认证
    url(r'^authen_user/$',dview.authen_user),
    url(r'^del_authen/(?P<authen_id>\d+)$', dview.del_authen),
    url(r'^pass_authen/(?P<authen_id>\d+)$', dview.pass_authen),

    # # 添加爬取结果
    url(r'^add_get_achievement/$', dview.add_get_achievement),
    url(r'^pass_new_achievement/(?P<id>\d+)$', dview.pass_new_achievement),
    url(r'^del_new_achievement/(?P<id>\d+)$', dview.del_new_achievement),

    #  小程序相关
    url(r'^user_id_get/', dview.user_id_get),
    url(r'^wx_register/', dview.wx_register),
    url(r'^searchPaper/', dview.searchPaper),
    url(r'^collectPaper/', dview.collectPaper),
    url(r'^paperInitial/', dview.paperInitial),
    url(r'^teacherInitial/', dview.teacherInitial),
    url(r'^searchTeacher/', dview.searchTeacher),
    url(r'^chengguoup', dview.chengguoup),
    url(r'^getCollection', dview.getCollection),
    url(r'^Identification', dview.Identification),
]
