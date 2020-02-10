#!user/bin/python
# -*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2020/1/20 11:38'

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import tkinter as tk
from tkinter import *
from LoginPage import *

root = tk.Tk()
root.resizable(width=False, height=False)
root.title('龖藏测试工具')
LoginPage(root)
root.mainloop()
