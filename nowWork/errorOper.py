# -*-coding:utf-8 -*-
#encoding=utf-8

import sys
import jTool
#import time
import rp
import random

reload(sys)
sys.setdefaultencoding('utf-8')


def makeParam(table):
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


def doTask(task, param):
    proxyList = jTool.getProxy('proxy.txt')
    pcount = len(proxyList)-1
    param['id'] = str(task[0])
#    param['url'] = param['preUrlip'] + task[1]
    param['url'] = task[1]
    param['ename'] = task[2]
    cursor = param['conn'].cursor()
    proxy = str(proxyList[random.randint(0, pcount)]).strip()
#    try:
    result = rp.crawlGetUrl(param['conn'], param, proxy)
    count = 1
    while not result['logic'] and count<=2:
            proxy = str(proxyList[random.randint(0, pcount)]).strip()
            result = rp.crawlGetUrl(param['conn'], param, proxy)
            count += 1
    if result['logic']:
        completeTask(param, task[3])
    if not result['logic']:
        print 'error record:'+ str(param['id'])
#    except Exception, e:
#        print 'doTask', __name__, e
#        return True
    param['conn'].commit()
    cursor.close()


def completeTask(param, id):
    upSql = 'update '+param['taskTable']+' set status = 1 where id = '+ str(id)
    cursor = param['conn'].cursor()
    cursor.execute(upSql)
    param['conn'].commit()
    cursor.close()


def rollbackTask(param, id):
    upSql = 'update '+param['taskTable']+' set status = -2 where id = '+str(id)
    cursor = param['conn'].cursor()
    cursor.execute(upSql)
    param['conn'].commit()
    cursor.close()


def mainLoop(table, start, end):
    param = makeParam(table)
    param['taskTable'] = table
    cursor = param['conn'].cursor()
    while start<=end:
        print start
        querySql = 'select eid, url, ename, id from '+param['taskTable']+' where id = '+str(start) +' and status = 0 limit 1'
        cursor.execute(querySql)
        record = cursor.fetchone()
        start += 1
        if not record:
            continue
        task = list(record)
        result = doTask(task, param)
    cursor.close()
    param['conn'].close()


if __name__=='__main__':
        print '*'*50
        print '例如： dClient tableName 1  100'
        print '*'*50
        table = sys.argv[1]
        start = sys.argv[2]
        end = sys.argv[3]
        mainLoop(table, int(start), int(end))
