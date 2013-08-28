# -*-coding:utf-8 -*-
#encoding=utf-8

from __future__ import division 
from Tkinter import Tk, Entry, Button, Label, mainloop
from tkFont import Font
import sys
import hashlib

reload(sys)
sys.setdefaultencoding('utf-8')


#if __name__=='__main__':
#    print 'input str want to md5'
#    mstr = sys.argv[0]
#    print (hashlib.md5(mstr).hexdigest().upper())
    
    


#from Tkinter import *
#def on_click():
#    label['text'] = 'no way out'
#root = Tk(className='bitunion')
#label = Label(root)
#label['text'] = 'be on your own'
#label.pack()
#button = Button(root)
#button['text'] = 'change it'
#button['command'] = on_click
#button.pack()
#root.mainloop()

#from Tkinter import *
#def on_click():
#    label['text'] = text.get()
#
#root = Tk(className='bitunion')
#label = Label(root)
#label['text'] = 'be on your own'
#label.pack()
#text = StringVar()
#text.set('change to what?')
#entry = Entry(root)
#entry['textvariable'] = text
#entry.pack()
#button = Button(root)
#button['text'] = 'change it'
#button['command'] = on_click
#button.pack()
#root.mainloop()





def pp(ev=None):
  foodl = ''
  try: foodl = eval( text.get())
  except : pass
  if isinstance(foodl, (int,float,long)): pass
  else: foodl = 'Error..'
  label.config(text=foodl)


#主窗口
top = Tk()
top.title('compute')

ft = Font(family = ('Verdana'), size = 8 ) #字体
#注册组件
text = Entry(top, font= ft)
button = Button(top, text='计算(注意先后运算)', command=pp)
label = Label(text='运算符: + - * / % **', font=ft)


Enter = lambda x: x.keycode == 13 and pp()

Key = lambda x: label.config(text='运算符: + - * / % **')

text.bind('<Key>', Enter)#回车事件
text.focus()  #获得焦点

#

text.bind('<Button-1>', Key)
text.pack()
button.pack() 
label.pack()
mainloop()

