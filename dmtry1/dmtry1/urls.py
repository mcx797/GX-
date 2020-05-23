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
    url(r'^delete_newauthen/(?P<id>\d+)$', dview.delete_one_newauthen),
    # url(r'^check_sch_ach_authen/', dview.check_sch_ach_authen),
    url(r'^check_schach_authen_details/(?P<id>\d+)$', dview.check_one_sch_ach_authen),
    url(r'^delete_schach_authen/(?P<id>\d+)$', dview.delete_one_schach_authen),

    url(r'^checkdepartment/', dview.check_department),
    url(r'^delete_one_dep/(?P<id>\d+)$', dview.delete_one_dep),
    url(r'^edit_one_dep/(?P<id>\d+)$', dview.edit_one_dep),
    url(r'^check_one_dep/(?P<id>\d+)$', dview.check_one_dep),
    url(r'^adddepartment/', dview.add_department),

    url(r'^checkreport/', dview.check_report),
    url(r'^delete_one_report/(?P<id>\d+)$', dview.delete_one_report),
    # url(r'^check_one_report/(?P<id>\d+)$', dview.check_one_report),

    # 用户相关
    url(r'^scholar/$', dview.scholar),
    url(r'^delete_scholar/(?P<id>\d+)$', dview.del_scholar),
    url(r'^edit_one_scholar/(?P<id>\d+)$', dview.edit_one_scholar),
    url(r'^check_one_scholar/(?P<id>\d+)$', dview.check_one_scholar),

    url(r'^student/$', dview.student),
    url(r'^delete_student/(?P<id>\d+)$', dview.del_student),
    url(r'^edit_one_student/(?P<id>\d+)$', dview.edit_one_student),
    url(r'^check_one_student/(?P<id>\d+)$', dview.check_one_student),
    url(r'^checkuser/$', dview.check_all_user),
    url(r'^delete_user/(?P<id>\d+)$', dview.delete_user),

    # 用户认证
    url(r'^authen_user/$',dview.authen_user),
    url(r'^check_auth_exist_user/$',dview.check_auth_exist_user),
    url(r'^del_authen/(?P<authen_id>\d+)$', dview.del_authen),
    url(r'^del_exist_scholar_authen/(?P<authen_id>\d+)$', dview.del_exist_scholar_authen),
    url(r'^pass_authen/(?P<authen_id>\d+)$', dview.pass_authen),
    url(r'^pass_exist_scholar_authen/(?P<authen_id>\d+)$', dview.pass_exist_scholar_authen),
    url(r'^authen_user_detail/(?P<id>\d+)', dview.authen_user_detail),
    url(r'^exist_user_auth_detail/(?P<authen_id>\d+)', dview.exist_user_auth_detail),

    # # 添加爬取结果
    # url(r'^add_get_achievement/$', dview.add_get_achievement),
    # url(r'^pass_new_achievement/(?P<id>\d+)$', dview.pass_new_achievement),
    # url(r'^del_new_achievement/(?P<id>\d+)$', dview.del_new_achievement),

    # 成果学者相关
    url(r'^scholar_achiev/(?P<id>\d+)$', dview.check_scholar_achievement),
    url(r'^achiev_scholar/(?P<id>\d+)$', dview.check_achievement_scholar),
    url(r'^last_page/$', dview.to_last_page),
    url(r'^department_scholar/(?P<id>\d+)$', dview.check_department_scholar),

    # 成果搜索
    url(r'^search_ach/', dview.search_ach),
    url(r'^change_search/', dview.change_search_ach),
    url(r'^check_search_ach/', dview.check_search_ach),

    # 成果认证细节相关
    url(r'^achauthen_scholar/(?P<id>\d+)$', dview.check_achauthen_scholar),

    # 公告发布相关
    url(r'^check_announce', dview.release_announce),
    url(r'^del_announce/(?P<id>\d+)$', dview.del_announce),

    # 举报相关
    url(r'^checkreport/', dview.check_report),
    url(r'^delete_one_report/(?P<id>\d+)$', dview.delete_one_report),
    url(r'^check_one_report/(?P<id>\d+)$', dview.add_pass_report),
    url(r'^report_detail/(?P<id>\d+)$', dview.show_report_detail),
    # url(r'^reject_report/(?P<id>\d+)$', dview.reject_report),

    url(r'^logout/', dview.logout),


    #  小程序相关
    url(r'^code2key', dview.code2key),
    url(r'^paperyears', dview.paperyears),
    url(r'paperInitial', dview.paperInitial),
    url(r'AchievementDetail', dview.AchievementDetail),
    url(r'ScholarDepartment', dview.ScholarDepartment),
    url(r'scholarGet', dview.scholarGet),
    url(r'ScholarDetail', dview.ScholarDetail),
    url(r'StudentCerti', dview.StudentCerti),
    url(r'faveAchievement', dview.faveAchievement),
    url(r'faveScholar', dview.faveScholar),
    url(r'getUserInfo', dview.getUserInfo),
    url(r'StudentCerti', dview.StudentCerti),
    url(r'show_log', dview.show_log, name = "image"),
    url(r'getFavScholar', dview.getFavScholar),
    url(r'getFavAchievement', dview.getFavAchievement),
    url(r'ScholarCerti', dview.ScholarCerti),
    url(r'AchievementSearch', dview.AchievementSearch),
    url(r'ScholarSearch', dview.ScholarSearch),
    url(r'WxReport', dview.WxReport),
    url(r'GetDepartment', dview.GetDepartment),
    url(r'getNotice', dview.getNotice),
    url(r'getAllNotice', dview.getAllNotice),
    url(r'achievePost', dview.achievePost),
]
