#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2020/4/20 11:12'

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import socket



class GetIp(object):

	def __init__(self):
		self._ip = socket.gethostname()

	@property
	def get_ip(self):
		return self._ip

