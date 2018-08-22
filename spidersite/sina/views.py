# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import sql
from .models import User,Following_Blogger
from django.utils import timezone

from sina_login import SinaLogin
# Create your views here.

def test(request):
	return HttpResponse("test by pzc 2018-8-17")
@csrf_exempt
def register_view(request):
	print '3333'
	if request.method == 'POST':
		username = request.POST['uname']
		password = request.POST['psw']
		nickname = request.POST['nickname']
		sina_username = request.POST['sina_user']
		sina_password = request.POST['sina_psw']
		user=User.objects.create_user(username=username,password=password,nickname=nickname,sina_username=sina_username,sina_password=sina_password)
		print "register:",user
		if user:
			user = authenticate(username=username,password=password)
			login(request,user)
			sinalogin = SinaLogin()
			sinalogin.login(sina_username,sina_password)
			following_list = sinalogin.get_myfollow()
			for item in following_list:
				following_blogger = Following_Blogger()
				following_blogger.following_name = item[0]
				following_blogger.avatar = item[1]
				following_blogger.save()
				following_blogger.owner.add(user)
				following_blogger.save()
			return redirect(reverse('sina:index'))
		else:
			return render_to_response('sina/register.html')

	else:
		return render_to_response('sina/register.html')
@csrf_exempt
def login_view(request):
	if request.method == 'POST':
		for key in request.POST:
			print key
		'''
		loginform = LoginForm(request.POST)
		if loginform.is_valid():
			username =loginform.cleaned_data['username']
			password =loginform.cleaned_data['password']
		'''
		username =request.POST['uname']
		password =request.POST['psw']
		user = authenticate(username=username,password=password)
		print 'user:',user
		if user:
			login(request,user)
			user.last_seen = timezone.now()
			user.save()
			print user.last_seen
			return redirect(reverse('sina:index'))
		return render_to_response('sina/login.html')
	else:
		return render_to_response('sina/login.html')
def logout_view(request):
	logout(request)
	return render_to_response('sina/login.html')
@login_required
def index(request):
	newest_list =[]
	f_list = []
	following_list = request.user.owner.all()
	for following in following_list:
		print following.following_name
		f_list.append(following.following_name)
	db,cursor = sql.Sql.connect_db()
	hot_list = sql.Sql.query_data_by_hot(cursor,f_list)
	click_rank_list = sql.Sql.query_data_by_click_num(cursor,f_list)
	sql.Sql.close_db(db)
	return render(request,'sina/index.html',{'following_list':following_list,'newest_list':newest_list,'hot_list':hot_list,'click_rank_list':click_rank_list})