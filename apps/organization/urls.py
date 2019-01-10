from django.conf.urls import url
from organization.views import *

urlpatterns = [
    #课程机构列表页
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    url(r'^course/(?P<org_id>\d+)/$', CourseView.as_view(), name="org_course"),
    url(r'^desc/(?P<org_id>\d+)/$', DescView.as_view(), name="org_desc"),
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),

    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),

]