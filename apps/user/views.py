# project
from django.shortcuts import render

# third-part
from rest_framework.generics import CreateAPIView
from .serializers import CreateUserSerializer


# Create your views here.


class UserView(CreateAPIView):
    """用户注册"""
    # 指定序列化器
    serializer_class = CreateUserSerializer
