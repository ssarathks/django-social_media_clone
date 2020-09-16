from django.conf.urls import url,include
from . import views

app_name = 'posts'

urlpatterns = [
    url(r'^$',views.PostList.as_view(),name="all"),
    url(r'^create/',views.CreatePost.as_view(),name="create"),
    url(r'^by/(?P<username>[-\w]+)/',views.UserPost.as_view(),name="for_user"),
    # url(r'^by/(?P<username>[-\w]+)/(?P<pk>[-\w]+)/',views.PostDetail.as_view(),name="single"),
    url(r'^post/(?P<pk>[-\w]+)/', views.PostDetail.as_view(),name="single"),
    url(r'^delete/(?P<pk>[-\w]+)/',views.DeletePost.as_view(),name="delete"),
    
]