#!user/bin/python
# -*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2020/1/20 11:37'

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import datetime
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from api import *
from GetFile import GetUserInfo, GetConfig, GetName
from LRedis import localRedis
import random
import json
import re
from mysql import Mysql
from redis_info import *


class BPFrame(Frame):  # 继承Frame类
	"""轰啪拍品"""
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.root = master  # 定义内部变量root
		self.beginPrice = StringVar()
		self.bid_Ivc = StringVar()
		self.images = StringVar()
		self.markePrice = StringVar()
		self.PlanTime = StringVar()
		self.PTpye = StringVar()
		self.name = StringVar()
		self.desc = StringVar()
		self.config = GetConfig().get_txt[0]
		self.desc_text = None
		self.createPage()

	def createPage(self):
		product_info = GetRedis().get_bid_product
		Label(self, text=" ").grid(row=0)
		Label(self, text="创建轰啪拍品", font=("楷体", 20), fg="#9370DB").grid(row=3, rowspan=2, columnspan=5)
		Label(self, text=" ").grid(row=5)
		Label(self, text='名 字: ', font=("楷体", 12)).grid(row=6, stick=W, pady=6)
		name_enrty = Entry(self, textvariable=self.name, width=38, font=("楷体", 12))
		name_enrty.grid(row=6, column=1, stick=E)
		name_enrty.insert(0, product_info['lotName'])
		Label(self, text='描 述: ', font=("楷体", 12)).grid(row=7, stick=W, pady=6)
		self.desc_text = Text(self, width=38, height=5, font=("楷体", 12))
		self.desc_text.grid(row=7, column=1, stick=E)
		self.desc_text.insert(INSERT, GetUserInfo().filter_emoji(product_info['lotDesc']))
		self.desc = self.desc_text.get('0.0', "end")
		Label(self, text='图 片: ', font=("楷体", 12)).grid(row=8, stick=W, pady=6)
		img = Entry(self, width=38, font=("楷体", 12), textvariable=self.images)
		img.grid(row=8, column=1, stick=E)
		img.insert(0, product_info['lotImages'])
		Label(self, text='起拍价: ', font=("楷体", 12)).grid(row=9, stick=W, pady=6)
		begin_price_enter = Entry(self, textvariable=self.beginPrice, width=43)
		begin_price_enter.grid(row=9, column=1, stick=E)
		begin_price_enter.insert(0, str(random.randrange(0, 10000, 500)))
		Label(self, text='加价幅度: ', font=("楷体", 12)).grid(row=10, stick=W, pady=6)
		bidlivc = ttk.Combobox(self, width=35, font=("楷体", 12), textvariable=self.bid_Ivc, state='readonly')
		bidlivc.grid(row=10, column=1, stick=E)
		bidlivc["values"] = list(self.config['bid_Ivc_list'].values())
		bidlivc.current(0)
		Label(self, text='市场估价: ', font=("楷体", 12)).grid(row=11, stick=W, pady=6)
		market = ttk.Combobox(self, width=35, font=("楷体", 12), textvariable=self.markePrice, state='readonly')
		market.grid(row=11, column=1, stick=E)
		market['values'] = list(self.config['market_value_list'].values())
		market.current(0)
		Label(self, text='预拍时长: ', font=("楷体", 12)).grid(row=12, stick=W, pady=6)
		pretime = ttk.Combobox(self, width=35, font=("楷体", 12), textvariable=self.PlanTime, state='readonly')
		pretime.grid(row=12, column=1, stick=E)
		pretime['values'] = list(self.config['pre_time_list'].values())
		pretime.current(0)
		Label(self, text='拍品类型: ', font=("楷体", 12)).grid(row=13, stick=W, pady=6)
		ptype = ttk.Combobox(self, width=35, font=("楷体", 12), textvariable=self.PTpye, state='readonly')
		ptype.grid(row=13, column=1, stick=E)
		ptype['values'] = list(self.config['type_list'].values())
		ptype.current(0)
		Label(self, text=" ").grid(row=14)
		Label(self, text=" ").grid(row=15)
		buttom_frame = Frame(self)
		buttom_frame.grid(row=16, column=1)
		Button(buttom_frame, text="添 加", font=("楷体", 12), command=self.addProduct, width = 10).grid(row=1, column=1, stick=E, pady=6)
		Button(buttom_frame, text="刷 新", font=("楷体", 12), command=self.refresh, width = 10).grid(row=1, column=2, stick=E, pady=6)
		Button(buttom_frame, text="关 闭", font=("楷体", 12), command=self.close, width = 10).grid(row=1, column=3, stick=E, pady=6)

	def addProduct(self):
		Authorization = GetUserInfo().get_file['Authorization']
		online_product = random.choice(localRedis.keys(pattern="APP_BID_INFO:*"))
		online_info = json.loads(list(localRedis.hscan(online_product, count=1)[1].values())[0].decode())
		lotname = self.name.get()
		lotImage = self.images.get()
		beginPrice = self.beginPrice.get()
		bidIvc = self.bid_Ivc.get()
		bidIvc = list(self.config['bid_Ivc_list'].keys())[list(self.config['bid_Ivc_list'].values()).index(bidIvc)]
		mprice = self.markePrice.get()
		mprice = list(self.config['market_value_list'].keys())[
			list(self.config['market_value_list'].values()).index(mprice)]
		ptye = self.PTpye.get()
		ptye = list(self.config['type_list'].keys())[list(self.config['type_list'].values()).index(ptye)]
		ptm = self.PlanTime.get()
		ptm = list(self.config['pre_time_list'].keys())[list(self.config['pre_time_list'].values()).index(ptm)]
		req = addMyAppProduct_270(Authorization, beginPrice=beginPrice, name=lotname, desc=self.desc, icon=lotImage,
								  bidInc=bidIvc, marketPrice=mprice, planTime=ptm, ptype=ptye)
		if req.status_code == 200:
			showinfo(title='恭喜', message='成功创建轰啪拍品')
		else:
			showinfo(title='Sorry', message=req.text)

	def close(self):
		self.quit()

	def refresh(self):
		product_info = GetRedis().get_bid_product
		self.name.set(product_info['lotName'])
		self.desc_text.delete("0.0", "end")
		self.desc_text.insert(INSERT, GetUserInfo().filter_emoji(product_info['lotDesc']))
		self.images.set(product_info['lotImages'])
		self.beginPrice.set(str(random.randrange(0, 100000, 1000)))
		self.bid_Ivc.set(list(self.config['bid_Ivc_list'].values())[0])
		self.markePrice.set(list(self.config['market_value_list'].values())[0])
		self.PlanTime.set(list(self.config['pre_time_list'].values())[0])
		self.PTpye.set(list(self.config['type_list'].values())[0])


class DPFrame(Frame):  # 继承Frame类
	"""秒啪拍品"""
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.root = master  # 定义内部变量root
		self.name = StringVar()
		self.desc = StringVar()
		self.img = StringVar()
		self.beginPrice = StringVar()
		self.bid_Ivc = StringVar()
		self.markePrice = StringVar()
		self.PlanTime = StringVar()
		self.PTpye = StringVar()
		self.config = GetConfig().get_txt[0]
		self.desc_text = None
		self.createPage()

	def createPage(self):
		product_info = GetRedis().get_delay_product
		Label(self, text=" ").grid(row=0)
		Label(self, text="创建秒啪拍品", font=("楷体", 20), fg="#9370DB").grid(row=3, rowspan=2, columnspan=5)
		Label(self, text=" ").grid(row=5)
		Label(self, text="名 字: ", font=("楷体", 12)).grid(row=6, stick=W, pady=6)
		name_entry = Entry(self, textvariable=self.name, font=("楷体", 12), width=43)
		name_entry.grid(row=6, column=1, stick=E)
		name_entry.insert(0, product_info['lotName'])
		Label(self, text="描 述: ", font=("楷体", 12)).grid(row=7, stick=W, pady=6)
		self.desc_text = Text(self, height=5, font=("楷体", 12), width=43)
		self.desc_text.grid(row=7, column=1, stick=E)
		self.desc_text.insert(INSERT, GetUserInfo().filter_emoji(product_info['lotDesc']))
		self.desc = self.desc_text.get('0.0', 'end')
		Label(self, text="图 片: ", font=("楷体", 12)).grid(row=8, stick=W, pady=6)
		img = Entry(self, textvariable=self.img, font=("楷体", 12), width=43)
		img.grid(row=8, column=1, stick=E)
		img.insert(0, product_info['lotImages'])
		Label(self, text='起拍价: ', font=("楷体", 12),).grid(row=9, stick=W, pady=6)
		bp = Entry(self, textvariable=self.beginPrice, width=49)
		bp.grid(row=9, column=1, stick=E)
		bp.insert(0, str(random.randrange(0, 2000, 100)))
		Label(self, text='加价幅度: ', font=("楷体", 12)).grid(row=10, stick=W, pady=6)
		ivp = Entry(self, textvariable=self.bid_Ivc, width=49)
		ivp.grid(row=10, column=1, stick=E)
		ivp.insert(0, str(random.randrange(0, 2000, 100)))
		Label(self, text='市场估价: ', font=("楷体", 12)).grid(row=11, stick=W, pady=6)
		mp = Entry(self, textvariable=self.markePrice, width=49)
		mp.grid(row=11, column=1, stick=E)
		mp.insert(0, str(random.randrange(5000, 200000, 1000)))
		Label(self, text='拍品类型: ', font=("楷体", 12)).grid(row=12, stick=W, pady=6)
		ptype = ttk.Combobox(self, width=40, font=("楷体", 12), textvariable=self.PTpye, state='readonly')
		ptype.grid(row=12, column=1, stick=E)
		ptype['values'] = list(self.config['type_list'].values())
		ptype.current(0)
		Label(self, text=" ").grid(row=13)
		Label(self, text=" ").grid(row=14)
		buttom_frame = Frame(self)
		buttom_frame.grid(row=15, column=1)
		Button(buttom_frame, text="添 加", font=("楷体", 12), command=self.addProduct, width=10).grid(row=1, column=1,
																								  stick=E, pady=6)
		Button(buttom_frame, text="刷 新", font=("楷体", 12), command=self.refresh, width=10).grid(row=1, column=2, stick=E,
																							   pady=6)
		Button(buttom_frame, text="关 闭", font=("楷体", 12), command=self.close, width=10).grid(row=1, column=3, stick=E,
																							 pady=6)

	def addProduct(self):
		Authorization = GetUserInfo().get_file['Authorization']
		lotname = self.name.get()
		lotdesc = self.desc
		lotImage = self.img.get()
		beginPrice = self.beginPrice.get()
		bidIvc = self.bid_Ivc.get()
		mprice = self.markePrice.get()
		ptye = self.PTpye.get()
		ptye = list(self.config['type_list'].keys())[list(self.config['type_list'].values()).index(ptye)]
		req = addMyDelayAucProduct_420(Authorization, beginPrice=beginPrice, name=lotname, desc=lotdesc,
									   images=lotImage,
									   bidIncValue=bidIvc, marketPriceValue=mprice, type=ptye)
		if req.status_code == 200:
			showinfo(title='恭喜', message='成功创建秒啪拍品')
		else:
			showinfo(title='Sorry', message=req.text)

	def close(self):
		self.quit()

	def refresh(self):
		product_info = GetRedis().get_delay_product
		self.name.set(product_info['lotName'])
		self.desc_text.delete("0.0", "end")
		self.desc_text.insert(INSERT, GetUserInfo().filter_emoji(product_info['lotDesc']))
		self.img.set(product_info['lotImages'])
		self.beginPrice.set(str(random.randrange(0, 2000, 100)))
		self.bid_Ivc.set(str(random.randrange(0, 2000, 100)))
		self.markePrice.set(str(random.randrange(5000, 200000, 1000)))


class BAFrame(Frame):  # 继承Frame类
	"""轰啪拍场"""
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.root = master  # 定义内部变量root
		self.startTime = StringVar()
		self.time_unit = StringVar()
		self.auctionType = StringVar()
		self.preEnter = StringVar()
		self.perActionDelay = StringVar()
		self.config = GetConfig().get_txt[0]
		self.images = StringVar()
		self.name = StringVar()
		self.auctionInfo = GetRedis().get_bid_auction
		self.createPage()

	def createPage(self):
		Label(self, text="").grid(row=0)
		Label(self, text="创建轰啪拍场", font=("楷体", 20), fg="#9370DB").grid(row=3, rowspan=2, columnspan=5)
		Label(self, text="").grid(row=5)
		Label(self, text="名 字: ", font=("楷体", 12)).grid(row=6, stick=W, pady=6)
		name_entry = Entry(self, textvariable=self.name, font=("楷体", 12), width=43)
		name_entry.grid(row=6, column=1, stick=E)
		name_entry.insert(0, self.auctionInfo[b'auctionName'].decode("utf-8"))
		Label(self, text="描 述: ", font=("楷体", 12)).grid(row=7, stick=W, pady=6)
		self.desc_text = Text(self, height=5, font=("楷体", 12), width=43)
		self.desc_text.grid(row=7, column=1, stick=E)
		self.desc_text.insert(INSERT, GetUserInfo().filter_emoji(self.auctionInfo[b'auctionDesc'].decode("utf-8")))
		self.desc = self.desc_text.get('0.0', 'end')
		Label(self, text="图 片: ", font=("楷体", 12)).grid(row=8, stick=W, pady=6)
		img = Entry(self, textvariable=self.images, font=("楷体", 12), width=43)
		img.grid(row=8, column=1, stick=E)
		img.insert(0, self.auctionInfo[b'auctionIcon'].decode("utf-8"))
		Label(self, text="开拍时间: ", font=("楷体", 12)).grid(row=9, stick=W, pady=6)
		stime_frame = Frame(self)
		stime_frame.grid(row=9, column=1, stick=W)
		Label(stime_frame, text="据当前时间增加: ", font=("楷体", 12)).grid(row=1, column=1, stick=W)
		addtime = Entry(stime_frame, textvariable=self.startTime, width=10, font=("楷体", 12))
		addtime.grid(row=1, column=2, stick=W)
		addtime.insert(0, "5")
		unitList = ttk.Combobox(stime_frame, textvariable=self.time_unit, width=5, state='readonly')
		unitList.grid(row=1, column=3, stick=E)
		unitList['values'] = ["分钟", "小时", "天"]
		unitList.current(0)
		Label(self, text="拍场类型: ", font=("楷体", 12)).grid(row=10, stick=W, pady=6)
		auctionType = ttk.Combobox(self, width=40, font=("楷体", 12), textvariable=self.auctionType, state='readonly')
		auctionType.grid(row=10, column=1, stick=E)
		auctionType['values'] = list(self.config['auctionTypelist'].values())
		auctionType.current(0)
		Label(self, text="预进入时间: ", font=("楷体", 12)).grid(row=11, stick=W, pady=6)
		PreEnter = ttk.Combobox(self, width=40, font=("楷体", 12), textvariable=self.preEnter, state='readonly')
		PreEnter.grid(row=11, column=1, stick=E)
		PreEnter['values'] = list(self.config['PreEnterlist'].values())
		PreEnter.current(0)
		Label(self, text="预热时间: ", font=("楷体", 12)).grid(row=12, stick=W, pady=6)
		perActionDelay = ttk.Combobox(self, width=40, font=("楷体", 12), textvariable=self.perActionDelay, state='readonly')
		perActionDelay.grid(row=12, column=1, stick=E)
		perActionDelay['values'] = list(self.config['perActionDelaylist'].values())
		perActionDelay.current(0)
		Label(self, text="", font=("楷体", 12)).grid(row=13)
		Label(self, text="", font=("楷体", 12)).grid(row=14)
		button_list = Frame(self)
		button_list.grid(row=16, column=1)
		Button(button_list, text="确 认", font=("楷体", 12), command=self.addAuction).grid(row=1, column=1, stick=E, pady=6)
		Label(button_list, text=" ", font=("楷体", 12)).grid(row=1, column=2, stick=W, pady=6)
		Button(button_list, text="刷 新", font=("楷体", 12), command=self.refresh).grid(row=1, column=3, stick=E, pady=6)
		Label(button_list, text=" ", font=("楷体", 12)).grid(row=1, column=4, stick=W, pady=6)
		Button(button_list, text="取 消", font=("楷体", 12), command=self.close).grid(row=1,column=5, stick=E, pady=6)

	def addAuction(self):
		user_info = GetUserInfo().get_file
		Authorization = user_info['Authorization']
		memberId = user_info['memberId']
		auctionResult = self.auctionInfo
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
				productList += (str(preq.json()['id']) + ",")
		productList = productList.strip(',')
		auctionName = self.name.get()
		auctionDesc = self.desc
		auctionIcon = self.images.get()
		startNum = self.startTime.get()
		unit_time = self.time_unit.get()
		if unit_time == "分钟":
			startTime = datetime.datetime.now() + datetime.timedelta(minutes=int(startNum))
		elif unit_time == "小时":
			startTime = datetime.datetime.now() + datetime.timedelta(hours=int(startNum))
		else:
			startTime = datetime.datetime.now() + datetime.timedelta(days=int(startNum))
		sqlstartTime = startTime.strftime("%Y-%m-%d %H:%M")
		startTime = startTime.strftime("%Y-%m-%d %H:%M:%S")
		auctionType = list(self.config['auctionTypelist'].keys())[list(self.config['auctionTypelist'].values()).index(self.auctionType.get())]
		preEnter = list(self.config['PreEnterlist'].keys())[list(self.config['PreEnterlist'].values()).index(self.preEnter.get())]
		perActionDelay = list(self.config['perActionDelaylist'].keys())[list(self.config['perActionDelaylist'].values()).index(self.perActionDelay.get())]
		req = addMyAppOfficeAuction_240 \
			(Authorization=Authorization, name=auctionName, icon=auctionIcon, auctionType=auctionType,
			 productIds=productList, startTime=startTime, desc=auctionDesc, preEnter=preEnter,
			 perActionDelay=perActionDelay)
		if req.status_code == 200:
			showinfo(title='恭喜', message='成功创建轰啪拍场')
			new_auctionId = Mysql().reslut_replace \
				(f'select id from auction where member_id={memberId} and bid_model="AUC_BID" and valid=TRUE '
				 f'AND source="APP" AND appr_state="W" and `name` ="{auctionName}" and '
				 f'DATE_FORMAT(start_time,"%Y-%m-%d %H:%i")="{sqlstartTime}" ORDER BY id DESC')
			UPDATESQL = f'UPDATE lot SET deliver_people="TESTADMIN" ' \
						f'WHERE auction_id={new_auctionId} AND valid=TRUE AND source="APP"'
			Mysql().do(UPDATESQL)
		else:
			showinfo(title='Sorry', message=req.text)

	def close(self):
		self.quit()

	def refresh(self):
		self.auctionInfo = GetRedis().get_bid_auction
		self.name.set(self.auctionInfo[b'auctionName'].decode("utf-8"))
		self.images.set(self.auctionInfo[b'auctionIcon'].decode("utf-8"))
		self.desc_text.delete("0.0", "end")
		self.desc_text.insert(INSERT, GetUserInfo().filter_emoji(self.auctionInfo[b'auctionDesc'].decode("utf-8")))


class DAFrame(Frame):
	"""添加秒啪拍场"""
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.root = master  # 定义内部变量root
		self.name = StringVar()
		self.images = StringVar()
		self.expectedStartTime = StringVar()
		self.UnitStartTime = StringVar()
		self.expectedEndTime = StringVar()
		self.UnitEndTime = StringVar()
		self.bidBondAmount = StringVar()
		self.buyerCommissionPercent = StringVar()
		self.freePost = StringVar()
		self.config = GetConfig().get_txt[0]
		self.auctionInfo = GetRedis().get_delay_auction
		self.createPage()

	def createPage(self):
		Label(self).grid(row=0)
		Label(self, text="创建秒啪拍场", font=("楷体", 20), fg="#9370DB").grid(row=3, rowspan=2, columnspan=5)
		Label(self, text=" ").grid(row=5)
		Label(self, text='拍场名字: ', font=("楷体", 12)).grid(row=6, stick=W, pady=6)
		aname = Entry(self, textvariable=self.name, font=("楷体", 12), width=43)
		aname.grid(row=6, column=1, stick=E)
		aname.insert(0, GetUserInfo().filter_emoji(self.auctionInfo[b'auctionName'].decode("utf-8")))
		Label(self, text="描 述: ", font=("楷体", 12)).grid(row=7, stick=W, pady=6)
		self.desc_text = Text(self, height=5, font=("楷体", 12), width=43)
		self.desc_text.grid(row=7, column=1, stick=E)
		self.desc_text.insert(INSERT, GetUserInfo().filter_emoji(self.auctionInfo[b'auctionDesc'].decode("utf-8")))
		self.desc = self.desc_text.get('0.0', 'end')
		Label(self, text="图 片: ", font=("楷体", 12)).grid(row=8, stick=W, pady=6)
		img = Entry(self, textvariable=self.images, font=("楷体", 12), width=43)
		img.grid(row=8, column=1, stick=E)
		img.insert(0, self.auctionInfo[b'auctionIcon'].decode("utf-8"))
		Label(self, text="预拍时间: ", font=("楷体", 12)).grid(row=9, stick=W, pady=6)
		stime_frame = Frame(self)
		stime_frame.grid(row=9, column=1, stick=W)
		Label(stime_frame, text="据当前时间增加: ", font=("楷体", 12)).grid(row=1, column=1, stick=W)
		addtime = Entry(stime_frame, textvariable=self.expectedStartTime, width=10, font=("楷体", 12))
		addtime.grid(row=1, column=2, stick=W)
		addtime.insert(0, "5")
		sunitList = ttk.Combobox(stime_frame, textvariable=self.UnitStartTime, width=5, state='readonly')
		sunitList.grid(row=1, column=3, stick=E)
		sunitList['values'] = ["分钟", "小时", "天"]
		sunitList.current(0)
		Label(self, text="预结束时间: ", font=("楷体", 12)).grid(row=10, stick=W, pady=6)
		end_frame = Frame(self)
		end_frame.grid(row=10, column=1, stick=W)
		Label(end_frame, text="据当前时间增加: ", font=("楷体", 12)).grid(row=1, column=1, stick=W)
		addtime = Entry(end_frame, textvariable=self.expectedEndTime, width=10, font=("楷体", 12))
		addtime.grid(row=1, column=2, stick=W)
		addtime.insert(0, "35")
		eunitList = ttk.Combobox(end_frame, textvariable=self.UnitStartTime, width=5, state='readonly')
		eunitList.grid(row=1, column=3, stick=E)
		eunitList['values'] = ["分钟", "小时", "天"]
		eunitList.current(0)
		Label(self, text="保证金: ", font=("楷体", 12)).grid(row=11, stick=W, pady=6)
		bda = Entry(self, textvariable=self.bidBondAmount, width=49)
		bda.grid(row=11, column=1, stick=E)
		bda.insert(0, str(random.randrange(1000, 50000, 1000)))
		Label(self, text="佣金比: ", font=("楷体", 12)).grid(row=12, stick=W, pady=6)
		bcp = Entry(self, textvariable=self.buyerCommissionPercent, width=49)
		bcp.grid(row=12, column=1, stick=E)
		bcp.insert(0, str(random.randint(0, 10)))
		button_list = Frame(self)
		button_list.grid(row=14, column=1)
		Button(button_list, text="确 认", font=("楷体", 12), command=self.addAuction).grid(row=1, column=1, stick=E, pady=6)
		Label(button_list, text=" ", font=("楷体", 12)).grid(row=1, column=2, stick=W, pady=6)
		Button(button_list, text="刷 新", font=("楷体", 12), command=self.refresh).grid(row=1, column=3, stick=E, pady=6)
		Label(button_list, text=" ", font=("楷体", 12)).grid(row=1, column=4, stick=W, pady=6)
		Button(button_list, text="取 消", font=("楷体", 12), command=self.close).grid(row=1, column=5, stick=E, pady=6)


	def addAuction(self):
		user_info = GetUserInfo().get_file
		Authorization = user_info['Authorization']
		memberId = user_info['memberId']
		auctionResult = self.auctionInfo
		productList = ''
		user_role = Mysql().reslut_replace(f'SELECT IF(put_auction,TRUE,FALSE) FROM member_seller_info WHERE member_id={memberId}')
		if user_role == "1":
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
			auctionName = self.name.get()
			auctionDesc = self.desc
			auctionIcon = self.images.get()
			StartNum = self.expectedStartTime.get()
			EndNum = self.expectedEndTime.get()
			StartUnit = self.UnitStartTime.get()
			EndUnit = self.UnitEndTime.get()
			bidBondAmount = self.bidBondAmount.get()
			if StartUnit == "分钟":
				expectedStartTime = datetime.datetime.now() + datetime.timedelta(minutes=int(StartNum))
			elif StartUnit == "小时":
				expectedStartTime = datetime.datetime.now() + datetime.timedelta(hours=int(StartNum))
			else:
				expectedStartTime = datetime.datetime.now() + datetime.timedelta(days=int(StartNum))
			if EndUnit == "分钟":
				expectedEndTime = datetime.datetime.now() + datetime.timedelta(minutes=int(StartNum))
			elif EndUnit == "小时":
				expectedEndTime = datetime.datetime.now() + datetime.timedelta(hours=int(StartNum))
			else:
				expectedEndTime = datetime.datetime.now() + datetime.timedelta(days=int(StartNum))
			expectedStartTime = expectedStartTime.strftime("%Y-%m-%d %H:%M:%S")
			expectedEndTime = expectedEndTime.strftime("%Y-%m-%d %H:%M:%S")
			buyerCommissionPercent = self.buyerCommissionPercent.get()
			req = addMyDelayAucAuction_420(Authorization=Authorization, name=auctionName,
										   icon=auctionIcon, productIdList=productList,
										   desc=auctionDesc, expectedStartTime=expectedStartTime,
										   expectedEndTime=expectedEndTime, bidBondAmount=bidBondAmount,
										   buyerCommissionPercent=buyerCommissionPercent)
			if req.status_code == 200:
				showinfo(title='恭喜', message='成功创建秒啪拍场')
			else:
				showinfo(title='Sorry', message=req.text)
		else:
			showinfo(title='Sorry', message="你当前无设置专场的权限,请联系管理员开通权限")

	def close(self):
		self.quit()

	def refresh(self):
		self.auctionInfo = GetRedis().get_delay_auction
		self.name.set(self.auctionInfo[b'auctionName'].decode("utf-8"))
		self.images.set(self.auctionInfo[b'auctionIcon'].decode("utf-8"))
		self.desc_text.delete("0.0", "end")
		self.desc_text.insert(INSERT, GetUserInfo().filter_emoji(self.auctionInfo[b'auctionDesc'].decode("utf-8")))
		self.bidBondAmount.set(str(random.randrange(1000, 50000, 1000)))
		self.buyerCommissionPercent.set(str(random.randint(0, 10)))


class AuctionList():

	def __init__(self, meberId):
		self._meberId = meberId

	def get_delay_aucution(self):
		sql = f'SELECT CONCAT("秒啪：", a.id) FROM auction a ' \
			  f'WHERE a.appr_state="P" AND a.valid=TRUE AND a.member_id={self._meberId} ' \
			  f'AND a.bid_model="AUC_DELAY" AND a.auction_state IN ("A", "N") AND a.id ' \
			  f'NOT in (SELECT auction_id FROM live WHERE live_type="DELAY_AUC_LIVE" AND source="APP" ' \
			  f'AND valid=TRUE AND appr_state="PASS" AND live_state="PROCESS") GROUP BY a.id ORDER BY a.start_time'
		auctionList = Mysql().sql_result(sql)
		return auctionList

	def get_bid_aucution(self):
		sql = f'SELECT CONCAT("轰啪：", id) FROM auction WHERE appr_state="P" AND member_id={self._meberId}' \
			  f' AND bid_model="AUC_BID" AND auction_state ="N" AND live_auction = FALSE'
		auctionList = Mysql().sql_result(sql)
		return auctionList

	def get_auction_list(self):
		auctionList = ["请选择拍场"] + self.get_delay_aucution() + self.get_bid_aucution()
		return auctionList


def get_liveType(name):
	if name == "轰啪直播":
		liveType = "BID_AUC_LIVE"
	elif name == "秒啪直播":
		liveType = "DELAY_AUC_LIVE"
	elif name == "商城直播":
		liveType = "MALL_SHOP_LIVE"
	else:
		liveType = "FORUM"
	return liveType

class CLiveFrame(Frame):
	"""直播创建"""
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.root = master
		self.name = StringVar()
		self.liveType = StringVar()
		self.images = StringVar()
		self.specialGuestId = StringVar()
		self.presenterId = StringVar()
		self.config = GetConfig().get_txt[0]
		self.UnitStartTime = StringVar()
		self.addtime = StringVar()
		self.preEnter = StringVar()
		self.auctionId = StringVar()
		self.createPage()

	def createPage(self):
		Label(self, text="").grid(row=0)
		Label(self, text="直播创建", font=("楷体", 20), fg="#9370DB").grid(row=3, rowspan=2, columnspan=5)
		Label(self, text="类 型: ", font=("楷体", 12)).grid(row=5, stick=W, pady=4)
		self.live_type = ttk.Combobox(self, width=40, font=("楷体", 12), textvariable=self.liveType, state='readonly')
		self.live_type.grid(row=5, column=1, stick=E)
		self.live_type['values'] = ["轰啪直播", "秒啪直播", "商城直播", "四点讲堂"]
		self.live_type.current(0)
		Label(self, text="名 字: ", font=("楷体", 12)).grid(row=6, stick=W, pady=4)
		name_entry = Entry(self, textvariable=self.name, font=("楷体", 12), width=42)
		name_entry.grid(row=6, column=1, stick=E)
		name_entry.insert(0, "请输入直播名称")
		Label(self, text="描 述: ", font=("楷体", 12)).grid(row=7, stick=W, pady=4)
		self.desc_text = Text(self, height=3, font=("楷体", 12), width=42)
		self.desc_text.grid(row=7, column=1, stick=E)
		self.desc_text.insert(INSERT, "请输入直播描述")
		self.desc = self.desc_text.get('0.0', 'end')
		Label(self, text="封 面: ", font=("楷体", 12)).grid(row=8, stick=W, pady=4)
		imgbox = ttk.Combobox(self, width=40, font=("楷体", 12), textvariable=self.images)
		imgbox.grid(row=8, column=1, stick=E)
		imgbox['values'] = self.config['imgList']
		imgbox.current(0)
		Label(self, text="嘉 宾: ", font=("楷体", 12)).grid(row=9, stick=W, pady=4)
		self.specialGuestBox = ttk.Combobox(self, width=40, font=("楷体", 12), textvariable=self.specialGuestId, state='readonly')
		self.specialGuestBox.grid(row=9, column=1, stick=E)
		user_info = GetUserInfo().get_file
		memberId = user_info['memberId']
		sql = f'SELECT u.id FROM `user` u, member_acc m ' \
			  f'WHERE m.member_id=u.id AND u.id in(SELECT member_id FROM fans WHERE ' \
			  f'member_id in (SELECT fans_id FROM fans WHERE member_id={memberId}) AND fans_id={memberId})'
		slist = Mysql().sql_result(sql)
		self.specialGuestBox['values'] = ["请选择嘉宾"] + slist
		self.specialGuestBox.current(0)
		Label(self, text="场 控: ", font=("楷体", 12)).grid(row=10, stick=W, pady=4)
		self.PresenterBox = ttk.Combobox(self, width=40, font=("楷体", 12), textvariable=self.presenterId, state='readonly')
		self.PresenterBox.grid(row=10, column=1, stick=E)
		self.PresenterBox['values'] =  ["请选择嘉宾"] + slist
		self.PresenterBox.current(0)
		start_label = Label(self, text="开播时间: ", font=("楷体", 12))
		start_label.grid(row=11, stick=W, pady=6)
		stime_frame = Frame(self)
		stime_frame.grid(row=11, column=1, stick=W)
		Label(stime_frame, text="据当前时间增加: ", font=("楷体", 12)).grid(row=1, column=1, stick=W)
		addtime = Entry(stime_frame, textvariable=self.addtime, width=5, font=("楷体", 12))
		addtime.grid(row=1, column=2, stick=W)
		addtime.insert(0, "5")
		Label(stime_frame, text="", width=2).grid(row=1, column=3, stick=W)
		addList = ttk.Combobox(stime_frame, textvariable=self.UnitStartTime, width=5, state='readonly')
		addList.grid(row=1, column=4, stick=E)
		addList['values'] = ["分钟", "小时", "天"]
		addList.current(0)
		pre_label = Label(self, text="预进入: ", font=("楷体", 12))
		pre_label.grid(row=12, stick=W, pady=6)
		PreEnter = ttk.Combobox(self, width=40, font=("楷体", 12), textvariable=self.preEnter, state='readonly')
		PreEnter.grid(row=12, column=1, stick=E)
		PreEnter['values'] = list(self.config['PreEnterlist'].values())
		PreEnter.current(0)
		aution_label = Label(self, text="拍 场: ", font=("楷体", 12))
		aution_label.grid(row=13, stick=W, pady=6)
		self.auction_combox = ttk.Combobox(self, width=40, font=("楷体", 12), textvariable=self.auctionId, state='readonly')
		self.auction_combox.grid(row=13, column=1, stick=E)
		self.auction_combox['values'] = AuctionList(memberId).get_auction_list()
		self.auction_combox.current(0)
		self.auction_combox.bind("<<ComboboxSelected>>", self.auto_tex)
		button_list = Frame(self)
		button_list.grid(row=15, column=1)
		Button(button_list, text="确 认", font=("楷体", 12), command=self.addLive).grid(row=1, column=1, stick=E, pady=6)
		Label(button_list, text=" ", font=("楷体", 12)).grid(row=1, column=2, stick=W, pady=6)
		Button(button_list, text="刷 新", font=("楷体", 12), command=self.refresh).grid(row=1, column=3, stick=E, pady=6)
		Label(button_list, text=" ", font=("楷体", 12)).grid(row=1, column=4, stick=W, pady=6)
		Button(button_list, text="取 消", font=("楷体", 12), command=self.close).grid(row=1, column=5, stick=E, pady=6)


	def auto_tex(self, event=None):
		if self.liveType.get() in ["轰啪直播", "秒啪直播"]:
			auctionId = ''.join(re.findall('\d', self.auctionId.get()))
			if len(auctionId) > 0:
				auction_info = Mysql().sql_result(f'select `name`, `desc` from auction where id = {auctionId}')
				self.name.set(auction_info[0][0])
				self.desc_text.delete("0.0", "end")
				self.desc_text.insert(INSERT, GetUserInfo().filter_emoji(auction_info[0][1]))
		else:
			self.name.set(GetName()._name)
			self.desc_text.delete("0.0", "end")
			self.desc_text.insert(INSERT, (GetName()._name + "\n") *5 )

	def close(self):
		self.quit()

	def refresh(self):
		self.live_type.current(0)
		self.name.set(GetName()._name)
		self.desc_text.delete("0.0", "end")
		self.desc_text.insert(INSERT, (GetName()._name + "\n") * 5)
		self.PresenterBox.current(0)
		self.specialGuestBox.current(0)
		self.auction_combox.current(0)

	def get_startTime(self):
		StartUnit = self.UnitStartTime.get()
		if StartUnit == "分钟":
			startTime = datetime.datetime.now() + datetime.timedelta(minutes=int(self.addtime.get()))
		elif StartUnit == "小时":
			startTime = datetime.datetime.now() + datetime.timedelta(hours=int(self.addtime.get()))
		else:
			startTime = datetime.datetime.now() + datetime.timedelta(days=int(self.addtime.get()))
		return startTime.strftime("%Y-%m-%d %H:%M:%S")

	def addLive(self):
		user_info = GetUserInfo().get_file
		Authorization = user_info['Authorization']
		name = self.name.get()
		desc = self.desc_text.get('0.0', 'end')
		liveType = get_liveType(self.liveType.get())
		startTime = self.get_startTime()
		auctionId = self.auctionId.get()
		auctionId = "".join(re.findall('\d', auctionId))
		icon = self.images.get()
		presenterId = self.presenterId.get()
		specialGuestId = self.specialGuestId.get()
		if not presenterId.isdigit():
			presenterId = None
		if not specialGuestId.isdigit():
			specialGuestId = None
		if not auctionId.isdigit():
			auctionId = None
		preEnter = list(self.config['PreEnterlist'].keys())[list(self.config['PreEnterlist'].values()).index(self.preEnter.get())]
		req = addMyLive_520(Authorization, liveType, presenterId, specialGuestId, icon, name, startTime, preEnter, desc, auctionId)
		if req.status_code == 200:
			showinfo(title='创建成功', message="恭喜！直播创建成功")
		else:
			showinfo(title='创建失败', message=f"对不起，直播创建失败。原因:\n{req.text}")



class ShopFrame(Frame):  # 继承Frame类
	"""商城商品"""
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.root = master  # 定义内部变量root
		self.name = StringVar()
		self.images = StringVar()
		self.single = BooleanVar()
		self.wait_price = BooleanVar()
		self.on_shelf = BooleanVar()
		self.freepost = BooleanVar()
		self.can_return = BooleanVar()
		self.shop_type = StringVar()
		self.dc_shop_type = StringVar()
		self.dc_shop_type = StringVar()
		self.saleprice = StringVar()
		self.originprice = StringVar()
		self.postage = StringVar()
		self.number = StringVar()
		self.productInfo = GetRedis().get_shop_product
		self.createPage()

	def createPage(self):
		Label(self, text="").grid(row=0)
		Label(self, text="创建商城商品", font=("楷体", 20), fg="#9370DB").grid(row=3, rowspan=2, columnspan=5)
		Label(self, text="名 字: ", font=("楷体", 12)).grid(row=5, stick=W, pady=4)
		name_entry = Entry(self, textvariable=self.name, font=("楷体", 12), width=43)
		name_entry.grid(row=5, column=1, stick=E)
		name_entry.insert(0, GetUserInfo().filter_emoji(self.productInfo['name']))
		Label(self, text="描 述: ", font=("楷体", 12)).grid(row=6, stick=W, pady=4)
		self.desc_text = Text(self, height=3, font=("楷体", 12), width=43)
		self.desc_text.grid(row=6, column=1, stick=E)
		if 'desc' in list(self.productInfo.keys()):
			self.desc_text.insert(INSERT, GetUserInfo().filter_emoji(self.productInfo['desc']))
		else:
			self.desc_text.insert(INSERT, GetUserInfo().filter_emoji((self.productInfo['name'] + '\n') * 5))
		self.desc = self.desc_text.get('0.0', 'end')
		Label(self, text="图 片: ", font=("楷体", 12)).grid(row=7, stick=W, pady=4)
		img = Entry(self, textvariable=self.images, font=("楷体", 12), width=43)
		img.grid(row=7, column=1, stick=E)
		img.insert(0, self.productInfo["images"])
		Label(self, text="单 品: ", font=("楷体", 12)).grid(row=8, stick=W, pady=4)
		single_combox = ttk.Combobox(self, width=40, font=("楷体", 12), textvariable=self.single, state='readonly')
		single_combox.grid(row=8, column=1, stick=E)
		single_combox['values'] = [False, True]
		single_combox.current(0)
		Label(self, text="待价估询: ", font=("楷体", 12)).grid(row=9, stick=W, pady=4)
		wait_combox = ttk.Combobox(self, width=40, font=("楷体", 12), textvariable=self.wait_price, state='readonly')
		wait_combox.grid(row=9, column=1, stick=E)
		wait_combox['values'] = [False, True]
		wait_combox.current(0)
		Label(self, text="是否上架: ", font=("楷体", 12)).grid(row=10, stick=W, pady=4)
		onshelf_combox = ttk.Combobox(self, width=40, font=("楷体", 12), textvariable=self.on_shelf, state='readonly')
		onshelf_combox.grid(row=10, column=1, stick=E)
		onshelf_combox['values'] = [True, False]
		onshelf_combox.current(0)
		Label(self, text="是否包邮: ", font=("楷体", 12)).grid(row=11, stick=W, pady=4)
		free_combox = ttk.Combobox(self, width=40, font=("楷体", 12), textvariable=self.freepost, state='readonly')
		free_combox.grid(row=11, column=1, stick=E)
		free_combox['values'] = [False, True]
		free_combox.current(0)
		Label(self, text="三天退货: ", font=("楷体", 12)).grid(row=12, stick=W, pady=4)
		self.free_combox = ttk.Combobox(self, width=40, font=("楷体", 12), textvariable=self.can_return, state='readonly')
		self.free_combox.grid(row=12, column=1, stick=E)
		self.free_combox['values'] = [True, False]
		self.free_combox.current(0)
		Label(self, text="藏品类型: ", font=("楷体", 12)).grid(row=13, stick=W, pady=4)
		self.dc_combox = ttk.Combobox(self, width=40, font=("楷体", 12), textvariable=self.dc_shop_type, state='readonly')
		self.dc_combox.grid(row=13, column=1, stick=E)
		self.dc_combox['values'] = Mysql().sql_result(f'select `name` from shop_category where valid=1')
		self.dc_combox.current(0)
		Label(self, text="店铺分类: ", font=("楷体", 12)).grid(row=14, stick=W, pady=4)
		self.shop_combox = ttk.Combobox(self, width=40, font=("楷体", 12), textvariable=self.shop_type, state='readonly')
		self.shop_combox.grid(row=14, column=1, stick=E)
		shop_type_list = Mysql().sql_result\
			(f'select `name` from shop_product_category where shop_id='
			 f'(SELECT id FROM mall_shop WHERE member_id={GetUserInfo().get_file["memberId"]}) and valid=TRUE')
		if len(shop_type_list) == 0:
			shop_type_list = ["请创建分类"]
		self.shop_combox['values'] = shop_type_list
		self.shop_combox.current(0)
		self.inventory_label = Label(self, text="库 存: ", font=("楷体", 12))
		self.inventory_label.grid(row=15, stick=W, pady=4)
		self.nentry = Entry(self, textvariable=self.number, font=("楷体", 12), width=43)
		self.nentry.grid(row=15, column=1, stick=E)
		self.nentry.insert(0, str(random.randint(1, 100)))
		self.origin_price_label = Label(self, text="原 价: ", font=("楷体", 12))
		self.origin_price_label.grid(row=16, stick=W, pady=4)
		self.opentry = Entry(self, textvariable=self.originprice, font=("楷体", 12), width=43)
		self.opentry.grid(row=16, column=1, stick=E)
		op = random.randint(1000, 1000000)
		self.opentry.insert(0, str(op))
		self.sale_price_label = Label(self, text="售 价: ", font=("楷体", 12))
		self.sale_price_label.grid(row=17, stick=W, pady=4)
		self.slentry = Entry(self, textvariable=self.saleprice, font=("楷体", 12), width=43)
		self.slentry.grid(row=17, column=1, stick=E)
		self.slentry.insert(0, str(int(op*0.85)))
		self.postage_label = Label(self, text="邮 费: ", font=("楷体", 12))
		self.postage_label.grid(row=18, stick=W, pady=4)
		self.postentry = Entry(self, textvariable=self.postage, font=("楷体", 12), width=43)
		self.postentry.grid(row=18, column=1, stick=E)
		self.postentry.insert(0, str(random.randint(5, 10)))
		button_list = Frame(self)
		button_list.grid(row=19, column=1)
		Button(button_list, text="确 认", font=("楷体", 12), command=self.addProdct).grid(row=1, column=1, stick=E, pady=6)
		Label(button_list, text=" ", font=("楷体", 12)).grid(row=1, column=2, stick=W, pady=6)
		Button(button_list, text="刷 新", font=("楷体", 12), command=self.refresh).grid(row=1, column=3, stick=E, pady=6)
		Label(button_list, text=" ", font=("楷体", 12)).grid(row=1, column=4, stick=W, pady=6)
		Button(button_list, text="取 消", font=("楷体", 12), command=self.close).grid(row=1, column=5, stick=E, pady=6)

		def dis_play(event=None):
			if wait_combox.get() == "True":
				self.inventory_label.grid_forget()
				self.nentry.grid_forget()
				self.origin_price_label.grid_forget()
				self.opentry.grid_forget()
				self.sale_price_label.grid_forget()
				self.slentry.grid_forget()
			else:
				self.inventory_label.grid(row=15, stick=W, pady=4)
				self.nentry.grid(row=15, column=1, stick=E)
				self.origin_price_label.grid(row=16, stick=W, pady=4)
				self.opentry.grid(row=16, column=1, stick=E)
				self.sale_price_label.grid(row=17, stick=W, pady=4)
				self.slentry.grid(row=17, column=1, stick=E)

		def display_postage(event=None):
			if free_combox.get():
				self.postage_label.grid_forget()
				self.postentry.grid_forget()
			else:
				self.postage_label.grid(row=18, stick=W, pady=4)
				self.postentry.grid(row=18, column=1, stick=E)
		wait_combox.bind("<<ComboboxSelected>>", dis_play)
		free_combox.bind("<<ComboboxSelected>>", display_postage)

	def close(self):
		self.quit()

	def refresh(self):
		self.productInfo = GetRedis().get_shop_product
		self.name.set(GetUserInfo().filter_emoji(self.productInfo['name']))
		self.images.set(self.productInfo['images'])
		self.desc_text.delete("0.0", "end")
		if "desc" in list(self.productInfo.keys()):
			self.desc_text.insert(INSERT, GetUserInfo().filter_emoji(self.productInfo['desc']))
		else:
			self.desc_text.insert(INSERT, GetUserInfo().filter_emoji((self.productInfo['name'] + "\n") * 10))
		op = random.randint(1000, 1000000)
		self.originprice.set(str(op))
		self.saleprice.set(str(int(op*0.9)))
		self.number.set(str(random.randint(1, 100)))

	def addProdct(self):
		user_info = user_info = GetUserInfo().get_file
		Authorization = user_info['Authorization']
		memberId = user_info['memberId']
		name = self.name.get()
		image = self.images.get()
		desc = self.desc
		waitPrice = word_swich_bool(self.wait_price.get())
		single = word_swich_bool(self.single.get())
		returnProduct = word_swich_bool(self.can_return.get())
		freePost = word_swich_bool(self.freepost.get())
		originalPrice = self.originprice.get()
		salesPrice = self.saleprice.get()
		inAuction= word_swich_bool(self.on_shelf.get())
		inventory = self.number.get()
		images = bigImages = self.images.get()
		postage = self.postage.get()
		user_role = Mysql().reslut_replace(f'SELECT IF(mall_shop,TRUE,FALSE) FROM member_seller_info WHERE member_id={memberId}')
		if user_role == "1":
			shopCategory = Mysql().reslut_replace \
				(f'SELECT id FROM shop_product_category WHERE shop_id='
				 f'(SELECT id FROM mall_shop WHERE member_id="{memberId}") and valid=1 and `name`="{self.shop_type.get()}"')
			dcCategory = Mysql().reslut_replace \
				(f'select id from shop_category where valid=1 and `name`="{self.dc_shop_type.get()}"')
			req = addAppShopProduct_500(Authorization, name, desc, waitPrice, originalPrice, salesPrice, shopCategory, dcCategory,
								  inAuction, single, inventory, images, bigImages, returnProduct, freePost, postage)
			if req.status_code == 200:
				showinfo(title='创建成功', message="恭喜！店铺商品创建成功")
			else:
				showinfo(title='创建失败', message= f"不好意思，当前商品创建失败。原因:\n{req.text}")
		else:
			showinfo(title='Sorry', message="你当前无店铺的权限,请联系管理员开通权限")


class DELPFrame(Frame):
	"""清理数据"""
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.root = master  # 定义内部变量root
		self.LotType = StringVar()
		self.createPage()

	def createPage(self):
		Label(self, text=" ").grid(row=0)
		Label(self, text=" ").grid(row=1)
		Label(self, text="清理拍品数据", font=("楷体", 20), fg="#9370DB").grid(row=3, rowspan=2, columnspan=5)
		Label(self, text=" ").grid(row=5)
		Label(self, text='商品类型: ', font=("楷体", 12)).grid(row=6, stick=W, pady=6)
		lot_type_list = ttk.Combobox(self, width=25, font=("楷体", 12), textvariable=self.LotType, state='readonly')
		lot_type_list.grid(row=6, column=1, stick=E)
		lot_type_list['values'] = ["轰啪", "秒啪", "商城"]
		lot_type_list.current(0)
		Label(self).grid(row=7, stick=W, pady=6)
		Label(self).grid(row=8, stick=W, pady=6)
		button_list = Frame(self)
		button_list.grid(row=10, column=1)
		Button(button_list, text="确 认", font=("楷体", 12), command=self.sure).grid(row=1, stick=W, pady=6)
		Label(button_list, text=" ").grid(row=1, column=2)
		Label(button_list, text=" ").grid(row=1, column=3)
		Button(button_list, text="取 消", font=("楷体", 12), command=self.esc).grid(row=1, column=5, stick=E)

	def sure(self):
		sure_value = askokcancel(title="清理数据", message="数据不可逆,请三思而后行。确认要删除数据？")
		memberId = GetUserInfo().get_file['memberId']
		ltype = self.LotType.get()
		if sure_value:
			if ltype == "轰啪":
				sql = f'UPDATE product SET valid=FALSE WHERE member_id={memberId} AND sold_out=FALSE AND in_auction=FALSE AND valid=TRUE AND auction_id IS NULL and bid_model="AUC_BID"'
				Mysql().do(sql)
				showinfo(title='确认', message='数据清除完成')
			elif ltype == "秒啪":
				sql = f'UPDATE product SET valid=FALSE WHERE member_id={memberId} AND sold_out=FALSE AND in_auction=FALSE AND valid=TRUE AND auction_id IS NULL and bid_model="AUC_DELAY"'
				Mysql().do(sql)
				showinfo(title='确认', message='数据清除完成')
			else:
				sql = f'UPDATE product SET valid=FALSE WHERE member_id={memberId} AND sold_out=FALSE AND in_auction=FALSE AND valid=TRUE AND auction_id IS NULL and bid_model="PRODUCT_SHOP"'
				Mysql().do(sql)
				showinfo(title='确认', message='数据清除完成')
		else:
			pass

	def esc(self):
		self.quit()
