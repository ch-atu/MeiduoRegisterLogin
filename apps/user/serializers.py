# standard
import re

# project
from .models import User

# third-part
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django_redis import get_redis_connection


class CreateUserSerializer(serializers.ModelSerializer):
    """注册序列化器"""
    # 需要序列化的字段: ['id', 'username', 'mobile', 'token']
    # 需要反序列化的字段: ['username', 'password', 'password2', 'mobile', 'sms_code', 'allow']
    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='验证码', write_only=True)
    allow = serializers.CharField(label='同意协议', write_only=True)  # 'true'
    token = serializers.CharField(label='token', read_only=True)

    class Meta:
        model = User  # 从User模型中映射序列化器字段
        fields = ['id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow', 'token']
        extra_kwargs = {  # 修改字段选项
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {  # 自定义校验出错后的错误信息提示
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    # 1.校验验证码格式
    def validate_mobile(self, value):
        """单独校验手机号"""
        if not re.match(r'1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式有误')
        return value

    # 2.校验是否勾选协议
    def validate_allow(self, value):
        """是否同意协议校验"""
        if value != 'true':
            raise serializers.ValidationError('请同意用户协议')
        return value

    # 3.校验密码是否相同
    # 4.校验验证码是否相同
    def validate(self, attrs):
        # 校验密码
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两个密码不一致')

        # 校验验证码
        redis_conn = get_redis_connection('verify_codes')
        mobile = attrs['mobile']
        # 向redis存储数据时都是以字条串进行存储的,取出来后都是bytes类型 [bytes]
        real_sms_code = redis_conn.get('sms_%s' % mobile)
        if real_sms_code is None or attrs['sms_code'] != real_sms_code.decode():
            raise serializers.ValidationError('验证码错误')

        return attrs

    # 5.创建用户
    def create(self, validated_data):
        # 1.把不需要存储的 password2, sms_code, allow 从字段中移除
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']
        # 2.把密码先取出来
        password = validated_data.pop('password')
        # 3。创建用户模型对象, 给模型中的 username和mobile属性赋值
        user = User(**validated_data)
        # 4.把密码加密后再赋值给user的password属性
        user.set_password(password)
        # 5.存储到数据库
        user.save()

        # 6.引用jwt中的叫jwt_payload_handler函数(生成payload)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # 7.函数引用 生成jwt
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # 8.根据user生成用户相关的载荷
        payload = jwt_payload_handler(user)
        # 9.传入载荷生成完整的jwt
        token = jwt_encode_handler(payload)

        user.token = token

        return user









