#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: xwren
# @Email:  renxuewu@hotmail.com
# @Fd: 随机获取请求头
# @Date:   2018-01-11 22:04:22
# @Last Modified by:   xwren
# @Last Modified time: 2018-02-03 23:19:52


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


def get_random_header():
	return random.choice(headers)

# test
if __name__ == '__main__':
	print(get_random_header())
