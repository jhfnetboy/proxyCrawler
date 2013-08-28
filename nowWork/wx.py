# -*-coding:utf-8 -*-
#encoding=utf-8

import sys
import jTool


reload(sys)
sys.setdefaultencoding('utf-8')


loginUrl = 'https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN'
#postdata = 'username=bss360%40sina.com&pwd=efe9e92c6f364daefac82ef7146ab572&imgcode=&f=json'
post_data_dic = {'username': 'bss360@sina.com', 'pwd': 'efe9e92c6f364daefac82ef7146ab572', 'imgcode': '', 'f': 'json'}
method = 'post'

head = ['Host: mp.weixin.qq.com', 
        'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:22.0) Gecko/20100101 Firefox/22.0', 
        'Accept: application/json, text/javascript, */*; q=0.01',
        'Accept-Language: zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3', 
        'Accept-Encoding: gzip, deflate', 
        'Content-Type: application/x-www-form-urlencoded; charset=UTF-8', 
        'X-Requested-With: XMLHttpRequest', 
        'Referer: https://mp.weixin.qq.com/cgi-bin/loginpage?t=wxm2-login&lang=zh_CN', 
        'Content-Length: 79', 
        'Cookie: pt2gguin=o1158794678; pgv_pvid=2969295504; o_cookie=1158794678; ptcz=0d261b3be08b72461bb308209aa45e91996c4c797cd79c595899cc05cd2696d7; ptui_loginuin=1158794678; ptisp=ctc; dm_login_weixin_scan=; pgv_info=ssid=s3256792473; uin=o1158794678; skey=@QNf4Bqiq6; qm_sid=c49eddaefd977b7f93b14d3fc601d26e,cIpkagpJqnV8.; qm_username=1158794678; cert=TVGT1E_TbFaJVhJ82VSQs9ZiP5cxfS35',
        'Connection: keep-alive',
        'Pragma: no-cache', 
        'Cache-Control: no-cache'
        ]
        
#jTool.fetchUrlProxy2(proxy, loginUrl, post_data_dic, method, head)
rt = jTool.fetchUrlHttps(loginUrl, post_data_dic, head,  method)
#print rt['ErrMsg']
#{
#"Ret": 302,
#"ErrMsg": "/cgi-bin/indexpage?t=wxm-index&lang=zh_CN&token=707843066",
#"ShowVerifyCode": 0,
#"ErrCode": 0
#}
#