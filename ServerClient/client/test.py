# -*-coding: utf-8 -*-
#encoding=utf-8

import sys


reload(sys)
sys.setdefaultencoding("utf-8")

print "脚本名：", sys.argv[0]
num = sys.argv[1]

print 'i get your num :'+str(num)