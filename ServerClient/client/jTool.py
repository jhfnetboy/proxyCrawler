# -*-coding: utf-8 -*-
#encoding=utf-8

import sys

import time
import urllib
import pycurl
import StringIO
import lxml.html as HTML

reload(sys)
sys.setdefaultencoding("utf-8")


def logit(content, filename='log.txt'):
    '''
    逐行添加日志,需要回车自己加‘\n’
    '''
    file = open(filename, 'a')
    try:
        file.write(content)
    finally:
        file.close()


def logError(content):
    '''
    记录错误日志
    '''
    timestr = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    logit(content, 'error.log')


def initCursor(host, user, passwd, db):
    import MySQLdb
    conn = MySQLdb.connect(host, user, passwd, charset="utf8")
    conn.select_db(db)
    return conn


def getProxy(proxyfilename):
    '''
    获得所有的list proxy
    '''
    file = open(proxyfilename)
    list = []
    for line in file:
        proxy = line.split('@')
        list.append(proxy[0])
    return list


def fetchUrl(url, post_data_dic = None, method = 'get'):
    content = None
    MAX_FECHPAGE_PER_TIME = 60
    CONNECT_TIMEOUT = 60
    c = pycurl.Curl()
    c.setopt(pycurl.URL, str(url))
    b = StringIO.StringIO()
    c.setopt(pycurl.TIMEOUT, MAX_FECHPAGE_PER_TIME)
    c.setopt(pycurl.CONNECTTIMEOUT, CONNECT_TIMEOUT)
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    head = ['Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset:GBK,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding:gzip,deflate,sdch',
            'Accept-Language:zh-CN,zh;q=0.8',
            'Cache-Control:no-cache',
            'Connection:keep-alive',
            'Cookie:lzstat_uv=1478958657197807570|2529639; ASP.NET_SessionId=izva2jmqq5iwzwnw1sjjzu55; _gscu_374314293=69618676a80oei18; _gscs_374314293=t70343786g6j4wf14|pv:8; _gscbrs_374314293=1; lzstat_ss=3816338630_7_1370374534_2529639; ECStaticSession=ECS81',
            'Host:www.zjcredit.gov.cn:8000',
            'Pragma:no-cache',
            'User-Agent:Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.22 (KHTML, like Gecko) Ubuntu Chromium/25.0.1364.160 Chrome/25.0.1364.160 Safari/537.22'
            ]
    c.setopt(pycurl.HTTPHEADER, head)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    if(method == 'post'):
        c.setopt(c.POSTFIELDS, urllib.urlencode(post_data_dic))
    try:
        c.perform()
        content = b.getvalue()
    except:
        print '   Fail with Http code :'+ str(c.getinfo(c.HTTP_CODE))
    finally:
        return content


def fetchUrlProxy(proxy, url, post_data_dic = None, method = 'get'):
    content = None
    MAX_FECHPAGE_PER_TIME = 60
    CONNECT_TIMEOUT = 60
    c = pycurl.Curl()
    c.setopt(pycurl.URL, str(url))
    b = StringIO.StringIO()
    c.setopt(pycurl.TIMEOUT, MAX_FECHPAGE_PER_TIME)
    c.setopt(pycurl.CONNECTTIMEOUT, CONNECT_TIMEOUT)
    c.setopt(pycurl.PROXY, proxy)
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    if(method == 'post'):
#        head = ['Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#                'Accept-Charset:GBK,utf-8;q=0.7,*;q=0.3',
#                'Accept-Encoding:gzip,deflate,sdch',
#                'Accept-Language:zh-CN,zh;q=0.8',
#                'Cache-Control:no-cache',
#                'Connection:keep-alive',
#                'Cookie:lzstat_uv=1478958657197807570|2529639; ASP.NET_SessionId=izva2jmqq5iwzwnw1sjjzu55; _gscu_374314293=69618676a80oei18; _gscs_374314293=t70343786g6j4wf14|pv:8; _gscbrs_374314293=1; lzstat_ss=3816338630_7_1370374534_2529639; ECStaticSession=ECS81',
#                'Host:www.zjcredit.gov.cn:8000',
#                'Pragma:no-cache',
#                'User-Agent:Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.22 (KHTML, like Gecko) Ubuntu Chromium/25.0.1364.160 Chrome/25.0.1364.160 Safari/537.22'
#                ]
#        c.setopt(pycurl.HTTPHEADER, head)  
        agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.22 (KHTML, like Gecko) Ubuntu Chromium/25.0.1364.160 Chrome/25.0.1364.160 Safari/537.22'
        c.setopt(pycurl.USERAGENT, agent)
        c.setopt(c.POSTFIELDS, urllib.urlencode(post_data_dic))
    try:
        c.perform()
        content = b.getvalue()
        if(method == 'post'):
            print content
    except:
        print '   Fail with Http code :'+ str(c.getinfo(c.HTTP_CODE))
    finally:
        return content


def getContent(url, post_data_dic = None, MAX_TRY_TIME=3, codec=None):
    '''
    根据给定的url，获取内容
    返回的是预先解码的内容
    '''
    i = 1
    content = None
    while i<=MAX_TRY_TIME:
        print 'connect url '+url
        print '    Try No. '+str(i) +' time to fetch page'
        i += 1
        try:
            if(post_data_dic):
                print 'post'
                content = fetchUrl(str(url), post_data_dic, 'post')
            else:
                print 'get'
                content = fetchUrl(str(url))
        except:
            print 'Fail this time '
            logError('Fail to get url: '+url)
        finally:
            return content


def getContentByProxy(proxy, url, post_data_dic = None, MAX_TRY_TIME=3, codec=None):
    '''
    根据给定的url，获取内容
    返回的是预先解码的内容
    '''
    i = 1
    content = None
    while i<=MAX_TRY_TIME:
        print 'connect url '+url+ ', with proxy '+ str(proxy)
        print '    Try No. '+str(i) +' time to fetch page'
        i += 1
#        try:
        if(post_data_dic):
            print 'post'
            content = fetchUrlProxy(proxy, str(url), post_data_dic, 'post')
        else:
            print 'get'
            content = fetchUrlProxy(proxy, str(url))
#        except:
#            print 'Fail this time '
#            logError('Fail to get url: '+url)
#        finally:
        return content


def getNodes(content, exp):
    '''
    lxml.xpath方式获取所有符合表达式的
    html节点，以列表方式返回
    '''
    tnodes = None
    try:
        root = HTML.document_fromstring(content.decode('UTF-8', 'ignore'))
        tnodes = root.xpath(exp)
    except:
        pass
    finally:
        return tnodes


def getStrIndex(str, content):
    if str in content:
        return content.find(str)
    return -1


def removeBetween(begin, end, clength, tagEnd, content):
    return content[0:begin]+content[end+len(tagEnd):clength]


def getBetween(begin, end, tagHead, content):
    return content[begin+len(tagHead):end]


def getBefore(start, content):
    return content[0:start]


def getAfter(start, tag, content):
    return content[start+len(tag):len(content)]


def clearX(list, rec):
    for char in list:
        rec = "".join(rec.split(char))
    return rec


def initConfig(filename):
    '''
    去掉文件头BOM等
    Window下用记事本打开配置文件并修改保存后，编码为UNICODE
    或UTF-8的文件的文件头
    #会被相应的加上\xff\xfe（\xff\xfe）或\xef\xbb\xbf
    '''
    import re
    try:
        content = open(filename).read()
        content = re.sub(r"\xfe\xff", "", content)
        content = re.sub(r"\xff\xfe", "", content)
        content = re.sub(r"\xef\xbb\xbf", "", content)
        open(filename, 'w').write(content)
    except:
        print "Read config file :"+filename+' failed,pls check'


def getConfigParam(paramList, configFileName, area = "global"):
    '''
    从指定配置文件中的指定区域读取指定list名称的变量，dic 返回
    '''
    initConfig(configFileName)
    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.read(configFileName)
    rtDic = {}
    for param in paramList:
        rtDic[param] = config.get(area, param)
    return rtDic


def getErrorPageNumList(errorLogFileName):
    '''
    默认error log 中以 ： 隔开正文和num
    返回list ,多个num
    '''
    import os
    list = []
    try:
        file = open(errorLogFileName)
        for line in file:
            errorNum = line.split(':')[1]
            list.append(int(errorNum))
        file.close()
        os.remove(errorLogFileName)
        return list
    except:
        print 'Fail to read error log to recover'
        return list


def insertData(cursor, table, fieldDic):
    '''
    用给定字典生成sql并执行，所有字段都是varchar,数字等其他暂不支持
    '''
    fields = list(fieldDic.keys())
    values = list(fieldDic.values())
    fs = ','.join(fields)
    vs = "'"+"','".join(values) + "'"
    IstSql = 'insert into '+ table + ' ('+ fs +') values(' + vs +')'
    return cursor.execute(IstSql)


def updateData(cursor, where, table, fieldDic):
    '''
    用给定字典生成sql并执行，所有字段都是varchar,数字等其他暂不支持
    '''
    fCount = len(fieldDic)
    list = []
    for (k, v) in fieldDic.items():
        list.append(k+'='+"'"+v+"'")
    setStr = ', '.join(list)
    upSql = 'update '+ table + ' set ' + setStr + where
    return cursor.execute(upSql)


'''
在跑server之前，要先跑这个，初始化记录表，生成任务表
'''


def initTaskTable(conn, sourceTableName):
    '''
    把待爬行的源表记录生成到任务表，任务表id,iid,status,owner(分配给谁了，记录ip）
    '''
    paramDic = getConfigParam(['host', 'user', 'passwd', 'db'], 'server.ini')
    conn = initCursor(paramDic['host'], paramDic['user'], paramDic['passwd'], paramDic['db'])
    cursor = conn.cursor()
    cursor2 = conn.cursor()
    sql = 'select id, status, item_url, eid, enterprise_name from '+sourceTableName
    cursor.execute(sql)
    while 1:
        record = cursor.fetchone()
        if not record:
            break
        recDic = {}
        recDic['status'] = '-1'
        if int(record[1]) == 0:
            recDic['iid'] = str(record[0])
            recDic['url'] = record[2].split('=')[1]#只适用信用浙江的企业查询
            recDic['eid'] = str(record[3])
            recDic['enterprise_name'] = str(record[4])
            insertData(cursor2, sourceTableName+'_task', recDic)
            print 'insert '+str(record[0])
        conn.commit()
    cursor.close()
    conn.close()

#初始化任务表用，每个任务跑一次就可以
#paramDic = getConfigParam(['host', 'user', 'passwd', 'db', 'oprateTable'], 'server.ini')
#conn = initCursor(paramDic['host'], paramDic['user'], paramDic['passwd'], paramDic['db'])
#initTaskTable(conn, 'item_url')


#url = 'http://www.zjcredit.gov.cn:8000/EnterpriseInfo.aspx?creditID=547A4A9A1F0F5D1B27B162943B5C562B'
#url = 'http://218.108.28.28:8000/EnterpriseInfo.aspx?creditID=547A4A9A1F0F5D1B27B162943B5C562B'
#url = 'http://www.baidu.com'
#pList = getProxy('proxy.txt')
#pcount = len(pList)-1
#proxy = pList[random.randint(0,pcount)]
#content = fetchUrlProxy(proxy, url)
