from django.conf.urls import url
from django.urls import path
from .views import UserView, CheckUsername, CheckMobile
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    # 注册用户
    url(r'^user/$', UserView.as_view()),
    # 用户名是否注册
    url(r'^username/(?P<username>\w{5,20})/count/$', CheckUsername.as_view()),
    # 手机号是否注册
    url(r'^mobile/(?P<mobile>1[3,9]\d{9})', CheckMobile.as_view()),
    # 用户登录
    url(r'^authorizations/$', obtain_jwt_token),

]
