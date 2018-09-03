# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^test/', views.test, name='test'),
    url(r'^index/', views.index, name='index'),
    url(r'^following_list/', views.get_following_list, name='following_list'),
    url(r'^sina_bloger/(?P<f_id>[0-9]+)/blogs', views.get_following_blogs, name='following_blogs'),    
    url(r'^query_all/ajax_blog',views.all_ajax_blog, name = 'all_ajax_blog'),
    url(r'^query_single/ajax_blog',views.single_ajax_blog, name = 'single_ajax_blog'), 
    url(r'^query_all/', views.query_all_blogs, name='query_all'),
    url(r'^about_me/', views.about_me, name='about_me'),
    url(r'^edit/', views.edit, name='edit'),
    url(r'^update_blogs/', views.update_blogs, name='update_blogs'),
]