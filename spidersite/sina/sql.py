# -*- coding: utf-8 -*-
import MySQLdb
import time
import sys
from spidersite.settings import MYSQL_HOSTS,MYSQL_USER,MYSQL_PASSWORD,MYSQL_DB

class Sql(object):
	@classmethod
	def create_tb(cls,cursor):
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
			`itemid` VARCHAR(255),
			`click_count` int)DEFAULT CHARSET=utf8;"""
		try:
			cursor.execute(sql)
		except MySQLdb.Error,e:
			print time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time())),'creating table failed...reason:',e
	@classmethod	
	def connect_db(cls):
		#这里连接的时候指定utf8会导致乱码
		db = MySQLdb.connect(host=MYSQL_HOSTS,user=MYSQL_USER,passwd=MYSQL_PASSWORD,db=MYSQL_DB)
		cursor = db.cursor()
		cls.create_tb(cursor)
		return db,cursor

	@classmethod	
	def query_data_by_hot(cls,cursor,following_list):
		sql = "SELECT * FROM sina_tb WHERE author in (%s) ORDER BY heat_count DESC LIMIT 5 " % ','.join(['%s'] * len(following_list))
		cursor.execute(sql,following_list)
		results = cursor.fetchall()
		if results !=():
			print 'results0:',results[0][0]
			print 'results1:',results[0][1]
			print 'results2:',results[0][3]
			print 'results6:',results[0][6]
			print 'results7:',results[0][7]
			print 'results8:',results[0][8]
		return results
	@classmethod	
	def query_data_by_click_num(cls,cursor,following_list):
		sql = "SELECT * FROM sina_tb WHERE author in (%s) ORDER BY click_count DESC LIMIT 5 " % ','.join(['%s'] * len(following_list))
		cursor.execute(sql,following_list)
		results = cursor.fetchall()
		return results
	@classmethod	
	def query_data_by_comments_count(cls,cursor,following_list):
		sql = "SELECT * FROM sina_tb WHERE author in (%s) ORDER BY comments_count DESC LIMIT 5 " % ','.join(['%s'] * len(following_list))
		cursor.execute(sql,following_list)
		results = cursor.fetchall()
		return results
	@classmethod	
	def query_data_by_attitudes_count(cls,cursor,following_list):
		sql = "SELECT * FROM sina_tb WHERE author in (%s) ORDER BY attitudes_count DESC LIMIT 5 " % ','.join(['%s'] * len(following_list))
		cursor.execute(sql,following_list)
		results = cursor.fetchall()
		return results
	@classmethod	
	def query_data_by_single(cls,cursor,following_name,offset,size):
		sql = "SELECT * FROM sina_tb WHERE author = '%s' LIMIT %d,%d " % (following_name,int(offset),int(size))
		print sql
		cursor.execute(sql)
		results = cursor.fetchall()
		return results
	@classmethod	
	def query_data_by_all(cls,cursor,offset,size,following_list): 
		sql = "SELECT * FROM sina_tb WHERE author in (%s) LIMIT %d,%d " %( ','.join(['%s'] * len(following_list)),int(offset),int(offset)+int(size)+1)
		# sql = "SELECT * FROM sina_tb WHERE `id` BETWEEN %d AND %d " % (int(offset),int(offset)+int(size)+1)

		print sql
		print '#######'
		cursor.execute(sql,following_list)
		results = cursor.fetchall()
		return results
	@classmethod
	def query_get_sum(cls,cursor,following_list):
		sql = "SELECT COUNT(*) FROM sina_tb WHERE author in (%s) " % ','.join(['%s'] * len(following_list))
		cursor.execute(sql,following_list)
		results = cursor.fetchall()
		print results
		return results
	@classmethod
	def close_db(cls,db):
		db.close()
		print 'close db !'