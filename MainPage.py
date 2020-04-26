#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2020/1/20 11:37'

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from tkinter import *
from view import *  # 菜单栏对应的各个子页面


class MainPage(object):
	def __init__(self, master=None):
		self.root = master  # 定义内部变量root
		sw = self.root.winfo_screenwidth()
		# 得到屏幕宽度
		sh = self.root.winfo_screenheight()
		self.root.geometry('%dx%d+%d+%d' % (800, 600, 400, 400))  # 设置窗口大小
		self.createPage()

	def createPage(self):
		self.BidProductPage = BPFrame(self.root)  # 创建不同Frame
		self.DelayProductPage = DPFrame(self.root)
		self.BidAuctionPage = BAFrame(self.root)
		self.DelayAuctionPage = DAFrame(self.root)
		self.CreatLivePage = CLiveFrame(self.root)
		self.DeleTeProductPage = DELPFrame(self.root)
		self.ShopProductPage = ShopFrame(self.root)
		self.BidAuctionPage.pack()  # 默认显示数据录入界面
		menubar = Menu(self.root)
		menubar.add_command(label='轰啪拍品', command=self.BidProduct)
		menubar.add_command(label='秒啪拍品', command=self.DelayProduct)
		menubar.add_command(label='商城商品', command=self.ShopProduct)
		menubar.add_command(label='轰啪拍场', command=self.BidAuction)
		menubar.add_command(label='秒啪拍场', command=self.DelayAuction)
		menubar.add_command(label='直播', command=self.CreatLive)
		menubar.add_command(label='数据清理', command=self.DLEProduct)
		self.root['menu'] = menubar  # 设置菜单栏

	def BidProduct(self):
		self.BidProductPage.pack()
		self.DelayProductPage.pack_forget()
		self.BidAuctionPage.pack_forget()
		self.DelayAuctionPage.pack_forget()
		self.CreatLivePage.pack_forget()
		self.DeleTeProductPage.pack_forget()
		self.ShopProductPage.pack_forget()

	def DelayProduct(self):
		self.BidProductPage.pack_forget()
		self.DelayProductPage.pack()
		self.BidAuctionPage.pack_forget()
		self.DelayAuctionPage.pack_forget()
		self.CreatLivePage.pack_forget()
		self.DeleTeProductPage.pack_forget()
		self.ShopProductPage.pack_forget()

	def BidAuction(self):
		self.BidProductPage.pack_forget()
		self.DelayProductPage.pack_forget()
		self.BidAuctionPage.pack()
		self.DelayAuctionPage.pack_forget()
		self.CreatLivePage.pack_forget()
		self.DeleTeProductPage.pack_forget()
		self.ShopProductPage.pack_forget()

	def DelayAuction(self):
		self.BidProductPage.pack_forget()
		self.DelayProductPage.pack_forget()
		self.BidAuctionPage.pack_forget()
		self.DelayAuctionPage.pack()
		self.CreatLivePage.pack_forget()
		self.DeleTeProductPage.pack_forget()
		self.ShopProductPage.pack_forget()

	def CreatLive(self):
		self.BidProductPage.pack_forget()
		self.DelayProductPage.pack_forget()
		self.BidAuctionPage.pack_forget()
		self.DelayAuctionPage.pack_forget()
		self.CreatLivePage.pack()
		self.DeleTeProductPage.pack_forget()
		self.ShopProductPage.pack_forget()

	def DLEProduct(self):
		self.BidProductPage.pack_forget()
		self.DelayProductPage.pack_forget()
		self.BidAuctionPage.pack_forget()
		self.DelayAuctionPage.pack_forget()
		self.CreatLivePage.pack_forget()
		self.DeleTeProductPage.pack()
		self.ShopProductPage.pack_forget()

	def ShopProduct(self):
		self.BidProductPage.pack_forget()
		self.DelayProductPage.pack_forget()
		self.BidAuctionPage.pack_forget()
		self.DelayAuctionPage.pack_forget()
		self.CreatLivePage.pack_forget()
		self.DeleTeProductPage.pack_forget()
		self.ShopProductPage.pack()