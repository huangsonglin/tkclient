#!user/bin/python
# -*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2020/1/20 11:36'

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import json
from tkinter import *
from tkinter.messagebox import *
from MainPage import *
from wirte import wirte
from api import *

class LoginPage(object):
	def __init__(self, master=None):
		self.root = master  # 定义内部变量root
		sw = self.root.winfo_screenwidth()
		# 得到屏幕宽度
		sh = self.root.winfo_screenheight()
		self.root.geometry('%dx%d+%d+%d' % (461, 344, (sw-461)/2, (sh-344)/2))  # 设置窗口大小
		self.username = StringVar()
		self.username.set("输入11位手机号码")
		self.password = StringVar()
		self.password.set("请输入密码")
		self.createPage()


	def createPage(self):
		self.img = Frame(self.root)
		Label(self.img, text='').grid(row=0, stick=W)
		Label(self.img, text='').grid(row=1, stick=W)
		Label(self.img, text='欢迎使用工具', font=("楷体", 25)).grid(row=2, stick=W)
		self.img.pack()
		self.page = Frame(self.root)  # 创建Frame
		self.page.pack()
		Label(self.page, text='', font=("楷体", 12)).grid(row=0, stick=W)
		Label(self.page, text='账户: ', font=("楷体", 12)).grid(row=2, stick=W, pady=10)
		self.NAME = Entry(self.page, textvariable=self.username).grid(row=2, column=1, stick=E)
		Label(self.page, text='密码: ', font=("楷体", 12)).grid(row=3, stick=W, pady=10)
		self.PWD = Entry(self.page, textvariable=self.password, show='*').grid(row=3, column=1, stick=E)
		Button(self.page, text='登 陆', command=self.loginCheck, font=("楷体", 12)).grid(row=4, stick=W, pady=10)
		Button(self.page, text='取 消', command=self.root.quit, font=("楷体", 12)).grid(row=4, column=1, stick=E)

	def loginCheck(self):
		name = self.username.get()
		secret = self.password.get()
		if name != "" and secret != "":
			req = login(name, secret)
			if req.status_code == 200:
				self.page.destroy()
				MainPage(self.root)
				Authorization = 'Bearer ' + req.json()['accessToken']
				user_info = {"username": name, "Authorization": Authorization, "memberId": req.json()['id']}
				wirte(json.dumps(user_info))
			else:
				showinfo(title='错误', message='账号或密码错误！')
		else:
			showinfo(title='错误', message='账号或密码错误！')



