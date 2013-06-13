# -*-coding: utf-8 -*-
#encoding=utf-8

import sys
import jTool

reload(sys)
sys.setdefaultencoding("utf-8")


def getParam():
    param = jTool.getConfigParam(['lHeader', 'rHeader', 'url'], 'router.ini')
    param['lHeader'] = eval('['+param['lHeader']+']')
    param['rHeader'] = eval('['+param['rHeader']+']')
    return param

def cip(param):
    '''
    读取配置，连接路由器，获取ip
    成功后发送重启路由器命令
    再次登录后获取当前ip，对比初始ip，相同则再次重启
    '''
    ip = loginRouter(param['lHeader'], param['url'])
    if ip:
        nip = resetRouter(param['rHeader'], param['url'])
        count = 0
        while nip == ip and count<6:
            nip = resetRouter(param['rHeader'], param['url'])
            count += 1
        return not nip == ip
    else:
        print 'Login router failed'
        

def loginRouter(lHeader):
    jTool.fechUrl(param['url'], lHeader, 'post')
    

def resetRouter(rHeader):
    jTool.fechUrl(param['url'], rHeader, 'post')