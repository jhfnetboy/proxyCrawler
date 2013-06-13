# -*-coding:utf-8 -*-
#encoding=utf-8

import sys
import jTool
import time
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


def doTask(task, param, proxy):
    param['id'] = str(task[0])
    param['url'] = param['preUrlip'] + task[1]
    param['ename'] = task[2]
#    try:
    return rp.crawlUrl(param['conn'], param, proxy)
#    except:
#        print 'crawlUrl failed '+param['url']
#        jTool.logError('\ncrawlUrl failed '+param['url'])
#        return True


def completeTask(param, id):
    upSql = 'update '+param['taskTable']+' set status = 1 where id = '+str(id)
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
    querySql = 'select id, url, enterprise_name from '+param['taskTable']+' where id >= '+str(start)+' and id <= '+ str(end)
    cursor = param['conn'].cursor()
    cursor.execute(querySql)
    proxyList = jTool.getProxy('proxy.txt')
    pcount = len(proxyList)-1
    proxy = proxyList[random.randint(0, pcount)]
    while start<end:
        record = cursor.fetchone()
        task = list(record)
        print 'Get new task on '+ str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        result = doTask(task, param, proxy)
        count += 1
        print count
        ids = ''
        if result:
            completeTask(param, task[0])
            start += 1
            continue
        if not result:
            rollbackTask(param, task[0])
            start += 1
            continue
    cursor.close()
    param['conn'].close()


if __name__=='__main__':
        print '*'*50
        print '请在末尾+空格+分配给你的id号，一般每台机器最多开20个进程\n你的id范围就是1-20,每个进程固定输入一个，如1或2'
        print '例如： dClient 2'
        print '*'*50
        num = sys.argv[1]
        start = sys.argv[2]
        end = sys.argv[3]
        mainLoop(num, int(start), int(end))
