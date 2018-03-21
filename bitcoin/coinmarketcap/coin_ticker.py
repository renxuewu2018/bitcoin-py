#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: xwren
# @Email:  renxuewu@hotmail.com
# @Fd:   数字货币24小时交易量
# @Date:   2018-03-17 10:34:49
# @Last Modified by:   xwren
# @Last Modified time: 2018-03-17 16:28:27

import requests
import mysql.connector
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz
import json
import time
'''
random get headers 

'''

import random

headers=[
	{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'},
	{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'},
	{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'},
	{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
]

ROOT_URL = 'https://api.coinmarketcap.com'


def get_random_header():
	return random.choice(headers)

def get_ticker():
	TRICKER_RESOURCE = '/v1/ticker/?convert=CNY&limit=0'
	repos = requests.get(ROOT_URL+TRICKER_RESOURCE).text
	data = json.loads(repos)
	# print(repos)
	sava(data)

'''
	连接数据库
'''
con = mysql.connector.connect(
	user='root', password='rxw1118', database='spider')
insert_sql = 'insert into coin_cap(COIN_ID,name,symbol,rank,price_usd,price_btc,24h_volume_usd,\
	market_cap_usd,available_supply,total_supply,max_supply,percent_change_1h,percent_change_24h,\
	percent_change_7d,create_times,last_updated,price_cny,24h_volume_cny,market_cap_cny) \
	values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

def sava(data):
	datas = []
	for item in data:
		lastTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
		item['create_times'] = lastTime
		last_updated = item['last_updated']
		print(last_updated)
		if last_updated:
			item['last_updated'] = get_datatime(int(last_updated))
		else:
			item['last_updated'] = "null"
		datas.append((item['id'],item['name'],item['symbol'],item['rank'],item['price_usd'],
			item['price_btc'],item['24h_volume_usd'],item['market_cap_usd'],item['available_supply'],item['total_supply'],item['max_supply'],
			item['percent_change_1h'],item['percent_change_24h'],item['percent_change_7d'],item['create_times'],item['last_updated'],
			item['price_cny'],item['24h_volume_cny'],item['market_cap_cny']
			))
	try:

		cursor1 = con.cursor()
		num = cursor1.executemany(insert_sql,datas)
		con.commit()
		print(get_time(),"已存入"+str(cursor1.rowcount)+"条数据！")
	except:
		import traceback
		traceback.print_exc()
		con.rollback()
	finally:
		cursor1.close()
		# con.close()
def get_time():
	lastTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
	return lastTime

def get_datatime(times):
	lasttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(times))
	return lasttime

def job():
	print("开始执行...")
	timez = pytz.timezone('Asia/Shanghai')
	scheduler = BlockingScheduler(timezone=timez)
	scheduler.add_job(func=get_ticker, trigger='cron', minute ='*/10')
	scheduler.start()

def main():
	job()
	# get_ticker()
	# get_datatime(1520655560)

if __name__ == '__main__':
	main()