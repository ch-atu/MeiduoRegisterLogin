import re
import datetime

from .models import User
from django.contrib.auth.backends import ModelBackend


# 通过传入的账号动态获取user 模型对象
def get_user_by_account(account):
    """
    通过传入的账号动态获取user 模型对象
    :param account:  有可以是手机号,有可能是用户名
    :return:  user或None
    """
    try:
        if re.match(r'1[3-9]\d{9}$', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None  # 如果没有查到返回None
    else:
        return user  # 注意不要写在模型类


# 修改Django的认证类,为了实现多账号登录
class UsernameMobileAuthBackend(ModelBackend):
    """修改Django的认证类,为了实现多账号登录"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        # 获取到user
        user = get_user_by_account(username)

        # 判断当前前端传入的密码是否正确
        if user and user.check_password(password):
            # 记录登录时间
            user.last_login = datetime.datetime.now()
            user.save()
            # 返回user
            return user


# 重写JWT登录视图的构造响应数据函数,多追加 user_id和username
def jwt_response_payload_handler(token, user=None, request=None):
    """重写JWT登录视图的构造响应数据函数,多追加 user_id和username"""
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }















