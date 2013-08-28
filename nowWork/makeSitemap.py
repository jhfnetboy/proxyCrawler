# -*-coding:utf-8 -*-
#encoding=utf-8

import sys
import jTool
import pycurl
import StringIO
import time

reload(sys)
sys.setdefaultencoding('utf-8')


'''
1.自动扫描网站，记录下各个功能入口url和介绍
2.从表中读取记录，生成html sitemap
3.生成xml sitemap
'''

def initMyCursor(db):
    host = 'localhost'
    user = 'root'
    passwd = 'root'
    conn = jTool.initCursor(host, user, passwd, db)
    return conn    


#def scanSite(beginUrl, depth, conn):
#    '''
#    扫描网站，记录表
#    '''
##    c = pycurl.Curl()
##    c.setopt(pycurl.URL, str(beginUrl))
##    b = StringIO.StringIO()
##    c.setopt(pycurl.TIMEOUT, 20)
##    c.setopt(pycurl.CONNECTTIMEOUT, 20)
##    c.setopt(pycurl.WRITEFUNCTION, b.write)
##    c.setopt(pycurl.FOLLOWLOCATION, 1)
##    c.setopt(pycurl.MAXREDIRS, 5)
##    c.perform()
##    content = b.getvalue()
##    jTool.logit(content, '888.txt')
##    print content
#    content = open('888.txt').read()
#    exp = '//a'
#    aList = jTool.getNodes(content, exp)
#    count = len(aList)
#    fieldDic = {}
#    
#    table = 'siteUrl'
#    cursor = conn.cursor()
#    
#    for i in range(count):
#        href = aList[i].xpath('@href')[0]
##        print aList[i].xpath('text()')[0]
##        print aList[i].xpath('@href')[0]
#        if 'javascript' not in href:
#            fieldDic['text'] = aList[i].xpath('text()')[0]
#            fieldDic['url'] = aList[i].xpath('@href')[0]
#            fieldDic['depth'] = depth
#            fieldDic['ctime'] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))       
#            jTool.insertDatai(cursor, table, fieldDic)
#            fieldDic = {}
#            conn.commit()
#        
#    cursor.close()
#    conn.close()


#beginUrl = 'http://www.bss360.com'
#include = 'bss360'
#scanSite(beginUrl, '1')



#def mainLoop(beginUrl, depth, include):
#    while depth>0:
#        scanSite(beginUrl, include)
#        depth = depth - 1
#
#
#if __name__=='__main__':
#        print '*'*50
#        print 'run like this :python makeSitemap.py beginUrl depth include'
#        print 'include seprate by comma,like this: www,/sitemap,www.xxxx.com'
#        print '*'*50
#        beginUrl = sys.argv[1]
#        depth =  sys.argv[2]
#        exceptStr =  sys.argv[3]
#        mainLoop(beginUrl, int(depth), exceptStr)


#def genFile(conn, table, start, end,urlTemp):
#    '''
#    直接根据信息数据库生产sitemap
#    此功能放弃，以XML函数为主
#    '''
#    baseFileHead = '''<HTML><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
#                    <meta name="author" content="SitemapX.com" />
#                    <meta name="robots" content="index,follow" />
#                    <title>HTML SiteMap</title></head><body><h1>浙江商安信息科技有限公司 sitemap HTML</h1><br/>'''
#    baseFileEnd = '<body></HTML'
#    file = open('sitemap.html', 'a')
#    file.write(baseFileHead)
#    
#    cursor = conn.cursor()
#    id = start
#    while id>=start and id<=end:
#        sql = 'select title from '+ table +' where id = '+str(id)
#        cursor.execute(sql)
#        record = cursor.fetchone()         
#        if not record:
#            id += 1
#            continue
#        
#        print record[0].decode('utf-8')
#        aStr = "<a href='"+urlTemp+str(id)+"'>"+'浙江商安  '+record[0].decode('utf-8')+' 商安卫士'+'</a><br/>'
#        file.write(aStr)
#        id += 1
##    file.write(baseFileEnd)
#    file.close()
#    cursor.close()
    


#conn = initMyCursor('bss360_dev')
#genFile(conn, 'enterprise', 1, 22000, 'http://www.bss360.com/news/show/')


def genFileXML(conn, table, start, end, urlTemp, xmlName):
    '''
    生成XML格式的sitemap
    '''
    baseFileHead = '''<?xml version="1.0" encoding="UTF-8"?>
                    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                    '''
    file = open(xmlName, 'a')
    file.write(baseFileHead)
    
    cursor = conn.cursor()
    id = start
    while id>=start and id<=end:
        sql = 'select name, createdTime from '+ table +' where id = '+str(id)
        cursor.execute(sql)
        record = cursor.fetchone()         
        if not record:
            id += 1
            continue
        
        print record[0].decode('utf-8')
        ltime=time.localtime(record[1])
        lastMod=time.strftime("%Y-%m-%dT%H:%M:%SZ", ltime)        
        uStr = '''<url>
                  <loc>'''+urlTemp+str(id)+'''</loc>
                  <lastmod>'''+lastMod+'''</lastmod>
                  <changefreq>monthly</changefreq>
                  <priority>1</priority>   
                </url>'''
        file.write(uStr)
        id += 1
    file.write('</urlset>')
    file.close()
    cursor.close()

'''
截至企业到20000
截至资讯到20712(7-20左右，最新）
'''

conn = initMyCursor('bss360_dev')

#baseUrl = 'http://www.bss360.com/news/show/'
#genFileXML(conn, 'article', 1, 20713, )


baseUrl = 'http://www.bss360.com/enterprise/'
start = 20000
end = 30000
table = 'enterprise'
xmlName = 'sitemap4.xml'
genFileXML(conn, table, start, end, baseUrl, xmlName)


