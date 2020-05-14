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
    # url(r'^check_sch_ach_authen/', views.check_sch_ach_authen),
    url(r'^check_schach_authen_details/(?P<id>\d+)$', views.check_one_sch_ach_authen),

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
    url(r'^student/$', views.student),
    url(r'^delete_student/(?P<id>\d+)$', views.del_student),
    url(r'^checkuser/$', views.check_all_user),
    url(r'^delete_user/(?P<id>\d+)$', views.delete_user),

    # 用户认证
    url(r'^authen_user/$', views.authen_user),
    url(r'^del_authen/(?P<authen_id>\d+)$', views.del_authen),
    url(r'^pass_authen/(?P<authen_id>\d+)$', views.pass_authen),
	

    #小程序用户
    url(r'^user_id_get', views.user_id_get),
    url(r'^wx_login', views.wx_register),
    url(r'^searchPaper', views.searchPaper),
    url(r'^collectPaper', views.collectPaper),
    url(r'^paperInitial', views.paperInitial),
    url(r'^searchTeacher', views.searchTeacher),
    url(r'^teacherInitial', view.teacherInitial),
    url(r'^chengguoup', view.chengguoup),
    url(r'^getCollection',view.getCollection),
    url(r'^Identification', view.Identification),
]
