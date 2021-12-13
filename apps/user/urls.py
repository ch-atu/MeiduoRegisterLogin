from django.conf.urls import url
from django.urls import path
from .views import UserView


urlpatterns = [
    url(r'^users/$', UserView.as_view())
]
