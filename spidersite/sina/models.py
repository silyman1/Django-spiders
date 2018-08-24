# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser,models.Model):
	user_register_time = models.DateTimeField('date to register',auto_now_add=True)	
	nickname = models.CharField(max_length=200,default='用户')
	last_seen = models.DateTimeField(auto_now_add=True)
	avatar = models.CharField(max_length=200,default='avatar-default.jpg')
	sina_username = models.CharField(max_length=200)
	sina_password = models.CharField(max_length=200)
class Following_Blogger(models.Model):
	following_name = models.CharField(max_length=200,)
	avatar = models.CharField(max_length=200,default='avatar-default.jpg')
	owner = models.ManyToManyField(User,related_name="owner")
	last_vist = models.DateTimeField(auto_now_add=True)
	brief = models.CharField(max_length=200,default='暂无')
	click_count = models.IntegerField(null=True,default=0)
	following_num = models.IntegerField(null=True,default=0)
	follower_num = models.IntegerField(null=True,default=0)