from django.conf.urls import url
import dm_demo.views as views

urlpatterns = [
    # url(r'^$', views.homepage),
    url(r'^$', views.login),
    url(r'^home/', views.homepage),
    url(r'^login/', views.login),
    url(r'^server/', views.homepage),

    # 新加的
    url(r'^checkachievement/', views.check_ach),
    url(r'^delete_one_ach/(?P<id>\d+)$', views.delete_one_ach),
    url(r'^edit_one_ach/(?P<id>\d+)$', views.edit_one_ach),
    url(r'^check_one_ach/(?P<id>\d+)$', views.check_one_ach),
    url(r'^addachievement/', views.add_achievement),

    url(r'^check_newach_authen/', views.check_newach_authen),
    url(r'^check_newauthen_details/(?P<id>\d+)$', views.check_one_newach_authen),
    url(r'^delete_newauthen/(?P<id>\d+)$', views.delete_one_newauthen),
    # url(r'^check_sch_ach_authen/', views.check_sch_ach_authen),
    url(r'^check_schach_authen_details/(?P<id>\d+)$', views.check_one_sch_ach_authen),
    url(r'^delete_schach_authen/(?P<id>\d+)$', views.delete_one_schach_authen),

    url(r'^checkdepartment/', views.check_department),
    url(r'^delete_one_dep/(?P<id>\d+)$', views.delete_one_dep),
    url(r'^edit_one_dep/(?P<id>\d+)$', views.edit_one_dep),
    url(r'^check_one_dep/(?P<id>\d+)$', views.check_one_dep),
    url(r'^adddepartment/', views.add_department),

    url(r'^checkreport/', views.check_report),
    url(r'^delete_one_report/(?P<id>\d+)$', views.delete_one_report),
    url(r'^check_one_report/(?P<id>\d+)$', views.check_one_report),

    # 用户相关
    url(r'^scholar/$', views.scholar),
    url(r'^delete_scholar/(?P<id>\d+)$', views.del_scholar),
    url(r'^edit_one_scholar/(?P<id>\d+)$', views.edit_one_scholar),
    url(r'^check_one_scholar/(?P<id>\d+)$', views.check_one_scholar),
    url(r'^student/$', views.student),
    url(r'^delete_student/(?P<id>\d+)$', views.del_student),
    url(r'^edit_one_student/(?P<id>\d+)$', views.edit_one_student),
    url(r'^check_one_student/(?P<id>\d+)$', views.check_one_student),
    url(r'^checkuser/$', views.check_all_user),
    url(r'^delete_user/(?P<id>\d+)$', views.delete_user),

    # 用户认证
    url(r'^authen_user/$', views.authen_user),
    url(r'^del_authen/(?P<authen_id>\d+)$', views.del_authen),
    url(r'^pass_authen/(?P<authen_id>\d+)$', views.pass_authen),
	
    # 成果学者相关
    url(r'^scholar_achiev/(?P<id>\d+)$', views.check_scholar_achievement),
    url(r'^achiev_scholar/(?P<id>\d+)$', views.check_achievement_scholar),
    url(r'^last_page/$', views.to_last_page),
    url(r'^department_scholar/(?P<id>\d+)$', views.check_department_scholar),


    #小程序用户
    url(r'code2key', view.code2key),
    url(r'paperyears', view.paperyears),
    url(r'paperInitial', view.paperInitial),
    url(r'AchievementDetail', view.AchievementDetail),
    url(r'ScholarDepartment', view.ScholarDepartment),
    url(r'scholarGet', view.scholarGet),
    url(r'ScholarDetail', view.ScholarDetail),
    url(r'StudentCerti', view.StudentCerti),
    url(r'faveAchievement', view.faveAchievement),
    url(r'faveScholar', view.faveScholar),
    url(r'getUserInfo', view.getUserInfo),
    url(r'StudentCerti', view.StudentCerti),
    url(r'show_log', view.show_log, name = "image"),
    url(r'getFavScholar', view.getFavScholar),
    url(r'getFavAchievement', view.getFavAchievement),
    url(r'ScholarCerti', view.ScholarCerti),
    url(r'AchievementSearch', view.AchievementSearch),
    url(r'ScholarSearch', view.ScholarSearch),
    url(r'WxReport', view.WxReport),
    url(r'GetDepartment', view.GetDepartment),
    url(r'getNotice', view.getNotice),
    url(r'getAllNotice', view.getAllNotice),
    url(r'achievePost', view.achievePost),
    url(r'getVerify', view.getVerify),
    url(r'myachieve', view.myachieve),
    url(r'achieveClaim', view.achieveClaim),
    url(r'show_department_image', view.show_department_image),
    url(r'ShouldCerty', view.ShouldCerty),
]
