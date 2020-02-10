#!user/bin/python
# -*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2020/1/10 17:33'

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import requests
import json
import hashlib
import random



class HTTPAPI:

	def __init__(self):
		f = open(os.path.join(rootPath, "config.js") , encoding="utf-8", errors='ignore')
		config = json.load(f)
		config = config[0]
		self.host = config["host"]
		self.headers = config["headers"]

	def login(self, username, password):
		hl = hashlib.md5()
		# 此处必须声明encode
		# 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
		hl.update(str(password).encode(encoding='utf-8'))
		pw = (hl.hexdigest())
		data = {"phoneNum": username, "pwd": pw}
		url = self.host + 'interface/mobile/pmall/loginByPhone_220'
		req = requests.post(url, data=data, headers=self.headers)
		return req

	# 添加轰啪拍品
	def addOfficeMyAppProduct_270(self, Authorization, name, beginPrice, bidInc, marketPrice, planTime, ptype,
								  icon, desc, video=None, videoImage=None):
		"""
		:param username:  会员账号
		:param password:  登陆密码
		:param beginPrice:  起拍价
		:param bidInc:  加价幅度
		:param desc:    拍场描述
		:param marketPrice:  市场估价
		:param name:    拍品名字
		:param planTime:    计划开始时间
		:param type:    拍品类型
		:param images:  拍品封面图
		:param video:   视频
		:param videoImage:  视频图片
		:return:
		"""
		url = self.host + 'interface/mobile/addMyAppProduct_270'
		data = {'beginPrice': beginPrice, 'bidInc': bidInc, 'desc': desc, 'marketPrice': marketPrice, 'name': name,
				'planTime': planTime, 'type': ptype, 'images': icon, 'video': video, 'videoImage': videoImage}
		self.headers.update(Authorization=Authorization)
		req = requests.post(url, data=data, headers=self.headers)
		return req

	# 添加轰啪拍场
	def addMyAppOfficeAuction_240(self, icon, name, startTime, productIds, desc):
		"""
		:param username: 会员账号
		:param password: 会员密码
		:param apprState: W: 提交审核/待审核，D：保存  P:审核通过  F:审核不通过
		:param icon: 拍场图片
		:param name: 拍场名称
		:param keyword: 拍场关键字
		:param auctionType: 拍场类型
		:param startTime:   开始时间
		:param productIds:  产品List
		:param desc:    拍场描述
		:return:
		"""
		url = self.host + 'interface/mobile/addMyAppAuction_240'
		auctionType = Mysql().reslut_replace('SELECT `key` FROM param WHERE type ="AUCTION_TYPE" order by rand() limit 1')
		keyword = "测试  轰啪  藏传"
		data = {'icon': icon, 'name': name, 'keyword': keyword, 'startTime': startTime, 'productIds': productIds,
				'desc': desc, 'apprState': "W", 'auctionType': auctionType, "perActionDelay": "A_I_01",
				"preEnter": "A_P_09"}
		self.headers.update(Authorization=Authorization)
		req = requests.post(url, data=data, headers=self.headers)
		return req

	# 添加秒啪拍品
	def addMyOfficeDelayAucProduct_420(self, name, desc, images, video=None,
									   videoImage=None, bigImages=None):
		beginPrice = random.randrange(0, 1000, 100)
		bidIncValue = random.randrange(100, 1000, 100)
		marketPriceValue = random.randrange(2000, 20000, 1000)
		type = Mysql().reslut_replace('SELECT `key` FROM param WHERE type="PRD_TYPE" ORDER BY id LIMIT 1')
		url = self.host + 'interface/mobile/addMyDelayAucProduct_420'
		data = {"images": images, "video": video, "videoImage": videoImage, "name": name, "desc": desc, "type": type,
				"beginPrice": beginPrice, "bidIncValue": bidIncValue,
				"marketPriceValue": marketPriceValue, 'bigImages': bigImages}
		self.headers.update(Authorization=Authorization)
		req = requests.post(url, data=data, headers=self.headers)
		return req

	# 添加秒啪拍场
	def addMyDelayAucAuction_420(self, name, desc, icon, productIdList, expectedStartTime, expectedEndTime):
		# 拍场类型
		categoryCode = 'A_D_T_01'
		autoIcon = random.sample([True, False], 1)[0]
		apprState = 'P'
		scheduled = random.sample([True, False], 1)[0]
		bidBondAmount = random.randint(0, 10000)
		buyerCommissionPercent = random.randint(0, 10)
		freePost = random.sample([True, False], 1)[0]
		url = self.host + 'interface/mobile/addMyDelayAucAuction_420'
		data = {'icon': icon, 'name': name, 'desc': desc, 'categoryCode': categoryCode, 'productIdList': productIdList,
				'autoIcon': autoIcon, 'apprState': apprState, 'expectedStartTime': expectedStartTime,
				'expectedEndTime': expectedEndTime, 'scheduled': scheduled, 'bidBondAmount': bidBondAmount,
				'buyerCommissionPercent': buyerCommissionPercent, 'freePost': freePost}
		self.headers.update(Authorization=Authorization)
		req = requests.post(url, data=data, headers=self.headers)
		return req

