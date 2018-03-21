#!/usr/bin/env python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'seektolive@gmail.com'
__date__="2017.04.19 15:59"
__project__='network_promotion'
__version__='v1.0.0'

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
