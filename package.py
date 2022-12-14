# coding=utf-8
# !/usr/bin/env python
# __author__ = 'Caroline'


import os
import glob
import shutil
import time


# 用于查找指定文件的路径
def find_path(filedir, filename):
    file_path = []
    for root, dirs, files in os.walk(filedir):
        if filename in files:
            path = root + '/' + filename
            file_path.append(path)

    if len(file_path) == 1:
        return file_path[0]
    else:
        return file_path

# if __name__ == '__main__':
#     print(find_path("/Users/ligt/PycharmProjects/pythonProject","aas.txt"))

    对应项目的changelog目录
CHANGES_DIR = '/var/lib/jenkins/changes/tools'

# 最新的代码包目录,代码包目录命名要求，
# 路径中不能出现相同的目录名
# 即 /var/lib/jenkins/changes/changes/tools/monkey不允许
# 存在相同的目录名字changes
SOURCE_DIR = '/var/lib/jenkins/changes/tools/monkey'

# 存放源码的目录的名称
# 切记！！！！和需要替换的源码的目录级别要相同
SOURCE_DIR_NAME = 'monkey'

# 需要替换的代码包目录
# 路径中不能出现相同的目录名
# 即 /var/lib/jenkins/changes/changes/tools/monkey不允许
# 存在相同的目录名字changes
# 切记！！！！和需要替换的源码的目录级别要相同
TARGET_DIR = '/home/test/ROOT'

# 获取需要删除的文件
delete_files = glob.glob('%s/D*.log' % CHANGES_DIR)

# 读取删除文件内容
delete_lines = []
if len(delete_files) == 1:
    f = open(delete_files[0], "r")
    delete_lines = f.readlines()
else:
    raise Exception('Dfile is not one')

# 解析文件内容，获取要删除的文件名字
d_names = []
for line in delete_lines:
    # 解析line，获取文件名
    file_names = line[:-1].split('/')
    d_name = file_names[-1]
    d_names.append(d_name)

# 获取需要替换的文件
modify_files = glob.glob('%s/[!D]*.log' % CHANGES_DIR)

# 读取文件内容
modify_lines = []
if len(modify_files) == 1:
    f = open(modify_files[0], "r")
    modify_lines = f.readlines()
else:
    raise Exception('Mfile is not one')

# 解析文件内容，获取要替换的文件名字
m_names = []
for line in modify_lines:
    # 解析line，获取文件名
    file_names = line[:-1].split('/')
    m_name = file_names[-1]
    m_names.append(m_name)

# step1:替换修改的文件
# 创建目录用于存放修改前的文件
modify_dir = '%s/modify' % CHANGES_DIR
os.mkdir(modify_dir)
# 记录替换的文件
f = open('%s/modify.log' % modify_dir, 'w')

# 开始进行文件替换，并将未替换的文件记录下来，作为增加的文件增加,新建一个列表用于存储替换的文件名字
m_file_names = []
for root, dirs, files in os.walk(TARGET_DIR):
    for file in files:
        if file in m_names:
            # 拼接路径
            full_path = root + '/' + file
            # 把修改的文件的全路径写入到modifylogs文件中
            f.write('modify : %s\n' % full_path)
            # mv原来的文件到modify文件夹中
            shutil.move(full_path, '%s/%s' % (modify_dir, file))
            # 更换文件，首先遍历，获取新文件路径
            new_file_path = find_path(SOURCE_DIR, file)
            # 将新文件换到对应target的目录下
            shutil.copy(new_file_path, full_path)
            # 将该file的名字，写入到m_file_names列表
            m_file_names.append(file)

        # 将待添加的文件名字取出
a_file_names = list(set(m_names) - set(m_file_names))
print
a_file_names
# 获取在最新的代码包目录中这个文件的绝对路径
for name in a_file_names:
    # 需要增加的文件的绝对路径
    full_path = find_path(SOURCE_DIR, name)
    print
    full_path
    # 截取该文件的上级路径
    file_dirs = full_path.split('/')
    # 找到第一个sourcedirname，获取其索引
    num = file_dirs.index(SOURCE_DIR_NAME)
    # 对列表进行切片，获取相对路径
    relative_path = '/'.join(file_dirs[(num + 1):])
    # 获取相对文件夹路径
    relative_dir_path = '/'.join(file_dirs[(num + 1):-1])
    # 需要增加至的绝对路径
    real_path = TARGET_DIR + '/' + relative_path
    # 需要增加至的绝对文件夹路径
    real_dir_path = TARGET_DIR + '/' + relative_dir_path
    # 创建文件夹
    os.popen('mkdir -p %s' % real_dir_path)
    # 记录增加文件的全路径
    f.write('add：%s --  %s \n' % (full_path, real_path))
    # copy 文件至指定位置
    shutil.copy(full_path, real_path)
f.close()

# step2:删除指定文件
# 创建目录用于存放删除的文件
delete_dir = '%s/delete' % CHANGES_DIR
os.mkdir(delete_dir)

# 获取删除文件的全路径并删除
f = open('%s/delete.log' % delete_dir, 'w')

for root, dirs, files in os.walk(TARGET_DIR):
    for file in files:
        if file in d_names:
            # 拼接路径
            full_path = root + '/' + file
            # 把删除的文件的全路径写入到deletelogs文件中
            f.write('%s\n' % full_path)
            # 将删除的文件转移到指定目录：
            new_path = '%s/%s' % (delete_dir, file)
            shutil.move(full_path, new_path)
f.close()

# step3:处理log文件
# 最终将所有的log信息打包并加上时间戳
# 根据时间戳定义压缩文件夹的名字
log_dir_name = '%s/%s' % (CHANGES_DIR, time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time())))
os.mkdir(log_dir_name)
# 将modify的log文件转移至新文件夹内
shutil.copytree(modify_dir, '%s/%s' % (log_dir_name, 'modify'))
shutil.rmtree(modify_dir)
# 将delete的log文件转移至新文件夹内
shutil.copytree(delete_dir, '%s/%s' % (log_dir_name, 'delete'))
shutil.rmtree(delete_dir)
# 将文件夹里的后缀名为log的文件转移到新文件夹内
shutil.move(delete_files[0], log_dir_name)
shutil.move(modify_files[0], log_dir_name)
