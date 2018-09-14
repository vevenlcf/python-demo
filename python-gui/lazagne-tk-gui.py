# -*- coding:utf-8 -*-
'''
# @Date    : 2018-9-14
# @Author  : vevenlcf
# @Link    : https://github.com/vevenlcf
# @Version : 1.0
'''

from tkinter import *
import  requests
from bs4 import BeautifulSoup
# 根据链接下载歌曲
import urllib
import argparse
import logging
import sys
import time
import os
import json

from lazagne.config.write_output import write_in_file, StandardOutput
from lazagne.config.manage_modules import get_categories
from lazagne.config.constant import constant
from lazagne.config.run import run_lazagne, create_module_dic


##############################################################################
#                                                                            #
#                           By Alessandro ZANNI                              #
#                                                                            #
##############################################################################

# Disclaimer: Do Not Use this program for illegal purposes ;)
constant.st = StandardOutput()  # Object used to manage the output / write functions (cf write_output file)
modules = create_module_dic()


def output(output_dir=None, txt_format=False, json_format=False, all_format=False):
    if output_dir:
        if os.path.isdir(output_dir):
            constant.folder_name = output_dir
        else:
            print('[!] Specify a directory, not a file !')

    if txt_format:
        constant.output = 'txt'

    if json_format:
        constant.output = 'json'

    if all_format:
        constant.output = 'all'

    if constant.output:
        if not os.path.exists(constant.folder_name):
            os.makedirs(constant.folder_name)
            # constant.file_name_results = 'credentials' # let the choice of the name to the user

        if constant.output != 'json':
            constant.st.write_header()


def quiet_mode(is_quiet_mode=False):
    if is_quiet_mode:
        constant.quiet_mode = True


def verbosity(verbose=0):
    # Write on the console + debug file
    if verbose == 0:
        level = logging.CRITICAL
    elif verbose == 1:
        level = logging.INFO
    elif verbose >= 2:
        level = logging.DEBUG

    formatter = logging.Formatter(fmt='%(message)s')
    stream = logging.StreamHandler(sys.stdout)
    stream.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(level)
    # If other logging are set
    for r in root.handlers:
        r.setLevel(logging.CRITICAL)
    root.addHandler(stream)


def manage_advanced_options(user_password=None):
    if user_password:
        constant.user_password = user_password


def runLaZagne(category_selected='all', subcategories={}, password=None):
    """
    This function will be removed, still there for compatibility with other tools
    Everything is on the config/run.py file
    """
    for pwd_dic in run_lazagne(category_selected=category_selected, subcategories=subcategories, password=password):
        yield pwd_dic


def clean_args(arg):
    """
    Remove not necessary values to get only subcategories
    """
    for i in ['output', 'write_normal', 'write_json', 'write_all', 'verbose', 'auditType', 'quiet']:
        try:
            del arg[i]
        except Exception:
            pass
    return arg


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=constant.st.banner, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-version', action='version', version='Version ' + str(constant.CURRENT_VERSION),
                        help='laZagne version')

    # ------------------------------------------- Permanent options -------------------------------------------
    # Version and verbosity
    PPoptional = argparse.ArgumentParser(
        add_help=False,
        formatter_class=lambda prog: argparse.HelpFormatter(prog,
                                                            max_help_position=constant.MAX_HELP_POSITION)
    )
    PPoptional._optionals.title = 'optional arguments'
    PPoptional.add_argument('-v', dest='verbose', action='count', default=0, help='increase verbosity level')
    PPoptional.add_argument('-quiet', dest='quiet', action='store_true', default=False,
                            help='quiet mode: nothing is printed to the output')

    # Output
    PWrite = argparse.ArgumentParser(
        add_help=False,
        formatter_class=lambda prog: argparse.HelpFormatter(prog,
                                                            max_help_position=constant.MAX_HELP_POSITION)
    )
    PWrite._optionals.title = 'Output'
    PWrite.add_argument('-oN', dest='write_normal', action='store_true', default=None,
                        help='output file in a readable format')
    PWrite.add_argument('-oJ', dest='write_json', action='store_true', default=None,
                        help='output file in a json format')
    PWrite.add_argument('-oA', dest='write_all', action='store_true', default=None, help='output file in both format')
    PWrite.add_argument('-output', dest='output', action='store', default='.',
                        help='destination path to store results (default:.)')

    # Windows user password
    PPwd = argparse.ArgumentParser(
        add_help=False,
        formatter_class=lambda prog: argparse.HelpFormatter(
            prog,
            max_help_position=constant.MAX_HELP_POSITION)
    )
    PPwd._optionals.title = 'Windows User Password'
    PPwd.add_argument('-password', dest='password', action='store',
                      help='Windows user password (used to decrypt creds files)')

    # -------------------------- Add options and suboptions to all modules --------------------------
    all_subparser = []
    all_categories = get_categories()
    for c in all_categories:
        all_categories[c]['parser'] = argparse.ArgumentParser(
            add_help=False,
            formatter_class=lambda prog: argparse.HelpFormatter(prog,
                                                                max_help_position=constant.MAX_HELP_POSITION)
        )
        all_categories[c]['parser']._optionals.title = all_categories[c]['help']

        # Manage options
        all_categories[c]['subparser'] = []
        for module in modules[c]:
            m = modules[c][module]
            all_categories[c]['parser'].add_argument(m.options['command'], action=m.options['action'],
                                                 dest=m.options['dest'], help=m.options['help'])

            # Manage all suboptions by modules
            if m.suboptions and m.name != 'thunderbird':
                tmp = []
                for sub in m.suboptions:
                    tmp_subparser = argparse.ArgumentParser(
                        add_help=False,
                        formatter_class=lambda prog: argparse.HelpFormatter(
                            prog,
                            max_help_position=constant.MAX_HELP_POSITION)
                    )
                    tmp_subparser._optionals.title = sub['title']
                    if 'type' in sub:
                        tmp_subparser.add_argument(sub['command'], type=sub['type'], action=sub['action'],
                                                   dest=sub['dest'], help=sub['help'])
                    else:
                        tmp_subparser.add_argument(sub['command'], action=sub['action'], dest=sub['dest'],
                                                   help=sub['help'])
                    tmp.append(tmp_subparser)
                    all_subparser.append(tmp_subparser)
                    all_categories[c]['subparser'] += tmp

    # ------------------------------------------- Print all -------------------------------------------

    parents = [PPoptional] + all_subparser + [PPwd, PWrite]
    dic = {'all': {'parents': parents, 'help': 'Run all modules'}}
    for c in all_categories:
        parser_tab = [PPoptional, all_categories[c]['parser']]
        if 'subparser' in all_categories[c]:
            if all_categories[c]['subparser']:
                parser_tab += all_categories[c]['subparser']
        parser_tab += [PPwd, PWrite]
        dic_tmp = {c: {'parents': parser_tab, 'help': 'Run %s module' % c}}
        # Concatenate 2 dic
        dic = dict(dic, **dic_tmp)

    # Main commands
    subparsers = parser.add_subparsers(help='Choose a main command')
    for d in dic:
        subparsers.add_parser(d, parents=dic[d]['parents'], help=dic[d]['help']).set_defaults(auditType=d)

    # ------------------------------------------- Parse arguments -------------------------------------------

    if len(sys.argv) == 1:
        #parser.print_help()
        #print "==============================================\n"
        #print sys.argv
        sys.argv.insert(2, 'all')

    args = dict(parser.parse_args()._get_kwargs())
    arguments = parser.parse_args()

    quiet_mode(is_quiet_mode=args['quiet'])

    # Print the title
    constant.st.first_title()

    # Define constant variables
    output(
        output_dir=args['output'],
        txt_format=args['write_normal'],
        json_format=args['write_json'],
        all_format=args['write_all']
    )
    verbosity(verbose=args['verbose'])
    manage_advanced_options(user_password=args.get('password', None))

    start_time = time.time()

    category = args['auditType']
    subcategories = clean_args(args)

    for r in runLaZagne(category_selected=category, subcategories=subcategories, password=args.get('password', None)):
        pass


    print "================================end1 ====================\n"
    global res;
    res = write_in_file(constant.stdout_result)
    print res
    res2 = json.loads(res)
    print res2
    print "================================end2 ====================\n"
    constant.st.print_footer(elapsed_time=str(time.time() - start_time))

#网易云音乐为我们提供了一个根据歌曲 id 来下载歌曲的地址
#http://music.163.com/song/media/outer/url?id=543710263
def download_song():
    # 1.获取用户输入的
    content = entry.get()
    if content == '':
        tkMessageBox.showinfo("提示", "请输入需要翻译的内容")
    else:
        print content
    # http://music.163.com/song/media/outer/url?id=543710263
    #     # 添加数据到列表框的最后
    text.insert(END, '展示结果:%s' % res)
    # 文本框向下滚动
    text.see(END)
    # 更新(不更新就一直卡在那，显示同样的内容)
    text.update()
    text.insert(END,"展示完毕")

# 1.创建窗口
root = Tk()

# 2.窗口标题
root.title('主机密码获取工具')

# 3.窗口大小以及显示位置,中间是小写的x
root.geometry('550x400+550+230')
# 窗口显示位置
# root.geometry('+573+286')

# 4.标签控件
lable = Label(root,text='输入扫描指令',font=('微软雅黑',15))
lable.grid(row=0,column=0)

# 5.输入控件
entry =Entry(root,font=('微软雅黑',25))
entry.grid(row=0,column=1)

# 6.列表框控件
text = Listbox(root,font=('微软雅黑',16),width=45,height=10 )
# columnspan组件所跨越的列数
text.grid(row=1,columnspan=2)

# 7.按钮控件
button = Button(root,text='开始执行',width=10,font=('微软雅黑',10),command=download_song)
button.grid(row=2,column=0,sticky=W)

button1 = Button(root,text='退出',width=10,font=('微软雅黑',10),command=root.quit)
button1.grid(row=2,column=1,sticky=E)

# 消息循环,显示窗口
root.mainloop()
