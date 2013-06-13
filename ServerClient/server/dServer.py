# -*-coding:utf-8 -*-
#encoding=utf-8

import sys
import web
import jTool
import time
import urllib
reload(sys)
sys.setdefaultencoding('utf-8')


class dServer:

    def __init__(self):
        paramDic = jTool.getConfigParam(['host', 'user', 'passwd', 'db'], 'server.ini')
        conn = jTool.initCursor(paramDic['host'], paramDic['user'], paramDic['passwd'], paramDic['db'])
        self.conn = conn

    def GET(self):
        return {'status': 'ok', 'msg': 'Connect jdServer OK'}

    def POST(self):
        data = web.data()
        data = data.split('&')
        taskDic = {}
        for datarec in data:
            tmp = datarec.split('=')
            taskDic[tmp[0]] = tmp[1]
        taskDic['ip'] = web.ctx.ip +':'+str(taskDic['num'])
        print taskDic
        cursor = self.conn.cursor()
        cursor2 = self.conn.cursor()
        if taskDic['type']=='apply':
            result = self.getTodoTask(taskDic, cursor, cursor2)
        if taskDic['type']=='complete':
            result = self.completeTask(taskDic, cursor)
            result = self.getTodoTask(taskDic, cursor, cursor2)
        cursor.close()
        cursor2.close()
        return result

    def getTodoTask(self, taskDic, cursor, cursor2):
        '''
        根据访客ip和申请任务表
        '''
        taskTable = taskDic['taskTable']+'_task'
        querySql = 'select eid, url, enterprise_name from '+taskTable+' where status = 0 and ip = '+"'"+taskDic['ip']+"' or status = -1 order by id limit 2"
        cursor.execute(querySql)
        records = cursor.fetchall()
        eids = []
        for rec in records:
            eids.append(str(rec[0]))
        eids = ','.join(eids)
        atime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        updateSql = 'update '+ taskTable +' set status = 0 ,apply_time = '+"'"+atime+"'"+", ip = '"+taskDic['ip']+"' where eid in ("+eids+')'
        cursor2.execute(updateSql)
        self.conn.commit()
        return records

    def completeTask(self, taskDic, cursor):
        '''
        根据发来的eid串把任务设置为完成并重新领取任务给客户端
        '''
        if not taskDic['eids']:
            return 'error'
        otime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        taskTable = taskDic['taskTable']+'_task'
        eids = str(urllib.unquote(taskDic['eids']))
        cursor = self.conn.cursor()
        updateSql = 'update '+ taskTable +' set status = 1 ,ok_time = '+"'"+otime+"'"+' where eid in ( '+eids+') and ip = '+"'"+taskDic['ip']+"'"
        cursor.execute(updateSql)
        self.conn.commit()

if __name__ == "__main__":
    urls = ("/.*", "dServer")
    app = web.application(urls, globals())    
    app.run()
