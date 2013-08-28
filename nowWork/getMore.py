# -*-coding:utf-8 -*-
#encoding=utf-8

import sys
import jTool
import random
import time

#from urllib import unquote

reload(sys)
sys.setdefaultencoding('utf-8')



def saveData(content):
    '''
    从页面内容提取url列表
    存入数据库
    '''
    pass

    
    


def getListPages(pageNo):
    '''
    起始页包含了若干需要抓取里面内容的列表项
    每个列表项打开后是若干url列表，每个url指向的页面是抓取目标
    '''    
    requestUrl = 'http://www.zjcredit.gov.cn:8000/ListPrompt.aspx'
    head = ['Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Charset:GBK,utf-8;q=0.7,*;q=0.3',
                    'Accept-Encoding:gzip,deflate,sdch',
                    'Accept-Language:zh-CN,zh;q=0.8',
                    'Cache-Control:max-age=0',
                    'Connection:keep-alive',
                    'Cookie:ASP.NET_SessionId=t3isah45gu5kb4454qyxkhzy; lzstat_uv=6061202253430616218|2529639; lzstat_ss=953382219_1_1373621147_2529639; _gscu_374314293=7359234405sddy11; _gscs_374314293=73592344d74zfy11|pv:3; _gscbrs_374314293=1; ECStaticSession=ECS81',
                    'Host:www.zjcredit.gov.cn:8000',
                    'Pragma:no-cache',
                    'Origin:http://www.zjcredit.gov.cn:8000',
                    'Referer:http://www.zjcredit.gov.cn:8000/ListPrompt.aspx',
                    'User-Agent:Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36'
                    ]
    sectionID = '01'
    post_data_dic = {'sectionID': sectionID, 'pageNo': pageNo, 'pageLength': 20, 'organizationCode': '', 'searchInfo': ''}
    proxy = '218.108.170.173:82'
    proxy = '218.108.170.170:80'
#    content = jTool.fetchUrlProxy2(proxy, requestUrl, post_data_dic, 'post', head)
    content = open('11.html').read()
    if content:
        exp = '/body/div/table/tr[1]/td[1]/table[1]'
        aList = jTool.getNodes(content, exp)
        print aList

#getListPages(4)


def getDetailListPages(pageNo, conn):
    '''
    最终目标页面的列表项
    每个列表项打开后是若干url列表，每个url指向的页面是抓取目标
    '''    
#    requestUrl = 'http://218.108.28.28:8000/ListPrompts.aspx?sectionID=01&tableID=CourtNotCarryOut&associateID=00000000000000000&hasPromptHistroy=False'
    requestUrl = 'http://218.108.28.28:8000/ListPrompts.aspx'
    head = ['Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Charset:GBK,utf-8;q=0.7,*;q=0.3',
                    'Accept-Encoding:gzip,deflate,sdch',
                    'Accept-Language:zh-CN,zh;q=0.8',
                    'Cache-Control:max-age=0',
                    'Connection:keep-alive',
                    'Cookie:ASP.NET_SessionId=t3isah45gu5kb4454qyxkhzy; lzstat_uv=6061202253430616218|2529639; lzstat_ss=953382219_1_1373621147_2529639; _gscu_374314293=7359234405sddy11; _gscs_374314293=73592344d74zfy11|pv:3; _gscbrs_374314293=1; ECStaticSession=ECS81',
                    'Host:www.zjcredit.gov.cn:8000',
                    'Pragma:no-cache',
                    'Origin:http://www.zjcredit.gov.cn:8000',
                    'Referer:http://218.108.28.28:8000/ListPrompts.aspx?sectionID=01&tableID=CourtNotCarryOut&associateID=00000000000000000&hasPromptHistroy=False',
                    'User-Agent:Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36'
                    ]
#    associateID = '00000000000000000'
#    field_CorporationName = ''
#    field_OrganizationCode = ''
#    isIntermediary = 'False'
#    pageLength = 20
#    recordTotal = 46358
#    sectionID = '01'
#    tableID = 'CourtNotCarryOut'
    post_data_dic = {'recordTotal': 46358, 'tableID': 'CourtNotCarryOut', 'associateID': '00000000000000000', 'field_CorporationName': '', 'sectionID': '01', 'field_OrganizationCode': '', 'isIntermediary': 'False', 'pageNo': pageNo, 'pageLength': 20}
    proxy = '218.108.170.173:82'
    proxy = '218.108.170.170:80'
    content = jTool.fetchUrlProxy2(proxy, requestUrl, post_data_dic, 'post', head)
#    jTool.logit(content, '22.html')
#    content = open('22.html').read()
    if content:
        exp = '//table[1]/tr[2]/td[1]/table[1]/tr/td/a'
        aList = jTool.getNodes(content, exp)
#        import lxml.etree as ETree
#        print aList[1].xpath('//@title')[0]
        titles = aList[1].xpath('//@title')
        corpRecords = {}
#        print aList[1].xpath('//@onclick')[20]
        aStr = aList[1].xpath('//@onclick')
        cursor = conn.cursor()
        from urllib import unquote
        for i in range(20):
#            corpRecords['`corpName`'] = (unquote(titles[i])).decode('utf-8')
            corpRecords['`corpName`'] = titles[i].decode('utf-8').encode('utf-8')
#            print corpRecords['`corpName`']
#            print unquote(corpRecords['`corpName`'])
#            print aStr[i+1]
            tmp = aStr[i+1].split(',')
#            print i+1
            corpRecords['`table`'] = tmp[0].split("'")[1]
            corpRecords['`rowID`'] = tmp[5].split("'")[1]
#            print corpRecords['rowID']
#            print corpRecords['corpName']
            corpRecords['`pageNo`'] = str(pageNo)
            result = jTool.insertData(cursor, 'base_page_list', corpRecords)
            conn.commit()
        cursor.close()
        conn.close()


def getAllpageList(start, end):
    conn = jTool.initCursor('localhost', 'root', 'root', 'rawData')
    while start<=end:
        pageNo = start
        getDetailListPages(pageNo, conn)
        print 'page ok:'+str(start)
        start += 1


#getAllpageList(101, 2318)



def getDetailPageContent(proxy, head, rowID, corpName):
    requestUrl = 'http://www.zjcredit.gov.cn:8000/BrowseDocumentPrompt.aspx'
    post_data_dic = {'sectionID': '01', 'associateID': '00000000000000000', 'tableID': 'CourtNotCarryOut', 'creditID': 0, 'rowID': rowID, 'timeSpan': '', 'seqNo': '', 'corpName': corpName, 'titleID': ''}
    content = jTool.fetchUrlProxy2(proxy, requestUrl, post_data_dic, 'post', head)
    return content



def getPageFields(content):
    '''
    携带参数发起请求，获得最终页面信息
    截取需要的内容，存入数据库
    '''
    if not content:
        return None
    result = {}
    exp = '//table[1]/tr[3]/td[1]/div[1]/text()'
    exp2 = '//table[1]/tr[3]/td[1]/table[1]'
    try:
        result['corpName'] = jTool.getNodes(content, exp)[0].strip()
    except Exception, e:
        print '得到页面非企业信息页面', e
        return None
    corpTable = jTool.getNodes(content, exp2)[0]
    is_15 = len(corpTable.xpath('//tr[15]'))
    is_13 = len(corpTable.xpath('//tr[13]'))
    is_12 = len(corpTable.xpath('//tr[12]'))
    print is_15, is_13, is_12
#    print result['corpName']
#    result['corpNameTable'] = corpTable.xpath('//tr[1]/td[2]/text()')[0]
#    print result['corpNameTable']
    result['orgCode'] = corpTable.xpath('//tr[2]/td[2]//text()')[0]
#    print result['orgCode']
    result['legacyPerson'] = corpTable.xpath('//tr[3]/td[2]//text()')[0]
#    print result['legacyPerson']

    if is_13>0:
        result['address'] = corpTable.xpath('//tr[4]/td[2]//text()')[0]
    #    print result['address']    
        result['execCourt'] = corpTable.xpath('//tr[5]/td[2]//text()')[0]
    #    print result['execCourt']
        result['courtNum'] = corpTable.xpath('//tr[6]/td[2]//text()')[0]
    #    print result['courtNum']
        result['execCause'] = corpTable.xpath('//tr[7]//td[2]//text()')[0]
    #    print result['execCause']
        result['execReason'] = corpTable.xpath('//tr[8]/td[2]//text()')[0]
    #    print result['execReason']
        result['execTime'] = corpTable.xpath('//tr[9]/td[2]//text()')[0]
    #    print result['execTime']
        result['execMoney'] = corpTable.xpath('//tr[10]/td[2]//text()')[0].strip()
    #    print result['execMoney']
        result['unExecMoney'] = corpTable.xpath('//tr[11]/td[2]//text()')[0].strip()
    #    print result['unExecMoney']
        result['togetherExecPerson'] = corpTable.xpath('//tr[12]/td[2]//text()')[0]
    #    print result['togetherExecPerson']
        result['announceDate'] = corpTable.xpath('//tr[13]/td[2]//text()')[0].strip()
    #    print result['announceDate']
        try:
            result['reportPhone'] = corpTable.xpath('//tr[14]/td[2]//text()')[0].strip()
    #        print result['reportPhone']
            result['reportPerson'] = corpTable.xpath('//tr[15]/td[2]//text()')[0].strip()
    #        print result['reportPerson']
        except Exception, e:
            pass
        
    if is_12>0 and is_13<1 and is_15<1:
        result['execCourt'] = corpTable.xpath('//tr[4]/td[2]//text()')[0]
    #    print result['execCourt']
        result['courtNum'] = corpTable.xpath('//tr[5]/td[2]//text()')[0]
    #    print result['courtNum']
        result['execCause'] = corpTable.xpath('//tr[6]//td[2]//text()')[0]
    #    print result['execCause']
        result['execReason'] = corpTable.xpath('//tr[7]/td[2]//text()')[0]
    #    print result['execReason']
        result['execTime'] = corpTable.xpath('//tr[8]/td[2]//text()')[0]
    #    print result['execTime']
        result['execMoney'] = corpTable.xpath('//tr[9]/td[2]//text()')[0].strip()
    #    print result['execMoney']
        result['unExecMoney'] = corpTable.xpath('//tr[10]/td[2]//text()')[0].strip()
    #    print result['unExecMoney']
        result['togetherExecPerson'] = corpTable.xpath('//tr[11]/td[2]//text()')[0]
    #    print result['togetherExecPerson']
        result['announceDate'] = corpTable.xpath('//tr[12]/td[2]//text()')[0]
    #    print result['announceDate']        
    return result


def getPageField(conn, proxy, head, id, rowID, corpName):
    cursor = conn.cursor()
    cursor2 = conn.cursor()
    content = getDetailPageContent(proxy, head, rowID, corpName)
#    content = open('4.html').read()
#    print content
    if not content:
        return None
    from urllib import quote
#    from urllib import unquote
    jTool.logit(content, '4.txt')
#    pageContentDic = {'content': quote(content)}
#    jTool.updateData(cursor2, ' where id = '+str(id)+' ', 'base_page_list', pageContentDic)    
#    try:
    resultDic = getPageFields(content)
    if not resultDic:
        return None
    resultDic['ctime'] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    resultDic['iid']   = str(id)
    rt = jTool.insertData(cursor, 'courtDetail', resultDic)
    return rt
#    except Exception, e:
#        print 'getPageField error', e
#        return None
    conn.commit()
    cursor.close()
    cursor2.close()
    conn.close()
    
    


def mainLoop(start, end):
    proxyList = jTool.getProxy('proxy.txt')
    pcount = len(proxyList)-1
    head = ['Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Charset:GBK,utf-8;q=0.7,*;q=0.3',
                    'Accept-Encoding:gzip,deflate,sdch',
                    'Accept-Language:zh-CN,zh;q=0.8',
                    'Cache-Control:max-age=0',
                    'Connection:keep-alive',
                    'Cookie:ASP.NET_SessionId=t3isah45gu5kb4454qyxkhzy; lzstat_uv=6061202253430616218|2529639; lzstat_ss=953382219_1_1373621147_2529639; _gscu_374314293=7359234405sddy11; _gscs_374314293=73592344d74zfy11|pv:3; _gscbrs_374314293=1; ECStaticSession=ECS81',
                    'Host:www.zjcredit.gov.cn:8000',
                    'Pragma:no-cache',
                    'Cookie:_gscu_374314293=73631708ff8h1y17; lzstat_uv=106813037832225946|2529639; ECStaticSession=ECS80; ASP.NET_SessionId=5dhxxl45gr4d0aexnf1uiu55; _gscbrs_374314293=1; lzstat_ss=815622537_1_1374448570_2529639; _gscs_374314293=t74419759zee6a318|pv:2',
                    'Origin:http://www.zjcredit.gov.cn:8000',
                    'Referer:http://www.zjcredit.gov.cn:8000/ListPrompts.aspx?sectionID=01&tableID=CourtNotCarryOut&associateID=00000000000000000&hasPromptHistroy=False',
                    'User-Agent:Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36'
                    ]
    conn = jTool.initCursor('localhost', 'root', 'root', 'rawData')
    cursor = conn.cursor()
    cursor2 = conn.cursor()
    while start<=end:
        sql = 'select *  from base_page_list where id = '+str(start)+' and status = 0 limit 1'
        cursor.execute(sql)
        record = cursor.fetchone()  
        if not record and start<=end:
            start += 1
            continue
        
        corpName = record[1]
        rowID = record[3]
        print corpName+', '+str(start)
        rt = None
        count = 1
        while not rt and count<=2:
#            print count
            proxy = str(proxyList[random.randint(0, pcount)]).strip()
#            print proxy
            rt = getPageField(conn, proxy, head, str(start), rowID, corpName)
#            print rt
            count += 1
            if rt:
                print 'id'+str(start)+' ok'
                jTool.updateData(cursor2, ' where id = '+str(start)+' ', 'base_page_list', {'status': '1'})
                continue
        start += 1
        conn.commit()
    cursor.close()
    cursor2.close()
    conn.close()

    
    



if __name__=='__main__':
        print '*'*50
        print '请在末尾+空格+记录起始，终止id号'
        print '例如： getMore 1  100'
        print '*'*50
        start = sys.argv[1]
        end = sys.argv[2]
        mainLoop(int(start), int(end))
        
        
