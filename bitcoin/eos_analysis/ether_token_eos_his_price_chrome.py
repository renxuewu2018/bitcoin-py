
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: xwren
# @Email:  renxuewu@hotmail.com
# @Fd:  spider eos transfers data every day for test
# @Date:   2018-03-22 21:51:17
# @Last Modified by:   renxuewu
# @Last Modified time: 2018-03-27 00:30:21

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from bs4  import BeautifulSoup as bs
import time
import mysql.connector
import random
from ether_token_eos_holders_top100 import token_holders_top100 as top100

transfer_crawler = webdriver.Chrome()
wait = WebDriverWait(transfer_crawler, 15)

def parser(url,tokenid):
	transfer_crawler.get(url)
	# 
	# element = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="PagingPanel"]/span/b[2]')))
	html =  transfer_crawler.page_source
	soup = bs(html,'lxml')
	trs = soup.find_all('tr')
	token_holders = []
	for tr in trs:
		if tr.th:
			continue
		else:
			tds = tr.find_all('td')
			timestr = str(tds[0].string)
			kpirce = tds[1]['data-format-value']
			maxprice = tds[2]['data-format-value']
			minprice = tds[3]['data-format-value']
			lprice = tds[4]['data-format-value']
			volnum = tds[5]['data-format-value']
			marketcap = tds[6]['data-format-value']
			if marketcap == '-':
				marketcap = 0
			createtime = get_current_time()
			print(timestr,kpirce,maxprice,minprice,lprice,volnum,marketcap,createtime,tokenid)
			token_holders.append((timestr,kpirce,maxprice,minprice,lprice,volnum,marketcap,createtime,tokenid))
	save_transfer(token_holders)

conn = mysql.connector.connect(
	user='root', password='rxw1118', database='spider')
cursor = conn.cursor()

holder_sql = 'insert into coin_price(pricetime,kprice,maxprice,minprice,lprice,volnum,marketcapstr,createtime,tokenid)  values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
# step 4
def save_transfer(holders):
	cursor.executemany(holder_sql,holders)
	conn.commit()

isexit_sql = 'SELECT TxHash FROM token_transfers ORDER BY transfertime DESC'

# 关闭数据库
def close_db():
	cursor.close()
	conn.close()
	transfer_crawler.close()

def get_current_time():
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def get_format_time(t):
	timeStruct = time.strptime(t, "%b-%d-%Y %I:%M:%S %p") 
	strTime = time.strftime("%Y-%m-%d %H:%M:%S", timeStruct) 
	return strTime

def main(url,tokenid):
	parser(url,tokenid)
	
tokenid = [
	'bitcoin','ethereum','litecoin','ripple','bitcoin-cash','eos','cardano','stellar','neo',
	'iota','monero','dash','tron','nem','tether','ethereum-classic','vechain','qtum','icon','binance-coin',
	'lisk','omisego','bitcoin-gold','nano','zcash','digixdao','populous','bytom','aeternity','0x','gas','storm'
	]
			
url = 'https://coinmarketcap.com/zh/currencies/%s/historical-data/?start=20171201&end=20180326'
if __name__ == '__main__':
	start = time.clock()
	for token in tokenid:
		url1 = (url) %(token)
		main(url1,token)
		time.sleep(random.choice(range(1,4)))
		# print(url1)
	# 
	end = time.clock()
	print('running time:%s seconds' %(end-start))
	close_db()