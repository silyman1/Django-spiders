# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import sql
# Create your views here.

def test(request):
	return HttpResponse("test by pzc 2018-8-17")
@csrf_exempt
def register_view(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		sina_username = request.POST['sina_username']
		sina_password = request.POST['sina_password']
		user=User.objects.create_user(username=username,password=password,email=email)
		print "register",user
		if user:
			user = authenticate(username=username,password=password)
			login(request,user)
			return redirect(reverse('sina:index'))
		else:
			return render_to_response('register.html')

	else:
		return render_to_response('register.html')
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
		return render_to_response('login.html')
	else:
		return render_to_response('login.html')
def logout_view(request):
	logout(request)
	return render_to_response('login.html')
@login_required
def index(request):

	following_list = request.user.owner.all()
	db,cursor = sql.Sql.connect_db()
	hot_list = sql.Sql.query_data_by_hot(cursor,following_list)
	click_rank_list = sql.Sql.query_data_by_click_num(cursor,following_list)
	sql.Sql.close_db(db)
	return render(request,'sina/index.html',{'newest_list':newest_list,'hot_list':hot_list,'click_rank_list':click_rank_list})