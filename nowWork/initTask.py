#!/usr/bin
#encoding=utf-8

import sys
import jTool



reload(sys)
sys.setdefaultencoding("utf-8")


#初始化任务表用，每个任务跑一次就可以


if __name__=='__main__':
    conn = jTool.initCursor('localhost', 'root', 'root', 'rawData')
    try:
        start = sys.argv[1]
        end = sys.argv[2]
        print 'start init in id ' + str(start)
        jTool.initTaskTable(conn, 'item_url', start, end)
    except:
        jTool.initTaskTable(conn, 'item_url')
