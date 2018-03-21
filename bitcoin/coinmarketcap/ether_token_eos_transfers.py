#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: xwren
# @Email:  seektolive@gmail.com
# @Date:   2018-03-19 16:34:51
# @Last Modified by:   xwren
# @Last Modified time: 2018-03-19 17:15:16
import requests
from bs4  import BeautifulSoup as bs
import random

headers=[
	{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'},
	{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'},
	{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'},
	{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
]

token_txhash = []

def get_random_header():
	return random.choice(headers)

def token_transfers_spider(token_url,token_id):
	res = requests.get(token_url,headers=get_random_header()).text
	soup = bs(res,'lxml')
	trs = soup.find_all('tr')
	print(trs)
	token_transfers = []
	for tr in trs:
		if tr.th:
			continue
		else:
			tds = tr.find_all('td')
			td_txhash = tds[0]
			print(td_txhash)
	# 		if td_txhash in token_txhash:
	# 			continue
	# 		else:
	# 			age = tds[1].span
	# 			fromaddress = 
	# 			[]
	# 			token_transfer = (str(tds[0].string),str(tds[1].string),str(tds[2].string),
	# 				str(tds[3].string)[:-2],get_current_time(),'0',token_id,'')
	# 		token_transfers.append(token_holder)
	# save_token_holder(token_transfers)

def main():
	URL = 'https://etherscan.io/token/generic-tokentxns2?contractAddress=0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0&mode=&p=1'
	token_transfers_spider(URL,'EOS')

if __name__ == '__main__':
	main()