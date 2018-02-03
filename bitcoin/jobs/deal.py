#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: xwren
# @Email:  renxuewu@hotmail.com
# @Fd:获取火币交易信息
# @Date:   2018-01-11 21:57:11
# @Last Modified by:   xwren
# @Last Modified time: 2018-02-03 23:20:45


import requests
import headers
import json
import mysql.connector
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz,time


def get_deal():
	for i in range(1,2):
		# print(i)
		parse_deal_page(str(i))

# https://api-otc.huobi.pro/v1/otc/trade/list/public?coinId=1&tradeType=1&currPage=1  btb in
# https://api-otc.huobi.pro/v1/otc/trade/list/public?coinId=2&tradeType=1&currPage=1  usdt in

# https://api-otc.huobi.pro/v1/otc/trade/list/public?coinId=1&tradeType=0&currPage=1  btb out
# https://api-otc.huobi.pro/v1/otc/trade/list/public?coinId=2&tradeType=0&currPage=1  usdt out
def parse_deal_page(currpage):
	url = 'https://api-otc.huobi.pro/v1/otc/trade/list/public?coinId=2&tradeType=1&currPage='+str(currpage)
	doc = requests.get(url,headers=headers.get_random_header()).text
	data = json.loads(doc)
	if data['code'] == 200:
		print('data is coming...')
		totalPage = data['totalPage']
		currPage = data['currPage']
		if totalPage < currPage:
			return
		else:
			items = []
			for item in data['data']:
				items.append(tuple(item.values()))
			insert(items)
			parse_deal_page(currPage+1)
	else:
		print("no data error!")
		return

url_list = [
	'https://api-otc.huobi.pro/v1/otc/trade/list/public?coinId=1&tradeType=1&currPage=',
	'https://api-otc.huobi.pro/v1/otc/trade/list/public?coinId=1&tradeType=0&currPage=',
	'https://api-otc.huobi.pro/v1/otc/trade/list/public?coinId=2&tradeType=1&currPage=',
	'https://api-otc.huobi.pro/v1/otc/trade/list/public?coinId=2&tradeType=0&currPage='
]

def parse_deal_page_all(currpage,url_init):
	url = url_init+str(currpage)
	doc = requests.get(url,headers=headers.get_random_header()).text
	data = json.loads(doc)
	if data['code'] == 200:
		# print('data is coming...')
		totalPage = data['totalPage']
		currPage = data['currPage']
		if totalPage < currPage:
			return
		else:
			items = []
			for item in data['data']:
				lastTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
				item['createtime'] = lastTime
				items.append(tuple(item.values()))
			insert(items)
			parse_deal_page_all(currPage+1,url_init)
	else:
		print("no data error!")
		return

'''
	连接数据库
'''
conn = mysql.connector.connect(
	user='root', password='test', database='test')
cursor = conn.cursor()
insert_sql = 'insert into huobi_trade values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

def insert(datalist):
	num = cursor.executemany(insert_sql,datalist)
	print('插入了',str(cursor.rowcount),'条数据！')
	conn.commit()


def run_total_job():
	print("-----------------------------------------------------------")
	for url in url_list:
		parse_deal_page_all(1,url)

def job():
	print("开始执行...")
	timez = pytz.timezone('Asia/Shanghai')
	scheduler = BlockingScheduler(timezone=timez)
	scheduler.add_job(func=run_total_job, trigger='cron', minute ='*/10')
	scheduler.start()

if __name__ == '__main__':
	# run_total_job()
	job()
	# for i in url_list:
	# 	print(i)
