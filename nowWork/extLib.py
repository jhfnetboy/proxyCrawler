#!/usr/bin
#encoding=utf-8

import sys
import jTool
import time
import rp

reload(sys)
sys.setdefaultencoding("utf-8")


def enterprise_raw_function(conn, start, end):
    print 'todo'


def e2record():
    '''
    把企业表的postContent 转换到企业记录表的content,一对多
    每个可能存在多个不同类别的信用记录（如工商，人社
    '''
    pass 


def enterprise_record_raw_1_function(conn, start, end):
    '''
    规则：看字段转换表内内容
    把enterprise_record_raw记录转换转入自己表中的其他字段（轻度数据提取）
    '''
    tableName = 'enterprise_record_raw_1'
    cursor = conn.cursor()
    cursor2 = conn.cursor()
    qSql = "select id, eid, enterprise_name, content from " + tableName + ' where id >='+str(start)+' and id <='+str(end)
    cursor.execute(qSql)
    print  "start extract data in "+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    count = 0
    while 1:
        record = cursor.fetchone()
        if not record or record[0]>end:
            continue      
        count += 1
        id = record[0]
        eid = record[1]
        content = record[3].strip()
#        print id
#        print eid
        clist = content.split('r_obj = t_obj.add_record(true);\n')
       
        print '企业名称：'+ record[2]+', eid:'+str(eid)+', id:'+str(id)
        tmp = clist[0].split('：')
        publisher = tmp[0].split(',')[-1].strip()
        print publisher
        try:
            category = tmp[1].split(',')[0].strip()
            print category
        except:
            continue
        if len(clist)<2:
            recs = clist[0]
        else:
            recs = ''.join(clist[1].split(', false);'))
        tmp = recs.split('\n')
        for i in range(len(tmp)):
            tt = tmp[i].split(',')
            del tt[0]
            tmp[i] = ''.join(tt)
        records = ';'.join(tmp)
        records = jTool.clearX(['(', ')', 'true'], records).strip()
        print records
        print '*'*30
        tmpDic = {}
        tmpDic['publisher'] = publisher
        tmpDic['category'] = category
        tmpDic['records'] = records
        where = ' where id = '+str(id)
        jTool.updateData(cursor2, where, tableName, tmpDic)
        tmpDic = {}
        conn.commit()
    print  "complete extract "+str(count)+" records in "+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    cursor2.close()
    cursor.close()
    conn.close()
    return True


def clearDust_record_raw(tableName, conn):
    '''
    规则：删除publisher为空的记录，是垃圾数据
    '''
    cursor = conn.cursor()
    cursor2 = conn.cursor()
    qSql = "select publisher, id from " + tableName
    cursor.execute(qSql)
    print  "start extract data in "+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    count = 0
    while 1:
        record = cursor.fetchone()
        if not record:
            continue
        if not record[0]:
            where = ' where id ='+str(record[1])
            print where
            jTool.delRecord(cursor2, where, tableName)
            conn.commit()
    cursor2.close()
    cursor.close()
    conn.close()


def contentToRecords(content):
    '''
    根据某条信息，如工商或人社的信息拆分出三个字段：publisher,category,records
    '''
    tmpDic = {}
    clist = content.split('r_obj = t_obj.add_record(true);\n')
    tmp = clist[0].split('：')
    publisher = tmp[0].split(',')[-1].strip()
#    print publisher
    
    try:
        category = tmp[1].split(',')[0].strip()
#        print category
    except Exception, e:
        print __name__, e
        return tmpDic
        
    del clist[0]
    ccount = len(clist)
    recs = ''
    for c in range(ccount):
        recs = recs+''.join(clist[c].split(', false);'))
    tmp = recs.split('\n')
    for i in range(len(tmp)):
        tt = tmp[i].split(',')
        del tt[0]
        tmp[i] = ''.join(tt)
    records = ';'.join(tmp)
    records = jTool.clearX(['(', ')', 'true'], records).strip()
    
    tmpDic['publisher'] = publisher
    tmpDic['category'] = category
    tmpDic['records'] = records
    return tmpDic   

def extractPostContent(conn, table, start, end):
    '''
    提取enterprise_raw表中的postContent字段到enterprse_record_raw中
    每条包括多种信用记录，每种信用记录包括多条
    '''
    cursor = conn.cursor()
    cursor2 = conn.cursor()
    id = int(start)
    while id>=int(start) and id<=int(end):
        print '*'*30
        sql = 'select eid, enterprise_name, url, postContent, id from '+str(table)+' where id ='+str(id)
        id += 1
        cursor.execute(sql)
        record = cursor.fetchone()
        if not record:
            continue
        recList = rp.getEntDetail(record[3])
        scount = 0
        recEntDetailDic = {}
        recEntDetailDic['url'] = record[2]
        recEntDetailDic['eid'] = record[0]
        recEntDetailDic['enterprise_name'] = record[1].strip() 
        print 'id:'+str(record[4])+', '+recEntDetailDic['enterprise_name']
        for rec in recList:
            scount += 1
            rDic = contentToRecords(str(rec).strip())
            if not rDic:
                continue
            rec = jTool.clearX(["'"], rec)
            recEntDetailDic['content'] = (str(rec)).strip()
            recEntDetailDic['records'] = ' '
            recEntDetailDic['ctime'] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            fDic = dict(recEntDetailDic, **rDic)
            jTool.insertData(cursor2, 'enterprise_record_raw', fDic)
            conn.commit()
    cursor.close()
    cursor2.close()
    conn.close()
