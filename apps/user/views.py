# project
from django.shortcuts import render

# third-part
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CreateUserSerializer
from .models import User


# Create your views here.

# 用户注册
class UserView(CreateAPIView):
    """用户注册"""
    # 指定序列化器
    serializer_class = CreateUserSerializer


# 用户名是否注册
class CheckUsername(APIView):
    def get(self, request, username):
        # 查询用户名是否存在
        count = User.objects.filter(username=username).count()

        # 包装响应数据
        data = {
            'username': username,
            'count': count
        }

        return Response(data)


# 手机号是否注册
class CheckMobile(APIView):
    def get(self, request, mobile):
        # 查询手机号是否存在
        count = User.objects.filter(mobile=mobile).count()

        # 返回数据
        data = {
            'mobile': mobile,
            'count': count
        }

        return Response(data)

