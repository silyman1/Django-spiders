# -*- coding: utf-8 -*-
import MySQLdb
import time
import sys
from spidersite.settings import MYSQL_HOSTS,MYSQL_USER,MYSQL_PASSWORD,MYSQL_DB

class Sql(object):
	
	@classmethod	
	def connect_db(cls):
		db = MySQLdb.connect(host=MYSQL_HOSTS,user=MYSQL_USER,passwd=MYSQL_PASSWORD,db=MYSQL_DB,charset='utf8')
		cursor = db.cursor()
		return db,cursor

	@classmethod	
	def query_data_by_hot(cls,cursor,following_list):
		sql = "SELECT * FROM sina_tb WHERE author in (%s) ORDER BY heat_count DESC LIMIT 5 " % ','.join(['%s'] * len(following_list))
		cursor.execute(sql,following_list)
		results = cursor.fetchall()
		print results
		return results
	@classmethod	
	def query_data_by_click_num(cls,cursor,following_list):
		sql = "SELECT * FROM sina_tb WHERE author in (%s) ORDER BY click_count DESC LIMIT 5 " % ','.join(['%s'] * len(following_list))
		cursor.execute(sql,following_list)
		results = cursor.fetchall()
		print results
		return results
	@classmethod
	def close_db(cls,db):
		db.close()
		print 'close db !'