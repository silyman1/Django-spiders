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
# from bs4 import BeautifulSoup
import sys
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
		self.s = self.session.get('http://login.sina.com.cn',headers=self.headers)
		if(self.s.status_code == 200):
			print 'init session successfully'
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
	def login(self):
		self.username = '1161626597@qq.com'#raw_input("username:")
		self.password = 'pzc1161626597'#raw_input("password:")
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
		uid = jsondata.get('uid')
		url2 = jsondata.get('crossDomainUrlList')[0]
		self.uid = uid 
		#set cookie 
		s = self.session.get(url2)
		cookies = {}
		for item in s.cookies.items():
			cookies[item[0]] = item[1]
		print cookies
		print 'login successfully'
		return None
	def get_homepage(self):
		home_url = 'https://weibo.com/u/{}/home?wvr=5'.format(str(self.uid))
		home_page = self.session.get(home_url)
		for item in home_page.cookies.items():
			print item
		return home_page.text
	def get_others_homepage(self,uid):
		home_url = 'https://weibo.com/u/{}/home?wvr=5'.format(str(uid))
		home_page = self.session.get(home_url).text
		return home_page
	def get_unique_page_id(self,uid):
		print 'uid:',uid
		html = self.get_others_homepage(uid)
		with open('ttt.txt','w+') as f:
			f.write(html)
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
			f = open('sina%d.txt'%i,'w+')
			__stdout__ = sys.stdout
			sys.stdout = f
			page_url = 'https://weibo.com/p/{}/myfollow?t=1&cfs=&Pl_Official_RelationMyfollow__92_page={}#Pl_Official_RelationMyfollow__92'.format(str(page_id),str(i))
			print page_url
			home_page = self.session.get(page_url).text

			print '==========================='
			print home_page.encode('gbk','ignore')
			sys.stdout = __stdout__
			f.close()
			uid_list = self.parse_myfollow(home_page)
			if uid_list == []:
				print '88888888'
				flag = False
				break;
			i = i+1
			for uid in uid_list:

				yield self.get_unique_page_id(uid)


			# return page_id_list
	def parse_myfollow(self,html):
		# soup = BeautifulSoup(html,'lxml')
		# print soup.title

		# following_list = soup.find_all('div',attrs={"class":"title W_fb W_autocut"})
		pattern = re.compile(r'<div class=\\"title W_fb W_autocut \\".*?title=\\"(.*?)\\"',re.S)
		following_list = re.findall(pattern, html)
		pattern2 = re.compile(r'<p class=\\"btn_bed\\">.*?&uid=(\d+)&sex',re.S)
		following_uid_list = re.findall(pattern2, html)
		print following_list
		print following_uid_list
		if following_list:
			for item in following_list:
				print item
		return following_uid_list

if __name__ == "__main__":
	sinalogin = SinaLogin()
	sinalogin.login()
	page_id_list = sinalogin.get_myfollowers_page_id()
	for id in page_id_list:
		print type(id)
		new_id = '107603' + id[6:]
		print "yield:  ",new_id 
	home_url = 'https://weibo.com/u/{}/home?wvr=5'.format(str(sinalogin.uid))
	cookies = sinalogin.session.get(home_url).cookies
	for item in cookies.items():
		print item
	# print s.status_code,'3333333'
	# print s.text.decode('utf-8').encode('gbk','ignore')
	# print s.history

