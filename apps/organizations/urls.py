from django.conf.urls import url
from django.urls import path

from apps.organizations.views import OrgView, AddAskView, OrgHomeView, OrgTeacherView, OrgCourseView, OrgDescView
from apps.organizations.views import TeacherListView, TeacherDetailView
#授课 ---子路由
urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name="list"),
    #我要学习 添加
    url(r'^add_ask/$', AddAskView.as_view(), name="add_ask"),
    url(r'^add_ask/$', AddAskView.as_view(), name="add_ask"),
    #正则匹配url
    url(r'^(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="home"),
    url(r'^(?P<org_id>\d+)/teacher/$', OrgTeacherView.as_view(), name="teacher"),
    url(r'^(?P<org_id>\d+)/course/$', OrgCourseView.as_view(), name="course"),
    url(r'^(?P<org_id>\d+)/desc/$', OrgDescView.as_view(), name="desc"),

    #讲师列表页
    url(r'^teachers/$', TeacherListView.as_view(), name="teachers"),
    url(r'^teachers/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),
    # path('<int:org_id>/', OrgHomeView.as_view(), name="home"),
]
