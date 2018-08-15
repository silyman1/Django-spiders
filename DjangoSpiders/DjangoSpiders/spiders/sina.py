# -*- coding: utf-8 -*-
import scrapy 
from scrapy import Request
import json
from scrapy.spiders import Spider
from sina_login import SinaLogin
from spiders.items import SinaItem
import sys
class WeiboSpider(Spider):
	name = 'weibo1'
	allowded_domains =['weibo.com']
	def start_requests(self):
		url = 'https://m.weibo.cn/p/1005052803301701'
		head1 = 'https://m.weibo.cn/api/container/getIndex?containerid='
		url = head1 + url.replace('https://m.weibo.cn/p/','').replace('100505','107603')
		yield Request(url)
	def parse(self,response):
		item = WeiboItem()
		fo = open('weibo1.log','w')
		sys.stdout = fo
		content = json.loads(response.body)
		weibo_info =content.get('data').get('cards')

		rawurl = response.url
		print rawurl
		i =1
		for info in weibo_info:
			print '========',i,'========='
			i = i+1
			if info.get('mblog') and info.get('mblog').get('text'):
				title = info.get('mblog').get('text').encode('utf-8')
				secondurl = "https://m.weibo.cn/status/%s" % info["mblog"]["mid"]
				time_record = info.get('mblog')['created_at'].encode('utf-8')
				picture_urls = ''
				if info.get('mblog').get('page_info'):
					if info.get('mblog').get('page_info').get('media_info'):
						picture_urls =info.get('mblog').get('page_info').get('page_pic')['url']
					print picture_urls,'======================'
				if not picture_urls:
					if info.get('mblog').get('pics'):
						pics = map(lambda x:x.get('url'),info.get('mblog')['pics'])
						picture_urls = ','.join(pics)
			print '++++++++++'
			print title
			item['title'] = title
			print secondurl
			item['reviewurl'] = secondurl
			print time_record
			item['time_record'] = time_record
			print picture_urls
			yield item
			if rawurl.replace('https://m.weibo.cn/api/container/getIndex?containerid=1076032803301701',''):
				continue
			j = i+1
			nexturl =rawurl+'&page='+'%d'%j
			yield Request(nexturl)