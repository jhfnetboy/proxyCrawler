#!/usr/bin
#encoding=utf-8

import sys
import rp
import jTool
import random


reload(sys)
sys.setdefaultencoding("utf-8")


def makeParam():
    paramDic = {}
    paramDic['station'] = '信用浙江'
    paramDic['begin_url'] = 'http://www.zjcredit.gov.cn:8000/CreditQuery.aspx?sectionID=02'
    paramDic['query_url'] = 'http://www.zjcredit.gov.cn:8000/ListQuery.aspx'
    paramDic['post_data_dic'] = {'isIntermediary': 'False', 'isOpen': 'False', 'pageLength': '20', 'recordTotal': '1778190', 'sectionID': '02', 'sortDirection': '1', 'sortField': 'CreditID'}
    paramDic['preUrl'] = 'http://www.zjcredit.gov.cn:8000/EnterpriseInfo.aspx?creditID='
    paramDic['preUrlip'] = 'http://218.108.28.28:8000/EnterpriseInfo.aspx?creditID='
    paramDic['basePostUrl'] = 'http://www.zjcredit.gov.cn:8000/GetInfoByDataSupplier.aspx'
    paramDic['basePostUrlip'] = 'http://218.108.28.28:8000/GetInfoByDataSupplier.aspx'
    paramDic['dbHost'] = 'localhost'
    paramDic['dbUser'] = 'root'
    paramDic['dbPasswd'] = 'root'
    paramDic['rdb'] = 'rawData'
    conn = jTool.initCursor(paramDic['dbHost'], paramDic['dbUser'], paramDic['dbPasswd'], paramDic['rdb'])
    paramDic['conn'] = conn
    return paramDic


def operLog(logFileName):
    file = open(logFileName)
    line = file.readline()
    param = makeParam()
    param['taskTable'] = 'item_url_task'
    param['num'] = '999'
    proxyList = jTool.getProxy('proxy.txt')
    pcount = len(proxyList)-1
    proxy = proxyList[random.randint(0, pcount)]
    while line:
        if line[0]=='G':
            tmp = line.split(',')
            for t in tmp:
                tt = t.split(':')
                if len(tt)>1:
                    param[tt[0].strip()] = tt[1]
                    if len(tt)>2:
                        param[tt[0]] = tt[1]+':'+tt[2]+':'+tt[3].strip('\n')
            param['id'] = param['eid']
            rp.crawlUrl(param['conn'], param, proxy)
        if line[0]=='P':
#            print line
            pass
        line = file.readline()


if __name__=='__main__':
    if sys.argv[1]:
        logFileName = sys.argv[1]
        operLog(logFileName)
    else:
        print 'Run like this: python operLog.py error.log'
