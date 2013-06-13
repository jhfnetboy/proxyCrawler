# -*-coding: utf-8 -*-
#encoding=utf-8

import sys
import jTool

reload(sys)
sys.setdefaultencoding("utf-8")

#初始化任务表用，每个任务跑一次就可以

paramDic = jTool.getConfigParam(['host', 'user', 'passwd', 'db', 'initTable'], 'server.ini')
conn = jTool.initCursor(paramDic['host'], paramDic['user'], paramDic['passwd'], paramDic['db'])
jTool.initTaskTable(conn, paramDic['initTable'])