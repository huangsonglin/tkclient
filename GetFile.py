#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2020/1/17 17:51'

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import json
import re

class GetUserInfo():

	def __init__(self):
		self._filename = os.path.join(curPath, "user_info")

	def wirte(self, result):
		with open(self._filename, 'w+') as file:
			file.write(result)

	@property
	def get_file(self):
		fp  = open(self._filename, 'r')
		result = fp.readlines()[0]
		result = json.loads(result)
		return result

	@staticmethod
	def filter_emoji(desstr, restr=''):
		# 过滤表情
		try:
			co = re.compile(u'[\U00010000-\U0010ffff]')
		except re.error:
			co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
		return co.sub(restr, desstr)


class GetConfig():

	def __init__(self):
		self._file = os.path.join(curPath, "config.js")

	@property
	def get_txt(self):
		f = open(self._file, encoding="utf-8", errors='ignore')
		config = json.load(f)
		return config

import random
class GetName():

	def __init__(self):
		self._file = os.path.join(curPath, "name")

	@property
	def _name(self):
		f = open(self._file, encoding="utf-8", errors='ignore')
		return random.choice(f.readlines())



