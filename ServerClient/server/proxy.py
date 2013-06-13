# -*-coding: utf-8 -*-
#encoding=utf-8
import sys
import jTool
import pycurl
import StringIO
import time

reload(sys)
sys.setdefaultencoding("utf-8")


def testProxy(proxy, url):
    content = None
    try:
        proxy = proxy if sys.argv[1] else proxy
        start = time.time()
        print 'begin to test proxy:'+ proxy.strip('\n') +','+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) +', '+ str(start)
        c = pycurl.Curl()
        c.setopt(pycurl.URL, url)
        b = StringIO.StringIO()
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.MAXREDIRS, 5)
        c.setopt(pycurl.PROXY, proxy)
        content = None
        try:
            c.perform()
            spend = time.time()-start
            print spend
            content = b.getvalue()
            return content
        except:
            print 'proxy failed'
    except:
        print 'This is a proxy test tool\ninput like:tp 220.15.23.98:80'
        print 'will write to proxy.txt'

#url = 'http://www.zjcredit.gov.cn:8000/EnterpriseInfo.aspx?creditID=A10C28F1BE28EEFA'
url = 'http://www.baidu.com'
file = open('proxy.txt')
for line in file:
    proxy = line.split('@')
    content = testProxy(proxy[0].strip('\n'), url)
    print content
    print proxy[0]
    if content:
        jTool.logit(str(proxy[0]), 'proxy.pre')
    print '\n\n\n'
print 'ok'