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
			`comments_count` int,
			`attitudes_count` int,
			`heat_count` int,
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
	def insert_db(cls,author,author_brief,post,post_detail,post_time,comments_count,attitudes_count,heat_count,itemid):
		results = cls.distinct_itemid(itemid)
		print results
		if results == ():
			sql = "INSERT INTO sina_tb(author,author_brief,post,post_detail,post_time,comments_count,attitudes_count,heat_count,itemid)VALUES ('%s','%s','%s','%s','%s','%d','%d','%d','%s')"%(author,author_brief,post,post_detail,post_time,comments_count,attitudes_count,heat_count,itemid)
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
		print 'results6:',results[0][6]
		print 'results7:',results[0][7]
		print 'results8:',results[0][8]
	@classmethod
	def create_pageid_tb(cls):
		sql = """CREATE TABLE IF NOT EXISTS pageid_tb(
			`id` int PRIMARY KEY AUTO_INCREMENT,
			`page_id` VARCHAR(255),
			`page_num` int DEFAULT 1)DEFAULT CHARSET=utf8;"""
		try:
			cursor.execute(sql)
		except MySQLdb.Error,e:
			print time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time())),'creating table failed...reason:',e
	@classmethod	
	def insert_pageid_tb(cls,page_id,page_num):
		sql1 = "SELECT 1 FROM pageid_tb WHERE page_id = '%s'" %page_id
		cursor.execute(sql1)
		results = cursor.fetchall()
		print results,page_id
		if results == ():
			sql2 = "INSERT INTO pageid_tb(page_id,page_num)VALUES('%s','%d')"%(page_id,page_num)
		else:
			sql2 ="UPDATE pageid_tb SET page_num='%d' WHERE page_id='%s'"%(page_num,page_id)

		try:
			result = cursor.execute(sql2)
			if result:
				print 'insert NO.%d page_id %s'%(db.insert_id(),page_id)
			else:
				print 'rolling back..................'
				db.rollback()
			db.commit()
		except MySQLdb.Error,e:
			print time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time())),'insert page_id error...reason:',e
	@classmethod	
	def get_page_num(cls,page_id):
		sql = "SELECT * FROM pageid_tb WHERE page_id = '%s'" %page_id
		cursor.execute(sql)
		results = cursor.fetchall()
		print results
		if results == ():
			return 1
		else:
			return results[0][2]
