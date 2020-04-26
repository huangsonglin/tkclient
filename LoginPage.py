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
from GetFile import *
from api import *
from GetIp import GetIp
from GetFile import GetUserInfo

class LoginPage(object):


	def __init__(self, master=None):
		self.root = master  # 定义内部变量root
		sw = self.root.winfo_screenwidth()
		# 得到屏幕宽度
		sh = self.root.winfo_screenheight()
		self.root.geometry('%dx%d+%d+%d' % (461, 344, (sw-461)/2, (sh-344)/2))  # 设置窗口大小
		self.username = StringVar()
		self.password = StringVar()
		self.ip = GetIp().get_ip
		self.remember = BooleanVar()
		self.user_info = GetUserInfo().get_file
		self.createPage()


	def createPage(self):
		self.page = Frame(self.root)  # 创建Frame
		self.page.pack()
		Label(self.page, text='登录', font=("楷体", 20)).grid(row=2, rowspan=2, columnspan=5)
		Label(self.page, text='', font=("楷体", 12)).grid(row=0, stick=W)
		Label(self.page, text='', font=("楷体", 12)).grid(row=1, stick=W)
		Label(self.page, text='', font=("楷体", 12)).grid(row=2, stick=W)
		Label(self.page, text='', font=("楷体", 12)).grid(row=3, stick=W)
		Label(self.page, text='', font=("楷体", 12)).grid(row=4, stick=W)
		Label(self.page, text='账 户: ', font=("楷体", 12)).grid(row=5, stick=W, pady=10)
		name_entry = Entry(self.page, textvariable=self.username)
		name_entry.grid(row=5, column=1, stick=E)
		name_entry.insert(0, "请输入账号")
		Label(self.page, text='密 码: ', font=("楷体", 12)).grid(row=6, stick=W, pady=10)
		pwd_entry = Entry(self.page, textvariable=self.password, show='*')
		pwd_entry.grid(row=6, column=1, stick=E)
		pwd_entry.insert(0, "请输入密码")
		cbx = Checkbutton(self.page, variable=self.remember, text="记住我", onvalue=1, offvalue=0, command=self.auto_login)
		cbx.grid(row=7, stick=W, pady=10)
		Button(self.page, text='登 陆', command=self.loginCheck, font=("楷体", 12)).grid(row=8, stick=W, pady=10)
		Button(self.page, text='取 消', command=self.root.quit, font=("楷体", 12)).grid(row=8, column=1, stick=E)

	def auto_login(self, event=None):
		user = self.user_info
		if user['remeber']:
			self.username.set(user['username'])
			self.password.set(user['passwrod'])
		else:
			self.username.set("请输入账号")
			self.password.set("请输入密码")

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
				if rm:
					user_info = {"username": name, "passwrod": secret, "Authorization": Authorization,
								 "memberId": req.json()['id'], "remeber": rm}
				else:
					user_info = {"username": name, "passwrod": "", "Authorization": Authorization,
								 "memberId": req.json()['id'], "remeber": rm}
				GetUserInfo().wirte(json.dumps(user_info))
			else:
				showinfo(title='错误', message='账号或密码错误')
		else:
			showinfo(title='错误', message='账号或密码错误！')




