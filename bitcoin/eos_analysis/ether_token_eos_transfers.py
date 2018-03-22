#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: xwren
# @Email:  seektolive@gmail.com
# @Date:   2018-03-19 16:34:51
# @Last Modified by:   xwren
# @Last Modified time: 2018-03-22 16:45:45
import requests
from lxml import etree
import random
from bs4  import BeautifulSoup as bs
import ether_token_eos_holders_top100 as token_top
import time,re
from  decimal import Decimal
from  decimal import getcontext
import mysql.connector

headers=[
	{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'},
	{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'},
	{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'},
	{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
]

token_holders_top50 = ['0xd0a6e6c54dbc68db5db3a091b171a77407ff7ccf']

def get_random_header():
	return random.choice(headers)

# step 3 
def parser(response):
	soup = bs(response,'lxml')
	trs = soup.find_all('tr')
	token_holders = []
	for tr in trs:
		if tr.th:
			continue
		else:
			tds = tr.find_all('td')

			TxHash = str(tds[0].string)
			transfertime = get_format_time(tds[1].find('span')['title'])
			Fromaddress = str(tds[2].string)
			InOrOut = str(tds[3].find('span').string)
			Toaddress = str(tds[4].string)
			Quantity = str(tds[5].string).replace(',','')
			createtime = get_current_time()
			token_holders.append((TxHash,transfertime,Fromaddress,InOrOut,Toaddress,Quantity,createtime,'EOS','0'))
	save_transfer(token_holders)

def get_current_time():
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def get_format_time(t):
	timeStruct = time.strptime(t, "%b-%d-%Y %I:%M:%S %p") 
	strTime = time.strftime("%Y-%m-%d %H:%M:%S", timeStruct) 
	return strTime

conn = mysql.connector.connect(
	user='root', password='imsbase', database='coin')
cursor = conn.cursor()

holder_sql = 'insert into token_transfers(TxHash,transfertime,Fromaddress,InOrOut,Toaddress,Quantity,createtime,tokenid,status)  values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
# step 4
def save_transfer(holders):
	cursor.executemany(holder_sql,holders)
	conn.commit()


# step 2
def next_page(token_url,token_id,current_page=0):
	try:
		response = requests.get(token_url,headers=get_random_header()).text
		parser(response)
		# tree = etree.HTML(response)
		# page_num = tree.xpath('//*[@id="PagingPanel"]/span/b[2]/text()')[0]
		# next_page_num = current_page+1
		# next_page_url = token_url+"&p="+str(current_page+1)
		# if page_num > current_page:
		# 	next_page(next_page_url,token_id,next_page_num)
		# else:
		# 	return 
	except Exception as e:
		print(e)
		return 
		# next_page(next_page_url,'EOS',current_page)


# try_times = 0
def loading(url):
	print(try_times+1)
	tree = etree.HTML(response)
	page_num = tree.xpath('//*[@id="PagingPanel"]/span/b[2]/text()')
	if page_num:
		return response
	else:
		time.sleep(4)
		return response
		# loading(url)

# step 1
EOS_URL = 'https://etherscan.io/token/generic-tokentxns2?contractAddress=0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0&mode='
def token_transfers_spider():
	for address in token_top.token_holders_top1:
		address_url = EOS_URL+'&a='+address
		for i in range(77):
			address_url = address_url +"&p=" +str(i+1)
			next_page(address_url,'EOS')
		
def main():
	URL = 'https://etherscan.io/token/generic-tokentxns2?contractAddress=0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0&mode=&a=0xf4b51b14b9ee30dc37ec970b50a486f37686e2a8'
	token_transfers_spider(URL,'EOS')
	# //*[@id="PagingPanel"]/span/b[2]/text()
test_url = 'https://etherscan.io/token/generic-tokentxns2?contractAddress=0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0&mode=&a='


if __name__ == '__main__':
	token_transfers_spider()
