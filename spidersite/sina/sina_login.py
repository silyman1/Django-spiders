#-*-coding:utf-8-*-
import requests
import json
import PyV8
import re
import base64
import binascii
import random
import rsa
import urllib
import json
import pytesseract
from PIL import Image
# from bs4 import BeautifulSoup
import sys
from io import BytesIO
reload(sys)
sys.setdefaultencoding('utf-8')
class SinaLogin(object):
	def __init__(self):
		self.username = ''
		self.password =''
		self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
						'Referer':'https://login.sina.com.cn/signup/signin.php'}

		self.uid = 0
		self.session = requests.session()
		self.page_id_list = set()
		self.s = self.session.get('http://login.sina.com.cn',headers=self.headers)
		self.following_list = []
		if(self.s.status_code == 200):
			print 'init session successfully'
		self.get_vercode()
		self.code = ''
	def get_vercode(self):
		response = self.session.get('https://login.sina.com.cn/cgi/pin.php?r=3309065&s=0',headers=self.headers)
		image = Image.open(BytesIO(response.content))
		path = 'E:\\gitprojects\\django-spiders\\spidersite\\sina\\static\\images'
		image.save(path+'\pin.png')
		print 'get verifycode ok !!'
		pic_open = Image.open(path+'\pin.png','r')
		# code = self.convert(path,pic_open)
		# return code
	# def convert(self,pic_path,pic):
	# 	#先将图片进行灰度处理，也就是处理成单色，然后进行下一步单色对比
	# 	imgrey = pic.convert('L')
	# 	#去除图片噪点,170是经过多次调整后,去除噪点的最佳值
	# 	'''
	# 	其实就是对已处理的灰度图片,中被认为可能形成验证码字符的像素进行阀值设定,
	# 	如果阀值等于170,我就认为是形成验证码字符串的所需像素,然后将其添加进一个空table中,
	# 	最后通过im.point将使用table拼成一个新验证码图片
	# 	'''
	# 	threshold = 170
	# 	table = []
	# 	for i in range(256):
	# 		if i < threshold:
	# 			table.append(0)
	# 		else:
	# 			table.append(1)
	# 	#使用table（是上面生成好的）生成图片
	# 	out = imgrey.point(table,'1')
	# 	out.save(pic_path + '/' + 'cjb'+ str(threshold) + '.jpeg','jpeg')
	# 	#读取处理好的图片的路径
	# 	a = pic_path + '/' + 'cjb' + str(threshold) + '.jpeg'

	# 	img3 = Image.open(a,'r')
	# 	#将图片中的像素点识别成字符串（图片中的像素点如果没有处理好，
	# 	#可能在识别过程中会有误差，如多个字符少个字符，或者识别错误等）
	# 	vcode = pytesseract.image_to_string(img3)

	# 	print(vcode)#此句也是测试结果时使用的
	# 	return vcode#此句才是将被破解的验证码字符串返回给需要的代码的
	def getpostdata(self):
		pre_url = 'https://login.sina.com.cn/sso/prelogin.php?entry=account&callback=sinaSSOController.preloginCallBack&su=MTE2MTYyNjU5NyU0MHFxLmNvbQ%3D%3D&rsakt=mod&client=ssologin.js(v1.4.15)&_=1534126164960%20HTTP/1.1'
		response = self.session.get(pre_url)
		jsondata = re.findall(r'\((\{.*?\})\)',response.text)[0]
		data = json.loads(jsondata)
		try:
			servertime = data.get('servertime')#time.time()*1000
			nonce = data.get('nonce')
			pubkey = data.get('pubkey')
			rsakv = data.get('rsakv')
			return servertime,nonce,pubkey,rsakv
		except Exception:
			print 'getpostdata failed'
			raise Exception
	def encode_su(self):
		a = base64.b64encode(urllib.quote(self.username))
		b = base64.encodestring(urllib.quote(self.username))
		return base64.b64encode(urllib.quote(self.username))
	def encode_sp(self,pubkey,servertime,nonce):
		Pubkey = int(pubkey, 16)
		rsa_n = int('10001',16)
		rsakey = rsa.PublicKey(Pubkey, rsa_n) #创建公钥
		codeStr = str(servertime) + '\t' + str(nonce) + '\n' + str(self.password) #根据js拼接方式构造明文
		pwd = rsa.encrypt(codeStr,rsakey)  #使用rsa进行加密
		return binascii.hexlify(pwd)  #将加密信息转换为16进制。
	def login(self,username,password):
		self.username = str(username)
		self.password = str(password)
		servertime,nonce,pubkey,rsakv = self.getpostdata()
		prelt = random.randint(40, 100)
		su = self.encode_su()
		sp = self.encode_sp(pubkey, servertime, nonce)

		# print '#######################################'
		# print su
		# print sp

		# print servertime
		# print nonce
		# print rsakv
		# print prelt
		post_data = {
					'entry':'account',
					'gateway':'1',
					'from':'',
					'savestate':30,
					'useticket':0,
					'pagerefer':'',
					'vsnf':1,
					'door':self.code,
					'su':su,
					'service':'account',
					'servertime':servertime,
					'nonce':nonce,
					'pwencode':'rsa2',
					'rsakv':rsakv,
					'sp':sp,
					'sr':'1024*768',
					'encoding':'UTF-8',
					'cdult':3,
					'domain':'sina.com.cn',
					'prelt':prelt,
					'returntype':'TEXT'
        }
		response = self.session.post('https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)',data =post_data,allow_redirects=False)
		if response.status_code != 200:
			print 'login failed'
			response.raise_for_status()
		jsondata = json.loads(response.text)
		print jsondata
		print 'code:',self.code
		uid = jsondata.get('uid')
		url2 = jsondata.get('crossDomainUrlList')[0]
		self.uid = uid 
		#set cookie 
		s = self.session.get(url2)
	def get_homepage(self):
		home_url = 'https://weibo.com/u/{}/home?wvr=5'.format(str(self.uid))
		home_page = self.session.get(home_url).text
		return home_page
	def get_myfollow(self):
		home_page = self.get_homepage()
		pattern = re.compile(r'<fieldset>.*?href=\\"\\/p\\/(.*?)\\/myfollow',re.S)
		page_id = re.findall(pattern, home_page)[0]
		flag = True
		i =1
		while flag:

			page_url = 'https://weibo.com/p/{}/myfollow?t=1&cfs=&Pl_Official_RelationMyfollow__92_page={}#Pl_Official_RelationMyfollow__92'.format(str(page_id),str(i))
			home_page = self.session.get(page_url).text


			flag = self.parse_myfollow(home_page)
			i = i+1
		return self.following_list
	def parse_myfollow(self,html):
		# soup = BeautifulSoup(html,'lxml')
		# print soup.title

		# following_list = soup.find_all('div',attrs={"class":"title W_fb W_autocut"})
		pattern = re.compile(r'<div class=\\"title W_fb W_autocut \\".*?title=\\"(.*?)\\".*?>',re.S)
		pattern2 = re.compile(r'class=\\"pic_box\\".*?img src=\\"(.*?)"')
		following_list = re.findall(pattern, html)
		avator_list = re.findall(pattern2, html)
		if following_list:
			for item,avatar in zip(following_list,avator_list):
				print item
				avatar = 'https:' + str(avatar.replace('\\','')) 
				print avatar
				self.following_list.append((item,avatar)) 
				
			return True
		return False
	def get_others_homepage(self,uid):
		home_url = 'https://weibo.com/u/{}/home?wvr=5'.format(str(uid))
		home_page = self.session.get(home_url).text
		return home_page
	def get_unique_page_id(self,uid):
		print 'uid:',uid
		html = self.get_others_homepage(uid)
		# with open('ttt.txt','w+') as f:
		# 	f.write(html)
		pattern  = re.compile("CONFIG\[\'page_id\'\]=\'(\d+)\'",re.S)
		page_id = re.findall(pattern,html)[0]
		return page_id
	def get_myfollowers_page_id(self):
		print '+++++++++'
		home_page = self.get_homepage()
		pattern = re.compile(r'<fieldset>.*?href=\\"\\/p\\/(.*?)\\/myfollow',re.S)
		page_id = re.findall(pattern, home_page)[0]
		flag = True
		i =1
		requests.adapters.DEFAULT_RETRIES = 10
		page_id_list = []
		while flag:
			# f = open('sina%d.txt'%i,'w+')
			# __stdout__ = sys.stdout
			# sys.stdout = f
			page_url = 'https://weibo.com/p/{}/myfollow?t=1&cfs=&Pl_Official_RelationMyfollow__92_page={}#Pl_Official_RelationMyfollow__92'.format(str(page_id),str(i))
			print page_url
			home_page = self.session.get(page_url).text

			print '==========================='
			#print home_page.encode('gbk','ignore')
			# sys.stdout = __stdout__
			# f.close()
			uid_list = self.parse_myfollow_2(home_page)
			if uid_list == []:
				flag = False
				break;
			i = i+1
			for uid in uid_list:

				self.page_id_list.add(self.get_unique_page_id(uid))

		return self.page_id_list
			# return page_id_list
	def parse_myfollow_2(self,html):
		# soup = BeautifulSoup(html,'lxml')
		# print soup.title

		# following_list = soup.find_all('div',attrs={"class":"title W_fb W_autocut"})
		pattern = re.compile(r'<div class=\\"title W_fb W_autocut \\".*?title=\\"(.*?)\\"',re.S)
		following_list = re.findall(pattern, html)
		pattern2 = re.compile(r'<p class=\\"btn_bed\\">.*?&uid=(\d+)&sex',re.S)
		following_uid_list = re.findall(pattern2, html)

		if following_list:
			for item in following_list:
				print item
		return following_uid_list
if __name__ == "__main__":
	sinalogin = SinaLogin()
	sinalogin.login()
	sinalogin.get_myfollow()
	# print s.status_code,'3333333'
	# print s.text.decode('utf-8').encode('gbk','ignore')
	# print s.history

