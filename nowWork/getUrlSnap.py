#!/usr/bin
#encoding=utf-8
# -*- coding: utf-8 -*-


import sys
import time
from selenium import webdriver
import os

reload(sys)
sys.setdefaultencoding("utf-8")


def snapUrl(url, save_fn="capture.png"):
    start = time.time()
    print 'start at '+str(start)
    browser = webdriver.Chrome()
#    browser.set_window_size(1,1)
    browser.set_window_size(1200, 900)
    browser.get(url)
    browser.execute_script("""
        (function () {
            var y = 0;
            var step = 100;
            window.scroll(0, 0);
 
            function f() {
                if (y < document.body.scrollHeight) {
                    y += step;
                    window.scroll(0, y);
                    setTimeout(f, 50);
                } else {
                    window.scroll(0, 0);
                    document.title += "scroll-done";
                }
            }
 
            setTimeout(f, 1000);
        })();
    """)
 
    for i in xrange(30):
        if "scroll-done" in browser.title:
            break
        time.sleep(1)
 
    browser.save_screenshot(save_fn)
    browser.close()
    print 'end at '+str(time.time())+', use '+str(time.time()-start)
    


def snapUrl2(url, filename):
    start = time.time()
    print 'start at '+str(start)
    command = 'python webkit2png -x 1024 768 -g 1024 0 '+url+' -o '+filename
    os.system(command)
    os.popen(command)
    print 'start at '+str(time.time())+', use '+str(time.time()-start)

    
def snapUrl3(url, filename):
    pass


    
if __name__ == "__main__":
    url = 'http://www.sina.com.cn'
    url = 'http://www.baidu.com'
    url = 'http://www.zjcredit.gov.cn:8000/EnterpriseInfo.aspx?creditID=76FC39FA4AB30C38'
    snapUrl(url, "capture"+str(time.time())+".png")
#    snapUrl2(url, "capture"+str(time.time())+".png")