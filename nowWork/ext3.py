#!/usr/bin
#encoding=utf-8

import sys
import jTool
import extLib


reload(sys)
sys.setdefaultencoding("utf-8")


#对enterprise_record_raw enterprise_raw的相关字段操作，提取，清洗，转换数据
#数据会还在对应表保存，完善后可以添加数据转换功能，替代php脚本，完成字段转换和默认值填充

def enterprise_record_raw_function(conn, start, end):
    print 'hi'

if __name__=='__main__':
    print '*'*50
    print 'Run like this : python ext2.py enterprise_raw  1 10'
    print 'now accept enterprise_raw,enterprise_record_raw'
    print '*'*50
    conn = jTool.initCursor('localhost', 'root', 'root', 'rawData')
    table = sys.argv[1]
    try:
        start = sys.argv[2]
        end = sys.argv[3]
    except:
        start = 1
        end = 1000000
extLib.extractPostContent(conn, table, start, end)

