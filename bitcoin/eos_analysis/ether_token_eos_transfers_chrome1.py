
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: xwren
# @Email:  renxuewu@hotmail.com
# @Fd:
# @Date:   2018-03-22 21:51:17
# @Last Modified by:   renxuewu
# @Last Modified time: 2018-03-23 16:20:34

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from bs4  import BeautifulSoup as bs
import time
import mysql.connector
import random

transfer_crawler = webdriver.Chrome()
wait = WebDriverWait(transfer_crawler, 15)

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
			transfertime = get_format_time(tds[1].find('span')['title'])
			Fromaddress = str(tds[2].string)
			InOrOut = str(tds[3].find('span').string)
			Toaddress = str(tds[4].string)
			Quantity = str(tds[5].string).replace(',','')
			createtime = get_current_time()
			print(TxHash,transfertime,Fromaddress,InOrOut,Toaddress,Quantity,createtime,'EOS','0')
			token_holders.append((TxHash,transfertime,Fromaddress,InOrOut,Toaddress,Quantity,createtime,'EOS','0'))
	save_transfer(token_holders)

conn = mysql.connector.connect(
	user='root', password='imsbase', database='coin')
cursor = conn.cursor()

holder_sql = 'insert into token_transfers(TxHash,transfertime,Fromaddress,InOrOut,Toaddress,Quantity,createtime,tokenid,status)  values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
# step 4
def save_transfer(holders):
	cursor.executemany(holder_sql,holders)
	conn.commit()

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

def main():
	url = 'https://etherscan.io/token/generic-tokentxns2?contractAddress=0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0&mode=&\
			a=0x236f9f97e0e62388479bf9e5ba4889e46b0273c3'
	transfer_crawler.get(url)
	html =  transfer_crawler.page_source
	tree = etree.HTML(html)
	page_num = tree.xpath('//*[@id="PagingPanel"]/span/b[2]/text()')[0]
	for i in range(int(page_num)):
		next_url = url + '&p=' + str(i+548)
		print(next_url)
		time.sleep(random.choice(range(1,3)))
		parser(next_url)

if __name__ == '__main__':
	main()
	close_db()