#!user/bin/python
# -*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2020/1/10 17:33'

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import redis
import json

f = open(os.path.join(curPath, "config.js"), encoding="utf-8", errors='ignore')
config = json.load(f)
config = config[0]
host = config['redis_host']
localRedis = redis.StrictRedis(host=host, password="123456")

