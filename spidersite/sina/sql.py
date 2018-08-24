# -*- coding: utf-8 -*-
import MySQLdb
import time
import sys
from spidersite.settings import MYSQL_HOSTS,MYSQL_USER,MYSQL_PASSWORD,MYSQL_DB

class Sql(object):
	
	@classmethod	
	def connect_db(cls):
		#这里连接的时候指定utf8会导致乱码
		db = MySQLdb.connect(host=MYSQL_HOSTS,user=MYSQL_USER,passwd=MYSQL_PASSWORD,db=MYSQL_DB)
		cursor = db.cursor()
		return db,cursor

	@classmethod	
	def query_data_by_hot(cls,cursor,following_list):
		sql = "SELECT * FROM sina_tb WHERE author in (%s) ORDER BY heat_count DESC LIMIT 5 " % ','.join(['%s'] * len(following_list))
		cursor.execute(sql,following_list)
		results = cursor.fetchall()
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
	def close_db(cls,db):
		db.close()
		print 'close db !'