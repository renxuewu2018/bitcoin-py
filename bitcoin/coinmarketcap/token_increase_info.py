#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: xwren
# 采集以太坊token的增长信息包括:
# 1. 持币用户数（holder）和 交易量（tranfers）data from  https://etherscan.io (e.g., https://etherscan.io/token/0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0)
# 2. github活跃度信息（watch、fork、star、commits）  data from github，(e.g.,https://github.com/EOSIO/eos)
# 3. 社区增长量（facebook、twitter、telegram用户互动信息）data from https://www.facebook.com 、 https://twitter.com telegram
# 4. 媒体报道（新增文章数等）TODO  
# @Email:  seektolive@gmail.com
# @Date:   2018-03-21 14:49:10
# @Last Modified by:   xwren
# @Last Modified time: 2018-03-21 23:48:34

import requests
import headers
import re
from lxml import etree
import time
import mysql.connector
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz

# 持币用户（新增地址）
def holders_spider(spider_url):
	test_url = 'https://etherscan.io/token/0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0'
	response = requests.get(test_url,headers=headers.get_random_header()).text
	# parser token_holders
	token_holders = re.findall('(\d{1,20}) addresses',response)
	supply = re.findall('EOS \(\$(.*)',response)
	supply_num = supply[0].strip().replace(',','')[:-1]

	if len(token_holders) > 0:
		token_holders_num = token_holders[0]
	else:
		token_holders_num = 0
	print('token_holders:%s' %(token_holders_num))
	return token_holders_num,supply_num
# 交易量数据采集
def tranfers_spider(spider_url):
	test_url = 'https://etherscan.io/token/generic-tokentxns2?contractAddress=0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0'
	response = requests.get(test_url,headers=headers.get_random_header()).text
	transfers = re.findall('(\d{7,20}) events',response)
	if len(transfers) > 0:
		transfers_num = transfers[0]
	else:
		transfers_num = 0
	print('transfers:%s' %(transfers_num))
	return transfers_num
# github 活跃度采集
def github_liveness_spider():
	test_url = 'https://github.com/EOSIO/eos'
	response = requests.get(test_url,headers=headers.get_random_header()).text
	tree = etree.HTML(response)

	commits = tree.xpath('//span[@class="num text-emphasized"]')
	if len(commits) > 0:
		commits_num = int(commits[0].text.strip().replace(',',''))
	else:
		commits_num = 0
	print("commits_num:%s" %(commits_num))

	star = tree.xpath('//a[@class="social-count js-social-count"]')
	if len(star) > 0:
		star_num = int(star[0].text.strip().replace(',',''))
	else:
		star_num = 0
	print("star_num:%s" %(star_num))

	fork = tree.xpath('//a[@class="social-count"]')
	if len(fork) > 1:
		watch_num = int(fork[0].text.strip().replace(',',''))
		fork_num = int(fork[1].text.strip().replace(',',''))
	else:
		watch_num = 0
		fork_num = 0
	print("watch_num:%s" %(watch_num))
	print("fork_num:%s" %(fork_num))

	return watch_num,star_num,fork_num,commits_num

# 社区增长量（facebook）
def facebook_spider():
	test_url = 'https://www.facebook.com/pg/eosblockchain/community/?ref=page_internal'
	response = requests.get(test_url,headers=headers.get_random_header()).text
	tree = etree.HTML(response)
	facebook = tree.xpath('//div[@class="_3xom"]/text()')
	if len(facebook) >1:
		facebook_like_num = facebook[0].strip().replace(',','')
		facebook_followers_num = facebook[1].strip().replace(',','')
	else:
		facebook_like_num = 0
		facebook_followers_num = 0

	print("facebook_like_num:%s" %(facebook_like_num))
	print("facebook_followers_num:%s" %(facebook_followers_num))

	return facebook_like_num,facebook_followers_num

# 社区增长量（twitter）
def twitter_spider():
	test_url = 'https://twitter.com/eos_io'
	response = requests.get(test_url,headers=headers.get_random_header()).text
	tree = etree.HTML(response)
	twitter_tween = tree.xpath('//span[@class="ProfileNav-value"]/@data-count')
	if len(twitter_tween) >2:
		twitter_tween_num = twitter_tween[0]
		twitter_following_num = twitter_tween[1]
		twitter_followers_num = twitter_tween[2]
	else:
		twitter_tween_num = 0
		twitter_following_num = 0
		twitter_followers_num = 0

	print("twitter_tween_num:%s" %(twitter_tween_num))
	print("twitter_following_num:%s" %(twitter_following_num))
	print("twitter_followers_num:%s" %(twitter_followers_num))

	return twitter_tween_num,twitter_following_num,twitter_followers_num

# 电报数据
def telegram_spider():
	test_url = 'https://t.me/joinchat/AAAAAEQbOeucnaMWN0A9dQ'
	response = requests.get(test_url,headers=headers.get_random_header()).text
	# print(response)
	tree = etree.HTML(response)
	members = tree.xpath('//div[@class="tgme_page_extra"]')
	if len(members) > 0:
		members_num = int(members[0].text.strip().replace('members','').replace(' ',''))
	else:
		members_num = 0
	return members_num

def run_total_job():
	start = time.clock()
	token_id = 'EOS'
	token_holders,supply_num= holders_spider('')
	transfers = tranfers_spider("url")
	watch_num,star_num,fork_num,commits_num = github_liveness_spider()
	save_data((token_holders,transfers,watch_num,star_num,fork_num,commits_num,supply_num,token_id,get_time()))
	# 需要科学上网
	# telegram_spider()
	# twitter_spider()
	# facebook_spider()
	end = time.clock()
	print('running time:%s seconds' %(end-start))

con = mysql.connector.connect(
	user='root', password='rxw1118', database='spider')
cursor = con.cursor()
insert_sql = 'insert into token_increase_info(token_holders,transfers,github_watch,github_star,github_fork,github_commits,supply,token_id,createtime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'

def save_data(data):
	try:
		num = cursor.execute(insert_sql,data)
		con.commit()
		print(get_time(),"已存入"+str(cursor.rowcount)+"条数据！")
	except:
		import traceback
		traceback.print_exc()
		con.rollback()
	# finally:
	# 	cursor.close()
	# 	con.close()
def get_time():
	lastTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
	return lastTime

def job():
	print("开始执行...")
	timez = pytz.timezone('Asia/Shanghai')
	scheduler = BlockingScheduler(timezone=timez)
	scheduler.add_job(func=run_total_job, trigger='cron', hour ='*/1')
	scheduler.start()


if __name__ == '__main__':
	run_total_job()
	# job()
