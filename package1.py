import os

if __name__ == '__main__':
    # 0.获取待处理的日志变更文件/home/yitong/package/change/dev/分支号/change_日期-时间-序号.log
    '''
    git diff HEAD dc2eb893e86ee3c5dfa06471fb697a9eabf1b4fe --name-status >> change.log
    
    注意：
    1.HEAD指当前开发分支的最新版本id，后面的id为拉取分支时的初始id.
    2.该id由项目经理新建分支议题的时候记录在议题和/home/yitong/package/branch/IDFiles.txt中
    格式为：分支号=初始id号，如：feature-20221228-test=dc2eb893e86ee3c5dfa06471fb697a9eabf1b4fe
    '''
    BRANCH_1 = 'HEAD'
    BRANCH_2 = 'dc2eb893e86ee3c5dfa06471fb697a9eabf1b4fe'
    CHANGE_DIR = 'package/change'
    MODE = 'dev'
    CHANGE_FILE = 'change.log'
    print('1.开始执行git diff命令生成change.log文件')
    print('开始执行...')
    if not os.path.exists(CHANGE_DIR + "/" + MODE):
        os.makedirs(CHANGE_DIR + "/" + MODE)
    if os.path.exists(CHANGE_DIR + "/" + MODE + "/" + CHANGE_FILE):
        os.remove(CHANGE_DIR + "/" + MODE + "/" + CHANGE_FILE)

    with open(os.path.join(os.getcwd()+"/"+CHANGE_DIR + "/" + MODE + "/",CHANGE_FILE), 'w') as f:
        CMD_GIT_DIFF = f'git diff {BRANCH_1} {BRANCH_2} --name-status >> {CHANGE_DIR + "/" + MODE + "/" + CHANGE_FILE}'
        os.system(CMD_GIT_DIFF)
        print('执行完毕...')

    # 1.编译成war包
    '''
    调用mvn命令进行编译打包
    
    /Applications/IntelliJ\ IDEA.app/Contents/plugins/maven/lib/maven3/bin/mvn clean package
    '''
    #拉取最新代码至本地

    CODE_DIR = 'package/code'

    CMD_GIT_CLONE =f'cd {os.getcwd()+"/"+CODE_DIR}'+f'/{MODE} '+ r'&& git clone https://github.com/lichuanghan/demo2.git '
    os.system(CMD_GIT_CLONE)


    CMD_MVN_PACKGE = f'cd {os.getcwd()+"/"+CODE_DIR}'+f'/{MODE}/demo2 '+r'&& /Applications/IntelliJ\ IDEA.app/Contents/plugins/maven/lib/maven3/bin/mvn clean package'
    os.system(CMD_MVN_PACKGE)

    # 2.分析change.log获取删除的文件列表，生成删除脚本

    # 3.分析change.log获取新增或更新的文件列表，从war包中拷贝增量文件至目标路径
