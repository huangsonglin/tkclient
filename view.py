#!user/bin/python
# -*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2020/1/20 11:37'

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from api import *
from wirte import get_file
from LRedis import localRedis
import random
import json
from mysql import Mysql


class BPFrame(Frame):  # 继承Frame类
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.root = master  # 定义内部变量root
		self.beginPrice = StringVar()
		self.bid_Ivc = StringVar()
		self.markePrice = StringVar()
		self.PlanTime = StringVar()
		self.PTpye = StringVar()
		self.createPage()

	def createPage(self):
		Label(self).grid(row=0, stick=W, pady=10)
		Label(self, text='起拍价: ', font=("楷体", 12)).grid(row=1, stick=W, pady=10)
		Entry(self, textvariable=self.beginPrice).grid(row=1, column=1, stick=E)
		Label(self, text='加价幅度: ', font=("楷体", 12)).grid(row=2, stick=W, pady=10)
		bidlivc = ttk.Combobox(self, width=15, font=("楷体", 12), textvariable=self.bid_Ivc)
		bidlivc.grid(row=2, column=1, stick=E)
		bidlivc["values"] = ['B_I_01:+¥50', 'B_I_02:+¥100', 'B_I_03:+¥200', 'B_I_04:+¥300', 'B_I_05:+¥400',
							 'B_I_06:+¥500', 'B_I_07:+¥1000', 'B_I_10:+¥1500', 'B_I_08:+¥2000', 'B_I_11:+¥3000',
							 'B_I_09:+¥5000', 'B_I_12:+¥30000', 'B_I_13:+¥10000', 'B_I_14:+¥50000', 'B_I_15:+¥100000']
		# 默认为下拉一个值
		bidlivc.current(0)
		Label(self, text='市场估价: ', font=("楷体", 12)).grid(row=3, stick=W, pady=10)
		market = ttk.Combobox(self, width=15, font=("楷体", 12), textvariable=self.markePrice)
		market.grid(row=3, column=1, stick=E)
		market['values'] = ['P_M_01:¥500以上', 'P_M_02:¥1,000以上', 'P_M_03:¥5,000以上', 'P_M_04:¥10,000以上',
							'P_M_08:¥30,000以上', 'P_M_05:¥50,000以上', 'P_M_09:¥80,000以上', 'P_M_06:¥100,000以上',
							'P_M_07:估价待询', 'P_M_10:¥40万以上', 'P_M_11:¥100万以上', 'P_M_12:¥200万以上',
							'P_M_13:¥500万以上']
		market.current(0)
		Label(self, text='预拍时长: ', font=("楷体", 12)).grid(row=4, stick=W, pady=10)
		pretime = ttk.Combobox(self, width=15, font=("楷体", 12), textvariable=self.PlanTime)
		pretime.grid(row=4, column=1, stick=E)
		pretime['values'] = ['P_P_01:2分钟', 'P_P_02:3分钟', 'P_P_03:5分钟', 'P_P_04:8分钟', 'P_P_05:10分钟', 'P_P_06:15分钟',
							 'P_P_07:240拍场出价测试专用']
		pretime.current(0)
		Label(self, text='拍品类型: ', font=("楷体", 12)).grid(row=5, stick=W, pady=10)
		ptype = ttk.Combobox(self, width=15, font=("楷体", 12), textvariable=self.PTpye)
		ptype.grid(row=5, column=1, stick=E)
		ptype['values'] = ['P_T_01:造像', 'P_T_02:唐卡', 'P_T_03:法器', 'P_T_04:古珠', 'P_T_05:杂项', 'P_T_07:综合',
						   'P_T_06:设计', 'P_T_08:古玉']
		ptype.current(0)
		Button(self, text="确 认", font=("楷体", 12), command=self.addProduct).grid(row=6, stick=W, pady=10)
		Button(self, text="取 消", font=("楷体", 12)).grid(row=6, column=1, stick=E)

	def addProduct(self):
		Authorization = get_file()['Authorization']
		online_product = random.choice(localRedis.keys(pattern="APP_BID_INFO:*"))
		online_info = json.loads(list(localRedis.hscan(online_product, count=1)[1].values())[0].decode())
		lotname = online_info['lotName']
		lotdesc = online_info['lotDesc']
		lotImage = online_info['lotImages']
		beginPrice = self.beginPrice.get()
		bidIvc = self.bid_Ivc.get()
		bidIvc = bidIvc.split(":")[0]
		mprice = self.markePrice.get()
		mprice = mprice.split(":")[0]
		ptye = self.PTpye.get()
		ptye = ptye.split(":")[0]
		ptm = self.PlanTime.get()
		ptm = ptm.split(":")[0]
		req = addMyAppProduct_270(Authorization, beginPrice=beginPrice, name=lotname, desc=lotdesc, icon=lotImage,
								  bidInc=bidIvc, marketPrice=mprice, planTime=ptm, ptype=ptye)
		if req.status_code == 200:
			showinfo(title='恭喜', message='成功创建轰啪拍品')
		else:
			showinfo(title='Sorry', message='创建轰啪拍品失败')


class DPFrame(Frame):  # 继承Frame类
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.root = master  # 定义内部变量root
		self.beginPrice = StringVar()
		self.bid_Ivc = StringVar()
		self.markePrice = StringVar()
		self.PlanTime = StringVar()
		self.PTpye = StringVar()
		self.createPage()

	def createPage(self):
		Label(self).grid(row=0, stick=W, pady=10)
		Label(self, text='起拍价: ', font=("楷体", 12)).grid(row=1, stick=W, pady=10)
		Entry(self, textvariable=self.beginPrice).grid(row=1, column=1, stick=E)
		Label(self, text='加价幅度: ', font=("楷体", 12)).grid(row=2, stick=W, pady=10)
		Entry(self, textvariable=self.bid_Ivc).grid(row=2, column=1, stick=E)
		Label(self, text='市场估价: ', font=("楷体", 12)).grid(row=3, stick=W, pady=10)
		Entry(self, textvariable=self.markePrice).grid(row=3, column=1, stick=E)
		Label(self, text='拍品类型: ', font=("楷体", 12)).grid(row=4, stick=W, pady=10)
		ptype = ttk.Combobox(self, width=15, font=("楷体", 12), textvariable=self.PTpye)
		ptype.grid(row=4, column=1, stick=E)
		ptype['values'] = ['P_T_01:造像', 'P_T_02:唐卡', 'P_T_03:法器', 'P_T_04:古珠', 'P_T_05:杂项', 'P_T_07:综合',
						   'P_T_06:设计', 'P_T_08:古玉']
		ptype.current(0)
		Button(self, text="确 认", font=("楷体", 12), command=self.addProduct).grid(row=6, stick=W, pady=10)
		Button(self, text="取 消", font=("楷体", 12)).grid(row=6, column=1, stick=E)

	def addProduct(self):
		Authorization = get_file()['Authorization']
		online_product = random.choice(localRedis.keys(pattern="APP_DELAY_INFO:*"))
		online_info = json.loads(list(localRedis.hscan(online_product, count=1)[1].values())[0].decode())
		lotname = online_info['lotName']
		lotdesc = online_info['lotDesc']
		lotImage = online_info['lotImages']
		beginPrice = self.beginPrice.get()
		bidIvc = self.bid_Ivc.get()
		mprice = self.markePrice.get()
		ptye = self.PTpye.get()
		ptye = ptye.split(":")[0]
		req = addMyDelayAucProduct_420(Authorization, beginPrice=beginPrice, name=lotname, desc=lotdesc, images=lotImage,
								  bidIncValue=bidIvc, marketPriceValue=mprice, type=ptye)
		if req.status_code == 200:
			showinfo(title='恭喜', message='成功创建轰啪拍品')
		else:
			showinfo(title='Sorry', message='创建轰啪拍品失败')


class BAFrame(Frame):  # 继承Frame类
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.root = master  # 定义内部变量root
		self.data_sources = StringVar()
		self.startTime = StringVar()
		self.startTime.set("开拍时间,格式如:2020-02-22 10:00:00")
		self.auctionType = StringVar()
		self.preEnter = StringVar()
		self.perActionDelay = StringVar()
		self.createPage()

	def createPage(self):
		Label(self).grid(row=0, stick=W, pady=10)
		Label(self, text='数据来源: ', font=("楷体", 12)).grid(row=1, stick=W, pady=10)
		data_sources = ttk.Combobox(self, width=25, font=("楷体", 12), textvariable=self.data_sources)
		data_sources.grid(row=1, column=1, stick=E)
		autionList = random.sample(localRedis.keys(pattern="BID_AUCTION_INFO:*"), 10)
		data_sources['values'] = autionList
		data_sources.current(0)
		Label(self, text="开拍时间: ", font=("楷体", 12)).grid(row=2, stick=W, pady=10)
		Entry(self, textvariable=self.startTime, width=31).grid(row=2, column=1, stick=E)
		Label(self, text="拍场类型: ", font=("楷体", 12)).grid(row=3, stick=W, pady=10)
		auctionType = ttk.Combobox(self, width=25, font=("楷体", 12), textvariable=self.auctionType)
		auctionType.grid(row=3, column=1, stick=E)
		auctionTypelist = Mysql().reslut_replace\
			('SELECT GROUP_CONCAT(`key`, ":", `value`) FROM param WHERE type ="AUCTION_TYPE" GROUP BY type')
		auctionType['values'] = auctionTypelist.split(',')
		auctionType.current(0)
		Label(self, text="预进入时间: ", font=("楷体", 12)).grid(row=4, stick=W, pady=10)
		PreEnter = ttk.Combobox(self, width=25, font=("楷体", 12), textvariable=self.preEnter)
		PreEnter.grid(row=4, column=1, stick=E)
		PreEnterlist = Mysql().reslut_replace \
			('SELECT GROUP_CONCAT(`key`, ":",`value`) FROM param WHERE type ="AUC_PE" GROUP BY type')
		PreEnter['values'] = PreEnterlist.split(',')
		PreEnter.current(0)
		Label(self, text="预热时间: ", font=("楷体", 12)).grid(row=5, stick=W, pady=10)
		perActionDelay = ttk.Combobox(self, width=25, font=("楷体", 12), textvariable=self.perActionDelay)
		perActionDelay.grid(row=5, column=1, stick=E)
		perActionDelaylist = Mysql().reslut_replace \
			('SELECT GROUP_CONCAT(`key`, ":",`value`) FROM param WHERE type ="AUC_ITIME" GROUP BY type')
		perActionDelay['values'] = perActionDelaylist.split(',')
		perActionDelay.current(0)
		Button(self, text="确 认", font=("楷体", 12), command=self.addAuction).grid(row=6, stick=W, pady=10)
		Button(self, text="取 消", font=("楷体", 12)).grid(row=6, column=1, stick=E)

	def addAuction(self):
		txtResult = get_file()
		Authorization = txtResult['Authorization']
		username = txtResult['username']
		memberId = txtResult['memberId']
		auctionId = self.data_sources.get()
		auctionResult = localRedis.hscan(auctionId, count=100)[1]
		productList = ''
		for keys in list(auctionResult.keys()):
			if "lotName" in keys.decode():
				lotInfo = json.loads(auctionResult[keys].decode())
				lotName = lotInfo['lotName']
				lotDesc = lotInfo['lotDesc']
				lotImages = lotInfo['lotImages']
				icon = lotImages.split(",")[0]
				preq = addOfficeMyAppProduct_270 \
					(Authorization=Authorization, name=lotName, icon=icon, desc=lotDesc)
				productList += (str(preq.json()['id'])+",")
		productList = productList.strip(',')
		auctionName = auctionResult[b'auctionName'].decode()
		auctionDesc = auctionResult[b'auctionDesc'].decode()
		auctionIcon = auctionResult[b'auctionIcon'].decode()
		startTime = self.startTime.get()
		auctionType = self.auctionType.get().split(":")[0]
		preEnter = self.preEnter.get().split(":")[0]
		perActionDelay = self.perActionDelay.get().split(':')[0]
		req = addMyAppOfficeAuction_240 \
			(Authorization=Authorization, name=auctionName, icon=auctionIcon, auctionType=auctionType,
			 productIds=productList, startTime=startTime, desc=auctionDesc, preEnter=preEnter, perActionDelay=perActionDelay)
		if req.status_code == 200:
			showinfo(title='恭喜', message='成功创建轰啪拍场')
			auctionId = Mysql().reslut_replace\
				(f'select id from auction where member_id={memberId} and bid_model="AUC_BID" and valid=TRUE '
				 f'AND source="APP" AND appr_state="W" and start_time="{startTime}" ORDER BY id DESC')
			UPDATESQL = f'UPDATE lot SET deliver_people="TESTADMIN" WHERE auction_id={auctionId} AND valid=TRUE AND source="APP"'
			Mysql().do(UPDATESQL)
		else:
			showinfo(title='Sorry', message='创建轰啪拍品拍场')

# 添加秒啪拍场Frame
class DAFrame(Frame):  # 继承Frame类
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.root = master  # 定义内部变量root
		self.data_sources = StringVar()
		# 预拍时间
		self.expectedStartTime = StringVar()
		self.expectedStartTime.set("预拍时间,格式如:2020-02-22 10:00:00")
		# 预结束时间
		self.expectedEndTime = StringVar()
		self.expectedEndTime.set("预结束时间,格式如:2020-02-22 10:00:00")
		# 保证金
		self.bidBondAmount = StringVar()
		# 买家佣金百分比
		self.buyerCommissionPercent = StringVar()
		# 是否包邮
		self.freePost = StringVar()
		self.createPage()

	def createPage(self):
		Label(self).grid(row=0, stick=W, pady=10)
		Label(self, text='数据来源: ', font=("楷体", 12)).grid(row=1, stick=W, pady=10)
		data_sources = ttk.Combobox(self, width=25, font=("楷体", 12), textvariable=self.data_sources)
		data_sources.grid(row=1, column=1, stick=E)
		autionList = random.sample(localRedis.keys(pattern="DELAY_AUCTION_INFO:*"), 10)
		data_sources['values'] = autionList
		data_sources.current(0)
		Label(self, text="预拍时间: ", font=("楷体", 12)).grid(row=2, stick=W, pady=10)
		Entry(self, textvariable=self.expectedStartTime, width=31).grid(row=2, column=1, stick=E)
		Label(self, text="预结束时间: ", font=("楷体", 12)).grid(row=3, stick=W, pady=10)
		Entry(self, textvariable=self.expectedEndTime, width=31).grid(row=3, column=1, stick=E)
		Label(self, text="保证金: ", font=("楷体", 12)).grid(row=4, stick=W, pady=10)
		Entry(self, textvariable=self.bidBondAmount, width=31).grid(row=4, column=1, stick=E)
		Label(self, text="佣金比: ", font=("楷体", 12)).grid(row=5, stick=W, pady=10)
		Entry(self, textvariable=self.buyerCommissionPercent, width=31).grid(row=5, column=1, stick=E)
		Button(self, text="确 认", font=("楷体", 12), command=self.addAuction).grid(row=7, stick=W, pady=10)
		Button(self, text="取 消", font=("楷体", 12)).grid(row=7, column=1, stick=E)

	def addAuction(self):
		Authorization = get_file()['Authorization']
		username = get_file()['username']
		username = get_file()['username']
		auctionId = self.data_sources.get()
		auctionResult = localRedis.hscan(auctionId, count=100)[1]
		memberId = Mysql().reslut_replace(f'select id from user where username={username}')
		productList = ''
		for keys in list(auctionResult.keys()):
			if "lotName" in keys.decode():
				lotInfo = json.loads(auctionResult[keys].decode())
				lotName = lotInfo['lotName']
				lotImages = lotInfo['lotImages']
				icon = lotImages.split(",")[0]
				preq = addMyOfficeDelayAucProduct_420 \
					(Authorization=Authorization, name=lotName, images=lotImages, desc=lotName)
				productList += (preq.json()['id'] + ",")
		productList = productList.strip(',')
		auctionName = auctionResult[b'auctionName'].decode()
		auctionDesc = auctionResult[b'auctionDesc'].decode()
		auctionIcon = auctionResult[b'auctionIcon'].decode()
		expectedStartTime = self.expectedStartTime.get()
		expectedEndTime = self.expectedEndTime.get()
		bidBondAmount = self.bidBondAmount.get()
		buyerCommissionPercent = self.buyerCommissionPercent.get()
		req = addMyDelayAucAuction_420(Authorization=Authorization, name=auctionName,
												icon=auctionIcon, productIdList=productList,
									   desc=auctionDesc, expectedStartTime=expectedStartTime,
									   expectedEndTime=expectedEndTime, bidBondAmount=bidBondAmount,
									   buyerCommissionPercent=buyerCommissionPercent)
		if req.status_code == 200:
			showinfo(title='恭喜', message='成功创建秒啪拍场')
		else:
			showinfo(title='Sorry', message='创建秒啪拍场失败')


class FLFrame(Frame):  # 继承Frame类
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.root = master  # 定义内部变量root
		self.createPage()

	def createPage(self):
		Label(self, text='讲堂直播').pack()
