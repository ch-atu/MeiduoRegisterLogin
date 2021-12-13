from django.conf.urls import url
from django.urls import path

from .views import SmsCodeView

urlpatterns = [
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', SmsCodeView.as_view()),
]
