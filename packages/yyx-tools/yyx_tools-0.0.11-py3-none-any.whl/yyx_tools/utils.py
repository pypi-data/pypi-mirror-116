# -*- coding: utf-8 -*-
'''
@Time    : 2021/8/13
@Author  : Yanyuxiang
@Email   : yanyuxiangtoday@163.com
@FileName: utils.py
@Software: PyCharm
'''

import os

def check_dir(dir_path):
    os.makedirs(dir_path) if not os.path.isdir(dir_path) else None
    return