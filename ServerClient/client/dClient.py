# -*-coding:utf-8 -*-
#encoding=utf-8

import sys
import jTool
import time
import rp

reload(sys)
sys.setdefaultencoding('utf-8')

version = '0.1'
introduce = 'It is a base frame work to communicate with dServer'


class baseClient:

    def __init__(self, host, num):
        self.host = host
        self.num = num

    def connect(self):
        result = {}
        try:
            result = jTool.fetchUrl(self.host)
            result = eval(result)
            if result['status'] != 'ok':
                print 'Fail to connect Server:'+self.host
                return False
            print self.host +':'+ result['msg']
            return True
        except:
            print 'Fail to connect Server:'+self.host
            return False

    def getMyTask(self, post_data_dic):
        result = jTool.fetchUrl(self.host, post_data_dic, 'post')
        return result


def doTask(eid, url, ename, param):
    '''
    循环6次尝试获取指定url的内容
    然后存储到远程数据库
    返回True,否则False
    '''
    param['eid'] = str(eid)
    param['ename'] = ename
#    param['url'] = param['preUrl'] + url
    param['url'] = param['preUrlip'] + url
    proxyList = jTool.getProxy('proxy.txt')
    return rp.crawlUrl(param['conn'], param, proxyList)


def operateTask(task, param):
    count = len(task)
    eids = []
    for i in range(count):
        task[i] = list(task[i])
        task[i].append(False)
        eids.append(str(task[i][0]))
    eids = ','.join(eids)
    ccount = 0
    while ccount < count:
        for i in range(count):
            if not task[i][3]:
                eid = int(task[i][0])
                url = str(task[i][1])
                ename = str(task[i][2])
                print str(eid)+'::'+ename
                task[i][3] = doTask(eid, url, ename, param)
                if task[i][3]:
                    ccount += 1
            else:
                continue
    post_data_dic = {'taskTable': 'item_url', 'type': 'complete', 'num': param['num'], 'eids': eids}
    return post_data_dic


def makeParam():
    paramDic = jTool.getConfigParam(['hostSvr', 'dbHost', 'dbUser', 'dbPasswd', 'rdb', 'basePostUrl', 'preUrl', 'basePostUrlip', 'preUrlip'], 'config.ini')
    conn = jTool.initCursor(paramDic['dbHost'], paramDic['dbUser'], paramDic['dbPasswd'], paramDic['rdb'])
    paramDic['conn'] = conn
    return paramDic


def mainLoop(num):
    post_data_dic = None
    param = makeParam()
    host = param['hostSvr']
    while 1:
        bc = baseClient(host, str(num))
        if not bc.connect():
            break
        post_data_dic = post_data_dic if post_data_dic else {'taskTable': 'item_url', 'type': 'apply', 'num': str(num)}
        task = eval(bc.getMyTask(post_data_dic))
        task = list(task)
        print 'Get new task on '+ str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        param['num'] = str(num)
        post_data_dic = operateTask(task, param)
    param['conn'].close()


if __name__=='__main__':
        print '*'*50
        print '请在末尾+空格+分配给你的id号，一般每台机器最多开20个进程\n你的id范围就是1-20,每个进程固定输入一个，如1或2'
        print '例如： dClient 2'
        print '*'*50
        num = sys.argv[1]
        mainLoop(num)

