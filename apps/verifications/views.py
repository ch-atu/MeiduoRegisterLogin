# standard
import random

# project
from django.shortcuts import render

# third-party
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_redis import get_redis_connection


# Create your views here.


# GET: sms_codes/(?P<mobile>1[3-9]\d{9})/
class SmsCodeView(APIView):
    def get(self, request, mobile):
        """短信验证码"""
        # 1. 创建redis连接对象
        redis_conn = get_redis_connection('verify_codes')

        # 2.先从redis获取发送标记
        send_flag = redis_conn.get('send_flag_%s' % mobile)

        # 3.如果取到了标记,说明此手机号频繁发短信
        if send_flag:
            return Response({'message': '手机频繁发送短信'}, status=status.HTTP_400_BAD_REQUEST)

        # 4.生成验证码
        sms_code = '%06d' % random.randint(0, 999999)

        #  创建redis管道:(把多次redis操作装入管道中,将来一次性去执行,减少redis连接操作)
        pl = redis_conn.pipeline()

        # 5. 把验证码存储到redis数据库
        pl.setex('sms_%s' % mobile, 300, sms_code)

        # 6. 存储一个标记,表示此手机号已发送过短信 标记有效期60s
        pl.setex('send_flag_%s' % mobile, 60, 1)

        # 执行管道
        pl.execute()

        # 7. 利用容联云通讯发送短信验证码
        # send_sms_code.delay(mobile, sms_code)  # 触发异步任务

        # 8. 响应
        return Response({'message': 'ok'})













