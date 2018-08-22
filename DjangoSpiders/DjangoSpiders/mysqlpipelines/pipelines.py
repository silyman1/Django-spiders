# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sql
from DjangoSpiders.items import SinaItem
import sys
import MySQLdb
class DjangospidersPipeline(object):
	def process_item(self, item, spider):
		if isinstance(item,SinaItem):
			author =  MySQLdb.escape_string(item['author'])
			author_brief =  MySQLdb.escape_string(item['author_brief'])
			post =  MySQLdb.escape_string(item['post'])
			post_detail =  MySQLdb.escape_string(item['post_detail'])
			post_time =  MySQLdb.escape_string(item['post_time'])
			comments_count =  item['comments_count']
			attitudes_count =  item['attitudes_count']
			heat_count = self.get_heat_count(int(item['comments_count']),int(item['attitudes_count']))
			itemid = MySQLdb.escape_string(item['itemid'])
			fo = open('sql.log','a+')
			__stdout__ = sys.stdout
			sys.stdout = fo
			sql.Sinadb.create_tb()
			sql.Sinadb.insert_db(author, author_brief, post, post_detail, post_time,comments_count,attitudes_count,heat_count,itemid)
			sys.stdout = __stdout__
		return item
	def get_heat_count(self,comments_count,attitudes_count):
		heat_count = comments_count*0.6+attitudes_count*0.4
		return heat_count
	@classmethod
	def process_page_id(cls,page_id,page_num):
		fo = open('pageid.log','a+')
		__stdout__ = sys.stdout
		sys.stdout = fo
		page_id = MySQLdb.escape_string(str(page_id))
		page_num =  int(page_num)
		sql.Sinadb.create_pageid_tb()	
		sql.Sinadb.insert_pageid_tb(page_id,page_num)
		sys.stdout = __stdout__
	@classmethod
	def get_page_num_by_pid(cls,page_id):
		fo = open('getpageid.log','a+')
		__stdout__ = sys.stdout
		sys.stdout = fo
		page_id = int(page_id)
		sql.Sinadb.create_pageid_tb()
		page_num = sql.Sinadb.get_page_num(page_id)
		sys.stdout = __stdout__
		return page_num