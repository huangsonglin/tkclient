#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2020/1/20 14:52'

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from tkinter import *
import tkinter as tk
from tkinter.messagebox import showinfo,showerror,showwarning   # 各种类型的提示框
from tkinter.tix import *
import hashlib
import requests
import time
import pymysql

# 初始化
# window = tk.Tk()
# sh = window.winfo_screenheight()
# sw = window.winfo_screenwidth()
# ww = wh = 400
# x = (sw-ww) / 2
# y = (sh-wh) / 2
# window.title(u'欢迎来到龖藏')
# window.geometry("%dx%d+%d+%d" %(ww,wh,x,y))
# window.resizable(width=False, height=False)
#
# # welcome image
# canvas = tk.Canvas(window, height=500, width=500)
# image_file = tk.PhotoImage(file='bround.png')
"""
说明：控制按钮上内容的位置。使用N, NE, E, SE, S, SW, W, NW, or CENTER这些值之一。默认值是CENTER。
"""
# image = canvas.create_image(200, 80, anchor='center', image=image_file)
# canvas.pack(side='top')
#
# # user information
# tk.Label(window, text="CountryCode: ").place(x=50, y=130)
# tk.Label(window, text='Phone: ').place(x=50, y=170)    # 标签控件
# tk.Label(window, text='Password: ').place(x=50, y=210)
# tk.Label(window, text='Nikename: ').place(x=50, y=250)
#
# var_usr_code = tk.StringVar()
# var_usr_code.set('请输入国际区号')
# entry_usr_code = tk.Entry(window, textvariable=var_usr_code)
# entry_usr_code.place(x=160, y=130)
# var_usr_name = tk.StringVar()   # 绑定标签变量
# var_usr_name.set('输入11位手机号码')
# entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
# entry_usr_name.place(x=160, y=170)
# var_usr_pwd = tk.StringVar()
# var_usr_pwd.set('请输入6-11位密码')
# entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
# entry_usr_pwd.place(x=160, y=210)
# var_usr_nkn = tk.StringVar()
# var_usr_nkn.set('请输入昵称')
# enter_usr_nkn = tk.Entry(window, textvariable=var_usr_nkn)
# enter_usr_nkn.place(x=160, y=250)
# tk.mainloop()

st = "P_T_01:造像,P_T_02:唐卡,P_T_03:法器,P_T_04:古珠,P_T_05:杂项,P_T_07:综合,P_T_06:设计,P_T_08:古玉"
print(st.split(","))