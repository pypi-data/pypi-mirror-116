# -*- coding: utf-8 -*-
'''
@Time    : /
@Author  : Yanyuxiang
@Email   : yanyuxiangtoday@163.com
@FileName: /
@Software: PyCharm
'''

def rm_elem(input_list, elem):
    ''' rm elem from input_list if elem in input_list '''
    if elem in input_list:
        input_list.remove(elem)
    return

def rm_dss(input_list):
    if '.DS_Store' in input_list:
        input_list.remove('.DS_Store')
    return
