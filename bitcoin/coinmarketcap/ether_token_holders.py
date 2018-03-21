#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: xwren
# 以太坊token 持有者数据采集
# @Email:  seektolive@gmail.com
# @Date:   2018-03-19 09:42:28
# @Last Modified by:   xwren
# @Last Modified time: 2018-03-19 20:42:47

import requests
from bs4  import BeautifulSoup as bs
from lxml import etree
import mysql.connector
import re
import time
from apscheduler.schedulers.blocking import BlockingScheduler

EOS_TOKEN_HOLDER_URL = 'https://etherscan.io/token/generic-tokenholders2?a=0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0&s=1E%2b27&p=1' 
EOS_TOKEN_HOLDER_URL1 = 'https://etherscan.io/token/generic-tokenholders2?a=0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0&s=1E%2b27' 
TOKEN_ID = 'EOS'

import random

headers=[
	{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'},
	{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'},
	{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'},
	{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
]


def get_random_header():
	return random.choice(headers)

def token_holders_spider(token_url,token_id):
	res = requests.get(token_url,headers=get_random_header()).text
	soup = bs(res,'lxml')
	trs = soup.find_all('tr')
	token_holders = []
	for tr in trs:
		if tr.th:
			continue
		else:
			tds = tr.find_all('td')
			token_holder = (str(tds[0].string),str(tds[1].string),str(tds[2].string),str(tds[3].string)[:-2],
				get_current_time(),'0',token_id,'')
			token_holders.append(token_holder)
	save_token_holder(token_holders)
'''
	获取数据采集时间
'''
def get_current_time():
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

conn = mysql.connector.connect(
	user='root', password='rxw1118', database='spider')
cursor = conn.cursor()
	
holder_sql = 'insert into token_holder(rank,Address,Quantity,Percentage,createtime,status,tokenid,addressname)  values(%s,%s,%s,%s,%s,%s,%s,%s)'
def save_token_holder(holders):
	cursor.executemany(holder_sql,holders)
	conn.commit()

# 关闭数据库
def close_db():
	cursor.close()
	conn.close()

def job():
	print("开始采集...")
	scheduler = BlockingScheduler()
	scheduler.add_job(func=spider, trigger='cron', hour ='*/1')
	scheduler.start()

def spider():
	html = requests.get(EOS_TOKEN_HOLDER_URL,headers=get_random_header()).text
	selector = etree.HTML(html)
	total_holders = selector.xpath('//*[@id="PagingPanel"]/span/b[2]/text()')
	pagenum = total_holders[0]
	for i in range(int(pagenum)):
		print('collect:'+str(i+889))
		url = EOS_TOKEN_HOLDER_URL1+'&p='+str(i+889)
		token_holders_spider(url,TOKEN_ID)
		time.sleep(random.choice(range(5,10)))

def main():
	start = time.clock()
	# job()
	spider()
	# close_db()
	# token_holders_spider(EOS_TOKEN_HOLDER_URL,'EOS')
	end = time.clock()
	print('running time:%s seconds' %(end-start))

if __name__ == '__main__':
	main()

# https://etherscan.io/token/generic-tokenholders2?a=0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0&s=1E%2b27&p=5
# https://etherscan.io/token/generic-tokenholders2?a=0xB8c77482e45F1F44dE1745F52C74426C631bDD52&s=1.97192382E%2b26&p=1