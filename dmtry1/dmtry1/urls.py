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
    1. Import the include() function: from django.urls import include, path/
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from dm_demo import views as dview
from django.contrib.auth.decorators import login_required
handler404=dview.page_not_found
handler500 = dview.page_not_found1

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', dview.login_dm),
    url(r'^hello/$', dview.hello),
    url(r'^msg/(?P<name>\w+)/(?P<age>\d+)$', dview.msg),
    url(r'^server/', login_required(dview.homepage)),
    url(r'^login/', dview.login_dm),
    url(r'^home/', login_required(dview.homepage)),
    # 新加的
    url(r'^checkachievement/', login_required(dview.check_ach)),
    url(r'^delete_one_ach/(?P<id>\d+)$', login_required(dview.delete_one_ach)),
    url(r'^edit_one_ach/(?P<id>\d+)$', login_required(dview.edit_one_ach)),
    url(r'^check_one_ach/(?P<id>\d+)$', login_required(dview.check_one_ach)),
    url(r'^addachievement/', login_required(dview.add_achievement)),

    url(r'^check_newach_authen/', login_required(dview.check_newach_authen)),
    url(r'^check_newauthen_details/(?P<id>\d+)$', login_required(dview.check_one_newach_authen)),
    url(r'^delete_newauthen/(?P<id>\d+)$', login_required(dview.delete_one_newauthen)),
    url(r'^pass_one_newach_authen/(?P<id>\d+)$', login_required(dview.pass_one_newach_authen)),
    # url(r'^check_sch_ach_authen/', dview.check_sch_ach_authen),
    url(r'^check_schach_authenmouetails/(?P<id>\d+)$', login_required(dview.check_one_sch_ach_authen)),
    url(r'^delete_schach_authen/(?P<id>\d+)$', login_required(dview.delete_one_schach_authen)),
    url(r'^pass_schach_authen/(?P<id>\d+)$', login_required(dview.pass_one_sch_ach_authen)),

    url(r'^checkdepartment/', login_required(dview.check_department)),
    url(r'^delete_one_dep/(?P<id>\d+)$', login_required(dview.delete_one_dep)),
    url(r'^edit_one_dep/(?P<id>\d+)$', login_required(dview.edit_one_dep)),
    url(r'^check_one_dep/(?P<id>\d+)$', login_required(dview.check_one_dep)),
    url(r'^adddepartment/', login_required(dview.add_department)),

    url(r'^checkreport/', login_required(dview.check_report)),
    url(r'^delete_one_report/(?P<id>\d+)$', login_required(dview.delete_one_report)),
    # url(r'^check_one_report/(?P<id>\d+)$', dview.check_one_report),

    # 用户相关
    url(r'^scholar/$', login_required(dview.scholar)),
    url(r'^delete_scholar/(?P<id>\d+)$', login_required(dview.del_scholar)),
    url(r'^edit_one_scholar/(?P<id>\d+)$', login_required(dview.edit_one_scholar)),
    url(r'^check_one_scholar/(?P<id>\d+)$', login_required(dview.check_one_scholar)),

    url(r'^student/$', login_required(dview.student)),
    url(r'^delete_student/(?P<id>\d+)$', login_required(dview.del_student)),
    url(r'^edit_one_student/(?P<id>\d+)$', login_required(dview.edit_one_student)),
    url(r'^check_one_student/(?P<id>\d+)$', login_required(dview.check_one_student)),
    url(r'^checkuser/$', login_required(dview.check_all_user)),
    url(r'^delete_user/(?P<id>\d+)$', login_required(dview.delete_user)),

    # 用户认证
    url(r'^authen_user/$', login_required(dview.authen_user)),
    url(r'^check_auth_exist_user/$', login_required(dview.check_auth_exist_user)),
    url(r'^del_authen/(?P<authen_id>\d+)$', login_required(dview.del_authen)),
    url(r'^del_exist_scholar_authen/(?P<authen_id>\d+)$', login_required(dview.del_exist_scholar_authen)),
    url(r'^pass_authen/(?P<authen_id>\d+)$', login_required(dview.pass_authen)),
    url(r'^pass_exist_scholar_authen/(?P<authen_id>\d+)$', login_required(dview.pass_exist_scholar_authen)),
    url(r'^authen_user_detail/(?P<id>\d+)', login_required(dview.authen_user_detail)),
    url(r'^exist_user_auth_detail/(?P<authen_id>\d+)', login_required(dview.exist_user_auth_detail)),

    # 成果学者相关
    url(r'^scholar_achiev/(?P<id>\d+)$', login_required(dview.check_scholar_achievement)),
    url(r'^achiev_scholar/(?P<id>\d+)$', login_required(dview.check_achievement_scholar)),
    url(r'^last_page/$', login_required(dview.to_last_page)),
    url(r'^department_scholar/(?P<id>\d+)$', login_required(dview.check_department_scholar)),

    url(r'^department_student/(?P<id>\d+)$', login_required(dview.check_department_student)),
    url(r'^student_achiev/(?P<id>\d+)$', login_required(dview.check_student_achievement)),
    url(r'^achiev_student/(?P<id>\d+)$', login_required(dview.check_achievement_student)),

    # 成果搜索
    url(r'^search_ach/', login_required(dview.search_ach)),
    url(r'^change_search/', login_required(dview.change_search_ach)),
    url(r'^check_search_ach/', login_required(dview.check_search_ach)),

    # 成果认证细节相关
    url(r'^achauthen_scholar/(?P<id>\d+)$', login_required(dview.check_achauthen_scholar)),

    # 公告发布相关
    url(r'^check_announce', login_required(dview.release_announce)),
    url(r'^del_announce/(?P<id>\d+)$', login_required(dview.del_announce)),

    # 举报相关
    url(r'^checkreport/', login_required(dview.check_report)),
    url(r'^delete_one_report/(?P<id>\d+)$', login_required(dview.delete_one_report)),
    url(r'^check_one_report/(?P<id>\d+)$', login_required(dview.add_pass_report)),
    url(r'^report_detail/(?P<id>\d+)$', login_required(dview.show_report_detail)),
    # url(r'^reject_report/(?P<id>\d+)$', dview.reject_report),

    url(r'^logout/', login_required(dview.logout_view)),

    # 学者成果查询
    url(r'^checkstuachievement/', login_required(dview.check_student_ach)),
    url(r'^delete_one_stu_ach/(?P<id>\d+)$', login_required(dview.delete_one_student_ach)),
    url(r'^check_one_stu_ach/(?P<id>\d+)$', login_required(dview.check_one_student_ach)),
    

    #  404
    
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
    url(r'getVerify', dview.getVerify),
    url(r'myachieve', dview.myachieve),
    url(r'achieveClaim', dview.achieveClaim),
    url(r'show_department_image', dview.show_department_image),
    url(r'ShouldCerty', dview.ShouldCerty),
]
