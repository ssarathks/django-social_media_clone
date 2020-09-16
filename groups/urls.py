from django.conf.urls import url,include
from . import views

app_name = 'groups'

urlpatterns = [
    url(r'^$',views.GroupList.as_view(),name="group_list"),
    url(r'^create/',views.GroupCreate.as_view(),name="create"),
    url(r'^posts/in/(?P<slug>[-\w]+)/',views.GroupDetail.as_view(),name='single'),
    url(r'^join/(?P<slug>[-\w]+)/',views.JoinGroup.as_view(),name='join'),
    url(r'^leave/(?P<slug>[-\w]+)/',views.LeaveGroup.as_view(),name='leave'),

]