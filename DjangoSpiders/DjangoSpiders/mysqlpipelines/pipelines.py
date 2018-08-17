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
			itemid = MySQLdb.escape_string(item['itemid'])
			fo = open('sql.log','a+')
			__stdout__ = sys.stdout
			sys.stdout = fo
			sql.Sinadb.create_tb()
			sql.Sinadb.insert_db(author, author_brief, post, post_detail, post_time, itemid)
			sys.stdout = __stdout__
		return item
