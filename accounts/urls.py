from django.conf.urls import url
from django.contrib.auth import views as authViews
from . import views


app_name = 'accounts'

urlpatterns = [
    url(r'^signup/$',views.SignUp.as_view(),name="signup"),
    url(r'^login/$',authViews.LoginView.as_view(template_name='accounts/login.html'),name="login"),
    url(r'^logout/$',authViews.LogoutView.as_view(),name="logout"),
]
