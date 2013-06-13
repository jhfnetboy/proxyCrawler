# -*-coding: utf-8 -*-
#encoding=utf-8
import sys
import time
import jTool
import random

"""
@author jason
给据起始范围获取企业信用记录网址（item_enterprise)
访问并获取企业基础信息，记录对应eid,记录企业基本信息（摘取字段）到
enterprise_raw
摘取多个类别的记录到enterprise_record_raw,如工商，法院
version 0.4
0.4 适合客户端调用的模块方式，入口为一个url数组
出口为成功失败id串（内容直接远程写入数据库）
0.3 改进：共用函数独立在jTool模块
"""

reload(sys)
sys.setdefaultencoding("utf-8")


def getEntBaseFields(trNode):
    '''
    针对table行数不同情况，返回字段字典（非list)
    '''
    fields = {}
    trCount = len(trNode)
    debug = False
    if(trCount == 3):
        credit = trNode[0].xpath('child::td[2]/a[1]/text()')[0].decode('utf-8')
        fields['credit'] = credit
        legalPerson = trNode[1].xpath('child::td[2]/text()')[0]
        fields['legalPerson'] = legalPerson
        regAdd = trNode[1].xpath('child::td[4]/text()')[0]
        fields['regAdd'] = regAdd.strip()
        busiScope = trNode[2].xpath('child::td[2]/text()')[0]
        fields['busiScope'] = busiScope.strip()
    if(trCount == 4):
        credit = trNode[0].xpath('child::td[2]/a[1]/text()')[0].decode('utf-8')
        fields['credit'] = credit
        legalPerson = trNode[1].xpath('child::td[2]/text()')[0]
        fields['legalPerson'] = legalPerson
        regAdd = trNode[1].xpath('child::td[4]/text()')[0]
        fields['regAdd'] = regAdd
        busiScope = trNode[2].xpath('child::td[2]/text()')[0]
        fields['busiScope'] = busiScope
        regDate = trNode[3].xpath('child::td[2]/text()')[0]
        fields['regDate'] = regDate
    if(trCount == 5):
        credit = trNode[0].xpath('child::td[2]/a[1]/text()')[0].decode('utf-8')
        fields['credit'] = credit
        orgCode = trNode[1].xpath('child::td[2]/text()')[0]
        fields['orgCode'] = orgCode
        postCode = trNode[1].xpath('child::td[4]/text()')[0]
        fields['postCode'] = postCode
        busiScope = trNode[2].xpath('child::td[2]/text()')[0]
        fields['busiScope'] = busiScope
        ecoScope = trNode[3].xpath('child::td[2]/text()')[0]
        fields['ecoScope'] = ecoScope
        legalPerson = trNode[3].xpath('child::td[4]/text()')[0]
        fields['legalPerson'] = legalPerson
        regAdd = trNode[4].xpath('child::td[2]/text()')[0]
        fields['regAdd'] = regAdd
        regDate = trNode[4].xpath('child::td[4]/text()')[0]
        fields['regDate'] = regDate
    return fields


def getEntBase(content):
    '''
    根据企业信用记录网页内容获取企业的基本信息
    以字段list方式返回
    '''
    exp = "//td[@id='xyddj']"
    fields = None
    try:
        tdNode = jTool.getNodes(content, exp)
        tbNode = tdNode[0].xpath('parent::tr/parent::table')
        trNode = tbNode[0].xpath('child::tr')
        fields = getEntBaseFields(trNode)
    except:
        pass
    finally:
        return fields


def getEntDetailRec(recordsStr):
    result = []
    recStart = jTool.getStrIndex('t_obj = d_obj.add_table', recordsStr)
    recordsStr = jTool.getAfter(recStart, 't_obj = d_obj.add_table', recordsStr)
    recEnd = jTool.getStrIndex('d_obj = add_dataSupplier(', recordsStr)
    record = jTool.getBefore(recEnd, recordsStr)
    recordsStr = jTool.getAfter(recEnd, 'd_obj = add_dataSupplier(', recordsStr)
    result.append(record)

    result.append(recordsStr)
    return result


def getEntDetail(content):
    '''
    根据post得到的企业详细信用记录，分解组装
    以字段list方式返回（一般包含多个分类，如工商，法院）
    '''
    start = jTool.getStrIndex('var d_obj, t_obj, r_obj;', content)
    end = jTool.getStrIndex('parent.putDatasAndLoad(datas);', content)
    recCount = 0
    if start>=0 and end >=0:
        recordsStr = jTool.getBetween(start, end, 'var d_obj, t_obj, r_obj;', content)
        recCount = recordsStr.count('t_obj = d_obj.add_table(')
    reclist = []
    for i in range(recCount):
        result = getEntDetailRec(recordsStr)
        reclist.append(result[0])
        recordsStr = result[1]
    return reclist


def crawlUrl(conn, param, proxyList):
    '''
    访问url并获得企业基本信息和信用记录并入库
    '''
    cursor2 = conn.cursor()
    cursor3 = conn.cursor()    
    pcount = len(proxyList)-1
    proxy = proxyList[random.randint(0,pcount)]    
    content = jTool.getContentByProxy(proxy, param['url'])
    if not content:
        jTool.logError('Fail to get page content, url:'+ param['url'])
        return False
    dataSupplier = "法院记录/工商记录/国税记录/质监记录/经信记录/安监记录/统计记录/环保记录/民政记录/司法记录/劳动记录/建设记录/国土记录/交通记录/发改记录/信息产业/科技记录/农业记录/林业记录/海洋渔业/物价记录/食品药品/文化记录/出版记录/广电记录/公安记录/外贸记录/外汇记录/海关记录/检验检疫/人防记录/证监记录/银监记录/保监记录/金融记录/其他记录/行业协会/机构评级/社会中介/阿里巴巴/企业自报/投诉记录/异议记录"
    post_data_dic = {'corpName': param['ename'], 'creditID': param['eid'], 'dataSupplier': dataSupplier, 'isAllInfo': 'False', 'organizeCode': '', 'returnFunction': 'parent.putDatasAndLoad'}
    recEntBaseDic = getEntBase(content)
    if not recEntBaseDic:
        return False
    recEntBaseDic['url'] = param['url']
    recEntBaseDic['eid'] = param['eid']
    recEntBaseDic['enterprise_name'] = param['ename'].strip('')
    recEntBaseDic['ctime'] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    try:
        jTool.insertData(cursor2, 'enterprise_raw', recEntBaseDic)
        conn.commit()
        print '    Insert enterprise baseinfo successfully in ' + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    except:
        print 'Fail to insert record '+ ', eid is '+str(param['eid'])
        jTool.logError('Fail to insert record on '+ 'url is '+param['url']+', id is '+str(id))
        return False
    recEntDetailDic = {}
    recEntDetailDic['url'] = param['url']
    recEntDetailDic['eid'] = param['eid']
    recEntDetailDic['enterprise_name'] = param['ename'].strip()
    recEntDetailDic['records'] = ' '
    recEntDetailDic['ctime'] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#    detailRecUrl = param['basePostUrl']
    detailRecUrl = param['basePostUrlip']
    contentRecord = jTool.getContentByProxy(proxy, detailRecUrl, post_data_dic)
    if not contentRecord:
        return True
    recList = getEntDetail(contentRecord)
    scount = 0
    for rec in recList:
        scount += 1
        rec = jTool.clearX(["'"], rec)
        recEntDetailDic['content'] = str(rec)
        jTool.insertData(cursor3, 'enterprise_record_raw', recEntDetailDic)
        conn.commit()
        print '       Insert enterprise detail info No. '+str(scount)+' successfully in ' + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print 'Fetch and insert successfully in ' + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    return True

#根据指定url获得企业信息和企业信用记录
#抓取到页面后还需要在此发起post请求，获取页面内的ajax内容（会有多条）
#对应页面和明细记录，都insert到对应表中


#conn = jTool.initCursor(paramDic['host'], paramDic['user'], paramDic['passwd'], paramDic['db'])
