# -*-coding:utf-8 -*-
#encoding=utf-8

import sys
import jTool
#import time
import rp
import random

reload(sys)
sys.setdefaultencoding('utf-8')


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


def doTask(task, param):
    proxyList = jTool.getProxy('proxy.txt')
    pcount = len(proxyList)-1
    param['id'] = str(task[0])
    param['url'] = param['preUrlip'] + task[1]
    param['ename'] = task[2]
    cursor = param['conn'].cursor()
    proxy = str(proxyList[random.randint(0, pcount)]).strip()
#    try:
    result = rp.crawlGetUrl(param['conn'], param, proxy)
    count = 1
    while not result['logic'] and count<=2:
            proxy = str(proxyList[random.randint(0, pcount)]).strip()
            result = rp.crawlGetUrl(param['conn'], param, proxy)
#            result = rp.crawlPostUrl(param['conn'], param, proxy)
            count += 1
#        if result['logic']:#insertId
#            print 'id:'+str(result['rtData'])
#            param['rid'] = result['rtData']
#            result2 = rp.crawlPostUrl(param['conn'], param, proxy)
#            count2 = 1
#            while not result2['logic'] and count2<=2:
#                result = rp.crawlPostUrl(param['conn'], param, proxy)
#                count2 += 1
#            if result2['logic']:
#                return True                          
#            if not result['logic']:
#                result2['rtData']['eid'] = param['id']
#                result2['rtData']['url'] = param['url']
#                result2['rtData']['ename'] = param['ename']
#                result2['rtData']['proxy'] = proxy.strip()
#                jTool.insertDatai(cursor, 'error_log', result2['rtData'])
    if result['logic']:
        completeTask(param, param['iid'])
    if not result['logic']:
        result['rtData']['eid'] = param['id']
        result['rtData']['url'] = param['url']
        result['rtData']['ename'] = param['ename']
        result['rtData']['proxy'] = proxy.strip()
        jTool.insertDatai(cursor, 'error_log_1', result['rtData'])
        print 'error record:'+ str(param['id'])
#    except Exception, e:
#        print 'doTask', __name__, e
#        return True
    param['conn'].commit()
    cursor.close()


def completeTask(param, id):
    upSql = 'update '+param['taskTable']+' set status = 1 where id = '+str(id)
    cursor = param['conn'].cursor()
    cursor.execute(upSql)
    param['conn'].commit()
    cursor.close()
    

def completeTask2(param, id):
    upSql = 'update '+param['taskTable']+' set status = 2 where id = '+str(id)
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


def mainLoop(num, start, end):
    param = makeParam()
    param['taskTable'] = 'item_url_task'
    param['num'] = str(num)
    count = 0
    cursor = param['conn'].cursor()
    while start<=end:
        querySql = 'select eid, url, enterprise_name from '+param['taskTable']+' where id = '+str(start)+' and status = 0 limit 1'
        cursor.execute(querySql)
        record = cursor.fetchone()
        print start
        param['iid'] = start
        start += 1
        if not record:
            continue
        task = list(record)
        result = doTask(task, param)
        count += 1
#        if result:
##            completeTask(param, task[0])
#            continue
#        if not result:
##            rollbackTask(param, task[0])
#            continue
    cursor.close()
    param['conn'].close()


if __name__=='__main__':
        print '*'*50
#        print '请在末尾+空格+分配给你的id号，一般每台机器最多开20个进程\n你的id范围就是1-20,每个进程固定输入一个，如1或2'
        print '例如： dClient 1  100'
        print '*'*50
        num = 1
        start = sys.argv[1]
        end = sys.argv[2]
        mainLoop(num, int(start), int(end))
