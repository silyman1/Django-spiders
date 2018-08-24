# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import sql
import random
from .models import User,Following_Blogger
from django.utils import timezone
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
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
			page_id_list = sinalogin.get_myfollowers_page_id()
			for page_id in page_id_list:
				new_id = '107603' + page_id[6:]
				url = 'https://m.weibo.cn/api/container/getIndex?containerid='+ new_id + '&page=1'
				response = sinalogin.session.get(url)
				content = json.loads(response.text)
				weibo_info =content.get('data').get('cards')[0]
				following_blogger = Following_Blogger()
				following_blogger.following_name = weibo_info.get('mblog').get('user').get('screen_name')
				following_blogger.avatar =  weibo_info.get('mblog').get('user').get('profile_image_url')
				brief_tmp = ''
				if weibo_info.get('mblog').get('user').get('verified_reason'):
					brief_tmp = brief_tmp +  weibo_info.get('mblog').get('user').get('verified_reason') + '<br>'
				if weibo_info.get('mblog').get('user').get('description'):
					brief_tmp = brief_tmp +  weibo_info.get('mblog').get('user').get('description')	
				following_blogger.brief =brief_tmp
				following_blogger.following_num = weibo_info.get('mblog').get('user').get('follow_count')
				following_blogger.follower_num = weibo_info.get('mblog').get('user').get('followers_count')
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
	random_list =set()
	f_list = []
	hot_list = []
	comments_count_list = []
	attitudes_count_list = []
	following_list = request.user.owner.all()
	update_following(following_list,request)
	following_list = request.user.owner.all()
	fo = open('view.log','w+')
	__stdout__ = sys.stdout
	sys.stdout = fo
	for t in range(len(following_list)):
		i = random.randint(1, len(following_list)-1)
		random_list.add(following_list[i])
		if len(random_list)>=6:
			break
	print random_list
	for following in following_list:
		print following.following_name
		print following.avatar
		f_list.append(following.following_name.encode('utf-8'))
	db,cursor = sql.Sql.connect_db()
	hot_list_l = sql.Sql.query_data_by_hot(cursor,f_list)
	for hot in hot_list_l:
		item = {}
		print type(hot[3])
		item['author'] = hot[1].encode('utf-8')
		item['post'] = hot[3].strip().encode('utf-8')
		print item['post']
		item['post_detail'] = hot[4]
		item['post_time'] = hot[5]
		item['comments_count'] = hot[6]
		item['attitudes_count'] = hot[7]
		item['click_count'] = hot[10]
		hot_list.append(item)
	comments_count_list_l = sql.Sql.query_data_by_comments_count(cursor,f_list)
	for c in comments_count_list_l:
		item = {}
		item['author'] = c[1]
		item['post'] = c[3]
		item['post_detail'] = c[4]
		comments_count_list.append(item)
	attitudes_count_list_l = sql.Sql.query_data_by_attitudes_count(cursor,f_list)
	for c in attitudes_count_list_l:
		item = {}
		item['author'] = c[1]
		item['post'] = c[3]
		item['post_detail'] = c[4]
		attitudes_count_list.append(item)
	sql.Sql.close_db(db)
	sys.stdout = __stdout__ 
	return render(request,'sina/index.html',{'following_list':following_list,'random_list':random_list,'hot_list':hot_list,'comments_count_list':comments_count_list,'attitudes_count_list':attitudes_count_list})
def get_following_list(request):
	following_list = request.user.owner.all()
	return render(request,'sina/followinglist.html',{'following_list':following_list})
def update_following(following_list,request):
	sinalogin = SinaLogin()
	sinalogin.login(request.user.sina_username,request.user.sina_password)
	following_list2_l = sinalogin.get_myfollow()
	following_list2 = [f[0] for f in following_list2_l]
	following_list1 = [f.following_name for f in following_list]
	for item in following_list2_l:
		if item[0] not in following_list1:
				following_blogger = Following_Blogger()
				following_blogger.following_name = item[0]
				following_blogger.avatar = item[1]
				following_blogger.save()
				following_blogger.owner.add(request.user)
				following_blogger.save()
	for item in following_list:
		if item.following_name not in following_list2:
			item.delete()
