# -*- coding:UTF-8 -*-
# file_name     :aaa.py
# author        :lichuanghan
# create_date   :2022/12/15
import os

"""
#
#
#
"""
def find_path(dir, name):
    filePaths = []
    for root, dirs, names in os.walk(dir):
        if(name in names):
            path = root + '/' + name
            filePaths.append(path)
    if(len(filePaths)==1):
        return filePaths[0]
    else:
        return filePaths


if __name__ == '__main__':
    a = find_path("..", "aaa.py")
    print(a)
