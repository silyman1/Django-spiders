# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^test/', views.test, name='test'),
    url(r'^index/', views.index, name='index'),
    url(r'^following_list/', views.get_following_list, name='following_list'),
]