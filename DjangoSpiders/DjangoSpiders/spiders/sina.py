# -*- coding: utf-8 -*-
import scrapy 
from scrapy import Request
import json
import re
from scrapy.spiders import Spider
from sina_login import SinaLogin
from DjangoSpiders.items import SinaItem
from DjangoSpiders.mysqlpipelines import pipelines
import sys
class SinaSpider(Spider):
	def __init__(self):
		self.cookies = {}
		self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
						}
		self.error_url = set()
	name = 'sina_following'
	allowded_domains =['weibo.com']
	def get_pageid_list(self):
		sinalogin = SinaLogin()
		self.cookies = sinalogin.login()
		page_id_list = sinalogin.get_myfollowers_page_id()
		return page_id_list
	def start_requests(self):
		for page_id in self.get_pageid_list():
			print '@@@@@@',page_id
			new_id = '107603' + page_id[6:]
			page_num = pipelines.DjangospidersPipeline.get_page_num_by_pid(new_id)
			url = 'https://m.weibo.cn/api/container/getIndex?containerid='+ new_id + '&page='+str(page_num)
			yield Request(url,cookies =self.cookies,headers =self.headers )
	def parse(self,response):
		item = SinaItem()
		content = json.loads(response.body)
		status = content.get('ok')

		fo = open('sina.log','a+')
		__stdout__ = sys.stdout
		sys.stdout = fo
		rawurl = response.url
		print '###############'
		print rawurl
		print status

		if status == 1:
			weibo_info =content.get('data').get('cards')
			print '11111'
			for info in weibo_info:
				try:
					brief_tmp = ''
					item['itemid'] = info.get('itemid')
					item['author'] = info.get('mblog').get('user').get('screen_name')
					print item['author']
					item['post_detail'] = info.get('scheme')
					item['post_time'] = info.get('mblog').get('created_at')
					item['comments_count'] = info.get('mblog').get('comments_count')	
					item['attitudes_count'] = info.get('mblog').get('attitudes_count')
					print '#############',item['comments_count'],item['attitudes_count']				
					if info.get('mblog').get('user').get('verified_reason'):
						brief_tmp = brief_tmp +  info.get('mblog').get('user').get('verified_reason') + '<br>'
					if info.get('mblog').get('user').get('description'):
						brief_tmp = brief_tmp +  info.get('mblog').get('user').get('description')	
					item['author_brief'] = brief_tmp

					if info.get('mblog').get('text'):
						item['post'] = 	info.get('mblog').get('text')	
					else:
						item['post'] = '' 
					print item['post'].encode('utf-8')
				except Exception:
					self.error_url.add(rawurl)
					print 'error_list:',self.error_url
					raise Exception
				yield item 

			num = re.findall(r'&page=(\d+)',rawurl)[0]
			pid = re.findall(r'containerid=(\d+)',rawurl)[0]
			print pid
			pipelines.DjangospidersPipeline.process_page_id(pid,num)
			new_num = int(num)+1
			nexturl = rawurl.replace('&page='+num,'&page='+str(new_num))
			print '%%%%%%%%%%%%%%%%%%%'
			print nexturl
			fo.close()
			sys.stdout = __stdout__
			yield Request(nexturl,cookies =self.cookies)
		# for info in weibo_info:
		# 	print '========',i,'========='
		# 	i = i+1
		# 	if info.get('mblog') and info.get('mblog').get('text'):
		# 		title = info.get('mblog').get('text').encode('utf-8')
		# 		secondurl = "https://m.weibo.cn/status/%s" % info["mblog"]["mid"]
		# 		time_record = info.get('mblog')['created_at'].encode('utf-8')
		# 		picture_urls = ''
		# 		if info.get('mblog').get('page_info'):
		# 			if info.get('mblog').get('page_info').get('media_info'):
		# 				picture_urls =info.get('mblog').get('page_info').get('page_pic')['url']
		# 			print picture_urls,'======================'
		# 		if not picture_urls:
		# 			if info.get('mblog').get('pics'):
		# 				pics = map(lambda x:x.get('url'),info.get('mblog')['pics'])
		# 				picture_urls = ','.join(pics)
		# 	print '++++++++++'
		# 	print title
		# 	item['title'] = title
		# 	print secondurl
		# 	item['reviewurl'] = secondurl
		# 	print time_record
		# 	item['time_record'] = time_record
		# 	print picture_urls
		# 	yield item
		# 	if rawurl.replace('https://m.weibo.cn/api/container/getIndex?containerid=1076032803301701',''):
		# 		continue
		# 	j = i+1
		# 	nexturl =rawurl+'&page='+'%d'%j
		# yield Request(nexturl)