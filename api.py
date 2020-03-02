#!user/bin/python
# -*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2020/1/8 15:59'

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import redis
import socket
import random
import hashlib
import json
import requests

localhost = socket.gethostname()
lredis = redis.StrictRedis(host=localhost, port="6379", db=0)
f = open(os.path.join(curPath, "config.js"), encoding="utf-8", errors='ignore')
config = json.load(f)
host = config[0]['host']
headers = config[0]['headers']


# 获取token信息
def login(username, password):
	hl = hashlib.md5()
	# 此处必须声明encode
	# 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
	hl.update(str(password).encode(encoding='utf-8'))
	pw = (hl.hexdigest())
	data = {"phoneNum": username, "pwd": pw}
	url = host + 'interface/mobile/pmall/loginByPhone_220'
	req = requests.post(url, data=data, headers=headers)
	return req


# 添加轰啪拍品
def addMyAppProduct_270(Authorization, name, icon, desc, beginPrice, bidInc, marketPrice, planTime, ptype, video=None,
						videoImage=None):
	url = host + 'interface/mobile/addMyAppProduct_270'
	data = {'beginPrice': beginPrice, 'bidInc': bidInc, 'desc': desc, 'marketPrice': marketPrice, 'name': name,
			'planTime': planTime, 'type': ptype, 'images': icon, 'video': video, 'videoImage': videoImage}
	headers.update(Authorization=Authorization)
	req = requests.post(url, data=data, headers=headers)
	return req

def addOfficeMyAppProduct_270(Authorization, name, icon, desc, video=None, videoImage=None):
	url = host + 'interface/mobile/addMyAppProduct_270'
	beginPrice = random.randrange(0, 1000, 100)
	data = {'beginPrice': beginPrice, 'bidInc': "B_I_05", 'desc': desc, 'marketPrice': "P_M_05", 'name': name,
			'planTime': "P_P_01", 'type': "P_T_01", 'images': icon, 'video': video, 'videoImage': videoImage}
	headers.update(Authorization=Authorization)
	req = requests.post(url, data=data, headers=headers)
	return req

# 添加轰啪拍场
def addMyAppOfficeAuction_240(Authorization, auctionType, preEnter, perActionDelay, icon, name, startTime, productIds, desc):
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
	url = host + 'interface/mobile/addMyAppAuction_240'
	keyword = "测试 轰啪 拍场"
	data = {'icon': icon, 'name': name, 'keyword': keyword, 'startTime': startTime, 'productIds': productIds,
			'desc': desc, 'apprState': "W", 'auctionType': auctionType, "perActionDelay": "A_I_01",
			"preEnter": "A_P_10"}
	headers.update(Authorization=Authorization)
	req = requests.post(url, data=data, headers=headers)
	return req


# 添加秒啪拍品
def addMyDelayAucProduct_420(Authorization, name, images, desc, type, beginPrice, bidIncValue,
							 marketPriceValue, video=None, videoImage=None, bigImages=None):
	url = host + 'interface/mobile/addMyDelayAucProduct_420'
	data = {"images": images, "video": video, "videoImage": videoImage, "name": name, "desc": desc, "type": type,
			"beginPrice": beginPrice, "bidIncValue": bidIncValue,
			"marketPriceValue": marketPriceValue, 'bigImages': bigImages}
	headers.update(Authorization=Authorization)
	req = requests.post(url, data=data, headers=headers)
	return req

def addMyOfficeDelayAucProduct_420(Authorization, name, desc, images, video=None,
									   videoImage=None, bigImages=None):
	beginPrice = random.randrange(0, 1000, 100)
	bidIncValue = random.randrange(100, 1000, 100)
	marketPriceValue = random.randrange(2000, 20000, 1000)
	type = "P_T_01"
	url = host + 'interface/mobile/addMyDelayAucProduct_420'
	data = {"images": images, "video": video, "videoImage": videoImage, "name": name, "desc": desc, "type": type,
			"beginPrice": beginPrice, "bidIncValue": bidIncValue,
			"marketPriceValue": marketPriceValue, 'bigImages': bigImages}
	headers.update(Authorization=Authorization)
	req = requests.post(url, data=data, headers=headers)
	return req


# 添加秒啪拍场
def addMyDelayAucAuction_420(Authorization, name, desc, icon, productIdList, expectedStartTime,
							 expectedEndTime, bidBondAmount, buyerCommissionPercent):
	categoryCode = "A_D_T_01"
	apprState = 'P'
	scheduled = random.sample([True, False], 1)[0]
	url = host + 'interface/mobile/addMyDelayAucAuction_420'
	data = {'icon': icon, 'name': name, 'desc': desc, 'categoryCode': categoryCode, 'productIdList': productIdList,
			'autoIcon': False, 'apprState': apprState, 'expectedStartTime': expectedStartTime,
			'expectedEndTime': expectedEndTime, 'scheduled': scheduled, 'bidBondAmount': bidBondAmount,
			'buyerCommissionPercent': buyerCommissionPercent, 'freePost': True}
	headers.update(Authorization=Authorization)
	req = requests.post(url, data=data, headers=headers)
	return req


if __name__ == '__main__':
	# write_token(19800000001, "123456")
	token = login(19800000001, "123456")
	print(token.text)
