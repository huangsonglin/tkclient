#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2020/4/20 15:45'

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from LRedis import localRedis
import random
import json

class GetRedis(object):

	def __init__(self):
		self.r = localRedis

	@property
	def get_bid_product(self):
		product = random.choice(self.r.keys(pattern="APP_BID_INFO:*"))
		online_info = json.loads(list(self.r.hscan(product, count=1)[1].values())[0].decode())
		return online_info

	@property
	def get_delay_product(self):
		product = random.choice(self.r.keys(pattern="APP_DELAY_INFO:*"))
		online_info = json.loads(list(self.r.hscan(product, count=1)[1].values())[0].decode())
		return online_info

	@property
	def get_bid_auction(self):
		auctionId = random.choice(self.r.keys(pattern="BID_AUCTION_INFO:*"))
		auction_info = (self.r.hscan(auctionId, count=100)[1])
		return auction_info

	@property
	def get_delay_auction(self):
		auctionId = random.choice(self.r.keys(pattern="DELAY_AUCTION_INFO:*"))
		auction_info = (self.r.hscan(auctionId, count=100)[1])
		return auction_info

	@property
	def get_shop_product(self):
		product = random.choice(self.r.keys(pattern="SHOP_PRODUCT:*"))
		product_info = json.loads(localRedis.get(product))
		return product_info




