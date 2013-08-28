#!/usr/bin
#encoding=utf-8

import sys
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
    cursor = param['conn'].cursor()
    cursor2 = param['conn'].cursor()
    cursor3 = param['conn'].cursor()
    count = 0
    while line:
        tmp = line.split(',')
        if len(tmp)>2:
            for t in tmp:
                tt = t.split(':')
                if len(tt)>1:
                    param[tt[0].strip()] = tt[1]
                    if len(tt)>3:
                        param[tt[0]] = tt[1]+':'+tt[2]+':'+tt[3].strip('\n')
            for i in range(10):
                ext = jTool.exsitsRecord(cursor, 'enterprise_raw_'+str(i), 'eid', param['id'])
                i += 1
                if not ext:
                    jTool.insertDatai(cursor, 'error_log', {'eid': param['id'], 'url': param['url'], 'ename': param['ename']})
                    print  str(param['id'])
                else:
                    try:
                        if ext!='error':
                            jTool.getField(cursor2, 'enterprise_raw_'+str(i), 'postContent', ' where eid = '+str(param['id']))
                            val = cursor2.fetchone()
                            if not val[0]:
                                jTool.insertDatai(cursor3, 'error_log', {'eid': param['id'], 'url': param['url'], 'ename': param['ename']})
                                print  str(param['id'])
                    except:
                        pass
            param['conn'].commit()
        line = file.readline()
        count += 1
    cursor.close()
    cursor2.close()
    cursor3.close()
    param['conn'].close()
    print 'line error :'+str(count)

if __name__=='__main__':
    if sys.argv[1]:
        logFileName = sys.argv[1]
        operLog(logFileName)
    else:
        print 'Run like this: python operLog.py error_log/error.log'
