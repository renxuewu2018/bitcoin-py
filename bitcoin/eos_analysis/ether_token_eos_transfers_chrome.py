
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: xwren
# @Email:  renxuewu@hotmail.com
# @Fd:  spider eos transfers data every day for test
# @Date:   2018-03-22 21:51:17
# @Last Modified by:   renxuewu
# @Last Modified time: 2018-03-27 17:33:02

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from bs4  import BeautifulSoup as bs
import time
import mysql.connector
import random
from datetime import date, datetime
from ether_token_eos_holders_top100 import token_holders_top100 as top100
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz


transfer_crawler = webdriver.Chrome()
wait = WebDriverWait(transfer_crawler, 15)

# 1. parser html and get transfers data
# 2. save parser data
def parser(url):
	transfer_crawler.get(url)
	# 
	element = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="PagingPanel"]/span/b[2]')))
	html =  transfer_crawler.page_source
	soup = bs(html,'lxml')
	trs = soup.find_all('tr')
	token_holders = []
	for tr in trs:
		if tr.th:
			continue
		else:
			tds = tr.find_all('td')
			TxHash = str(tds[0].string)
			transfertime = get_transfer_time(tds[1].find('span')['title'])
			distime = (transfertime - last_time).total_seconds()
			if distime < 0  :
				return False
			Fromaddress = str(tds[2].string)
			InOrOut = str(tds[3].find('span').string)
			Toaddress = str(tds[4].string)
			Quantity = str(tds[5].string).replace(',','')
			createtime = get_current_time()
			token_holders.append((TxHash,transfertime,Fromaddress,InOrOut,Toaddress,Quantity,createtime,'EOS','12'))
	save_transfer(token_holders)
	return True

# database
conn = mysql.connector.connect(
	user='root', password='imsbase', database='coin')
cursor = conn.cursor()

holder_sql = 'insert into token_transfers(TxHash,transfertime,Fromaddress,InOrOut,Toaddress,Quantity,createtime,tokenid,status)  values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'

# save tranfers data
def save_transfer(holders):
	cursor.executemany(holder_sql,holders)
	conn.commit()

isexit_sql = 'SELECT TxHash FROM token_transfers ORDER BY transfertime DESC'
# 判断数据是否已存储
txhash_list = []
def isExit():
	cursor.execute(isexit_sql)
	results = cursor.fetchall()
	for i in results:
		txhash_list.append(i[0])
		# print(i[0])

last_time = None
# 获取最近一次更新时间
def get_latestP_time():
	get_current_time_sql = 'SELECT transfertime FROM token_transfers ORDER BY transfertime DESC '
	cursor.execute(get_current_time_sql)
	results = cursor.fetchall()
	return results[0][0]

# 关闭数据库
def close_db():
	cursor.close()
	conn.close()
	transfer_crawler.close()

def get_current_time():
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def get_transfer_time(t):
	return datetime.strptime(t, '%b-%d-%Y %I:%M:%S %p')

def get_format_time(t):
	timeStruct = time.strptime(t, "%b-%d-%Y %I:%M:%S %p") 
	strTime = time.strftime("%Y-%m-%d %H:%M:%S", timeStruct) 
	return strTime

def main():
	isExit()
	root_url = 'https://etherscan.io/token/generic-tokentxns2?contractAddress=0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0&mode=&a=%s'
	for address in top100:
		url = (root_url) %(address)
		transfer_crawler.get(url)
		html =  transfer_crawler.page_source
		tree = etree.HTML(html)
		page_num = tree.xpath('//*[@id="PagingPanel"]/span/b[2]/text()')[0]
		for i in range(int(page_num)):
			page = i+1
			next_url = url + '&p=' + str(page)
			print(address,page)
			# parser(next_url)
			time.sleep(random.choice(range(1,2)))
			isexitstr = parser(next_url)
			if isexitstr:
				continue
			else:
				break

def run_job():
	tart = time.clock()
	last_time = get_latestP_time()
	main()
	end = time.clock()
	print('running time:%s seconds' %(end-start))

def job():
	print("开始执行...")
	timez = pytz.timezone('Asia/Shanghai')
	scheduler = BlockingScheduler(timezone=timez)
	scheduler.add_job(func=run_job, trigger='cron',hour ='*/4')
	scheduler.start()
			

if __name__ == '__main__':
	job()	