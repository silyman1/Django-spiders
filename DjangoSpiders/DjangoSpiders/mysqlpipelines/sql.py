# -*- coding: utf-8 -*-
import MySQLdb
from DjangoSpiders.settings import *
import time
import sys
db = MySQLdb.connect(host=MYSQL_HOSTS,user=MYSQL_USER,passwd=MYSQL_PASSWORD,db=MYSQL_DB)
cursor = db.cursor()

class Sinadb(object):

	@classmethod
	def create_tb(cls):
		sql = """CREATE TABLE IF NOT EXISTS sina_tb(
			`id` int PRIMARY KEY AUTO_INCREMENT,
			`author` VARCHAR(255),
			`author_brief` TEXT,
			`post` TEXT,
			`post_detail` VARCHAR(255),
			`post_time` VARCHAR(255),
			`itemid` VARCHAR(255))DEFAULT CHARSET=utf8;"""
		try:
			cursor.execute(sql)
		except MySQLdb.Error,e:
			print time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time())),'creating table failed...reason:',e
	@classmethod
	def distinct_itemid(cls,itemid):
		sql = "SELECT 1 FROM sina_tb WHERE itemid = '%s'" %itemid
		cursor.execute(sql)
		results = cursor.fetchall()

		return results
	@classmethod
	def insert_db(cls,author,author_brief,post,post_detail,post_time,itemid):
		results = cls.distinct_itemid(itemid)
		print results
		if results == ():
			sql = "INSERT INTO sina_tb(author,author_brief,post,post_detail,post_time,itemid)VALUES ('%s','%s','%s','%s','%s','%s')"%(author,author_brief,post,post_detail,post_time,itemid)
			try:
				result = cursor.execute(sql)
				if result:
					print 'insert NO.%d data'%db.insert_id()
				else:
					print 'rolling back..................'
					db.rollback()
				db.commit()
				# if self.db.insert_id()>=200:
				# 	return 'stop'
				# else:
				# 	return 'continue'
			except MySQLdb.Error,e:
				print time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time())),'insert data error...reason:',e
		else:
			print 'this item already exists ...'

			
		sql2 = "SELECT * FROM sina_tb WHERE itemid = '%s'"%itemid
		cursor.execute(sql2)
		results = cursor.fetchall()
		print 'results0:',results[0][0]
		print 'results1:',results[0][1]
		print 'results2:',results[0][2]
