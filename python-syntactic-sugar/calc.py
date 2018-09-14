#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
# @Date    : 2018-9-14
# @Author  : vevenlcf
# @Link    : https://github.com/vevenlcf
# @Version : 1.0
'''

oper = {}
#python 语法糖 @ 用法
def  all_calc(operator):
    def calc(func):
        oper[operator] = func
        return  func
    return calc

@all_calc(operator = '+')
def  sum(a, b):
    return a + b

@all_calc(operator = '-')
def sub(a, b):
    return a - b

@all_calc(operator = '*')
def cheng(a, b):
    return a * b

@all_calc(operator = '/')
def chu(a, b):
    return  a/b

if __name__ == "__main__":
    res  = oper['+'](3, 4)
    print res
