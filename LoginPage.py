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
import time
from tkinter import *
from tkinter.messagebox import *
from MainPage import *
from wirte import wirte
from api import *
import socket

class LoginPage(object):
	def __init__(self, master=None):
		self.root = master  # 定义内部变量root
		sw = self.root.winfo_screenwidth()
		# 得到屏幕宽度
		sh = self.root.winfo_screenheight()
		self.root.geometry('%dx%d+%d+%d' % (461, 344, (sw-461)/2, (sh-344)/2))  # 设置窗口大小
		self.username = StringVar()
		self.password = StringVar()
		self.ip = socket.gethostname()
		value = localRedis.get(f"TK_NUMBER:{self.ip}")
		if value != None:
			rm_dict = json.loads(value.decode())
			rm = rm_dict['remeber']
			if rm:
				self.username.set(rm_dict['username'])
				self.password.set(rm_dict['password'])
			else:
				self.username.set("输入11位手机号码")
				self.password.set("请输入密码")
		else:
			self.username.set("输入11位手机号码")
			self.password.set("请输入密码")
		self.remember = BooleanVar()
		self.createPage()


	def createPage(self):
		self.page = Frame(self.root)  # 创建Frame
		self.page.pack()
		Label(self.page, text='', font=("楷体", 12)).grid(row=0, stick=W)
		Label(self.page, text='', font=("楷体", 12)).grid(row=1, stick=W)
		Label(self.page, text='', font=("楷体", 12)).grid(row=2, stick=W)
		Label(self.page, text='', font=("楷体", 12)).grid(row=3, stick=W)
		Label(self.page, text='', font=("楷体", 12)).grid(row=4, stick=W)
		Label(self.page, text='账 户: ', font=("楷体", 12)).grid(row=5, stick=W, pady=10)
		self.NAME = Entry(self.page, textvariable=self.username).grid(row=5, column=1, stick=E)
		Label(self.page, text='密 码: ', font=("楷体", 12)).grid(row=6, stick=W, pady=10)
		self.PWD = Entry(self.page, textvariable=self.password, show='*').grid(row=6, column=1, stick=E)
		cbx = Checkbutton(self.page, variable=self.remember, text="记住我", onvalue=1, offvalue=0)
		cbx.grid(row=7, stick=W, pady=10)
		Button(self.page, text='登 陆', command=self.loginCheck, font=("楷体", 12)).grid(row=8, stick=W, pady=10)
		Button(self.page, text='取 消', command=self.root.quit, font=("楷体", 12)).grid(row=8, column=1, stick=E)

	def loginCheck(self):
		name = self.username.get()
		secret = self.password.get()
		rm = self.remember.get()
		if name != "" and secret != "":
			req = login(name, secret)
			if req.status_code == 200:
				self.page.destroy()
				MainPage(self.root)
				Authorization = 'Bearer ' + req.json()['accessToken']
				user_info = {"username": name, "Authorization": Authorization, "memberId": req.json()['id']}
				localRedis.set(name=f"TK_NUMBER:{self.ip}",
							   value=json.dumps({"username": name, "password": secret, "remeber": rm, "wip":self.ip,
									  "loginTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}))
				wirte(json.dumps(user_info))
			else:
				showinfo(title='错误', message='账号或密码错误！')
		else:
			showinfo(title='错误', message='账号或密码错误！')


	def auto_name(self):
		value = localRedis.get(f"TK_NUMBER:{self.ip}")
		if value != None:
			rm_dict = json.loads(value.decode())
			rm = rm_dict['remeber']
			if rm:
				self.username.set(rm_dict['username'])

	def auto_pwd(self):
		value = localRedis.get(f"TK_NUMBER:{self.ip}")
		if value != None:
			rm_dict = json.loads(value.decode())
			rm = rm_dict['remeber']
			if rm:
				self.password.set(rm_dict['password'])


