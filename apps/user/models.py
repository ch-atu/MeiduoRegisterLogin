from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    mobile = models.CharField(verbose_name='手机号', unique=True, max_length=11)
    email_active = models.BooleanField(verbose_name='邮箱激活状态', default=False)

    class Meta:
        db_table = 'User'
        verbose_name = '用户'
        verbose_name_plural = verbose_name













