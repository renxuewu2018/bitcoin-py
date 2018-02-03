#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: xwren
# @Email:  renxuewu@hotmail.com
# @Fd: 查询拉勾关于区块链的招聘信息
# @Date:   2018-01-13 23:14:26
# @Last Modified by:   xwren
# @Last Modified time: 2018-02-03 23:19:36

import headers
import requests
import json
from math import ceil
import time
import hashlib
import mysql.connector
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz

url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'

def get_body(page,keyword):
	body = {
		'first':'false',
		'pn':page,
		'kd':keyword

	}
	return body

def get_header():
	header =  headers.get_random_header()
	header['Referer'] = 'https://www.lagou.com/jobs/list_%E5%8C%BA%E5%9D%97%E9%93%BE?labelWords=&fromSearch=true&suginput='
	return header

proxies = {
  "http": "http://160.226.214.183:8080",# test
  "https": "http://160.226.214.183:8080",
}

def get_md5(s):
	s_encode = s.encode("utf-8")
	hash_md5=hashlib.md5(s_encode)
	return hash_md5.hexdigest()

insertintozhaopinsql = 'insert into lagou_blockchain values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
def save_zhaopin(data):
	datas = []
	for item in data:
		lastTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
		item['publishTime'] = lastTime
		datas.append((item['companyId'],item['companyFullName'],item['companyShortName'],item['city'],str(item['companyLabelList']),item['companySize'],
			item['publishTime'],item['education'],item['financeStage'],item['industryField'],item['jobNature'],item['positionAdvantage'],
			str(item['positionLables']),item['positionName'],item['salary'],item['secondType'],item['workYear'],item['createTime']
			))
	try:
		cursor1 = con.cursor()
		num = cursor1.executemany(insertintozhaopinsql,datas)
		con.commit()
		print(get_time(),"已存入"+str(cursor1.rowcount)+"条数据！")
	except:
		import traceback
		traceback.print_exc()
		con.rollback()
	finally:
		cursor1.close()
		# con.close()

def get_zhaopin(page,keyword):
	responsestr = requests.post(url,data=get_body(page,keyword),headers=get_header()).text
	responsesjson = json.loads(responsestr)
	result = responsesjson["content"]['positionResult']
	page_size = responsesjson["content"]['pageSize']
	current_page = responsesjson["content"]['pageNo']
	totalCount = result['totalCount']
	data = result['result']
	save_zhaopin(data)

	page_total = ceil(int(totalCount)/int(page_size))
	for i in range(page+1,page_total+1):
		time.sleep(20)
		repstr = requests.post(url,data=get_body(i,keyword),headers=get_header()).text
		repjson = json.loads(repstr)
		result_other = repjson["content"]['positionResult']['result']
		save_zhaopin(result_other)
import telnetlib
def verify_proxy_ip(ip,port):
	try:
		telnetlib.Telnet(ip, port, timeout=20)
	except Exception as e:
		return False
	else:
		return True

proxy_ip_url = 'http://pvt.daxiangdaili.com/ip/?tid=557861105519513&num=30000'
def get_proxy_ip(url):
	result = requests.get(url).text
	iplist = result.split('\r\n')
	ips = []
	for item in iplist:
		ip_port = item.split(":")
		ip = ip_port[0]
		port = ip_port[1]
		# print(ip,port)
		verify = verify_proxy_ip(ip,port)
		ips = []
		if(verify):
			ipmd5 = get_md5(ip+port)
			ips.append((ip,port,'1',get_time(),ipmd5))
			save_ip_port(ips)
	# save_ip_port(ips)

def get_time():
	lastTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
	return lastTime

'''
	连接数据库
'''
con = mysql.connector.connect(
	user='root', password='test', database='test')
cursor = con.cursor()
insert_sql = 'insert into proxy_ip(ip,port,status,createtime,ipportmd5) values(%s,%s,%s,%s,%s)'

def save_ip_port(data):
	try:
		num = cursor.executemany(insert_sql,data)
		con.commit()
		print(get_time(),"已存入"+str(cursor.rowcount)+"条数据！")
	except:
		import traceback
		traceback.print_exc()
		con.rollback()
	# finally:
	# 	cursor.close()
	# 	con.close()

def run_total_job():
	try:
		get_proxy_ip(proxy_ip_url)
	except Exception as e:
		get_proxy_ip(proxy_ip_url)
	
def job():
	print("开始执行...")
	timez = pytz.timezone('Asia/Shanghai')
	scheduler = BlockingScheduler(timezone=timez)
	scheduler.add_job(func=run_total_job, trigger='cron', minute ='*/10')
	scheduler.start()

if __name__ == '__main__':
	# get_zhaopin(1,'区块链')
	# get_proxy_ip(proxy_ip_url)
	job()