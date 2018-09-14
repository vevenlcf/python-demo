#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
# @Date    : 2018-9-14
# @Author  : vevenlcf
# @Link    : https://github.com/vevenlcf
# @Version : 1.0
'''

from  Tkinter import *
import tkMessageBox
import requests

# 定义button事件
def translation():
    content=entry.get()
    if  content == '':
        tkMessageBox.showinfo("提示", "请输入需要翻译的内容")
    else:
        print content
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
    url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
    # url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
    data = {}
    data['i'] = content
    data['from'] = 'AUTO'
    data['to'] = 'AUTO'
    data['smartresult'] = 'dict'
    data['client'] = 'fanyideskweb'
    # data['salt'] = '1530332652360' # 时间戳
    # data['sign'] = '7f281888e41d12a63b20790707672708'
    data['doctype'] = 'json'
    data['version'] = '2.1'
    data['keyfrom'] = 'fanyi.web'
    data['action'] = 'FY_BY_CLICKBUTTION'
    data['typoResult'] = 'false'
    result = requests.post(url,data=data,headers=header)
    translation = result.json()
    translation = translation['translateResult'][0][0]['tgt']
    print(translation)
    res.set(translation)


root = Tk()
#1、窗口标题

res = StringVar()

root.title('中英文互译')
#2、窗口大小，显示位置
root.geometry('290x100+573+286')
#3、标签控件
lable = Label(root,text='输入要翻译的文字',font=('微软雅黑',10), fg='black')
lable.grid()

lable = Label(root,text='翻译结果',font=('微软雅黑',10), fg='black')
lable.grid()

#4、输入控件
entry=Entry(root, font='微软雅黑')
entry.grid(row=0,column=1)
#显示翻译之后的内容
entry2=Entry(root, font='微软雅黑', textvariable=res)
#输入标签位置
entry2.grid(row=1,column=1)

#5、按钮控件
button = Button(root, text ="翻译",width=10,font=('微软雅黑',10),command=translation)
button.grid(row=2,column=0,sticky=W)

button = Button(root, text ="退出",width=10,font=('微软雅黑',10), command=root.quit)
button.grid(row=2,column=1,sticky=E)

#-----------------至此，界面已经画出来了---------------------------

root.mainloop()
