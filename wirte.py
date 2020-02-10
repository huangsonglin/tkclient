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

def wirte(result):
	with open(os.path.join(curPath, "user_info"), 'w+') as file:
		file.write(result)

def get_file():
	fp  = open(os.path.join(curPath, "user_info"), 'r')
	result = fp.readlines()[0]
	result = json.loads(result)
	return result


