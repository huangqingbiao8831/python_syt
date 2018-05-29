#!/usr/bin/python
# coding=utf-8

import sys
import psutil
import logging
import os
import time
import pwd
import stat




# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG) # logger的总开关，只有大于Debug的日志才能被logger对象处理


# 第二步，创建一个handler，用于写入日志文件
file_handler = logging.FileHandler('monitor_netmon.log',mode='w')
file_handler.setLevel(logging.DEBUG) # 输出到file的log等级的开关
# 创建该handler的formatter
file_handler.setFormatter(
        logging.Formatter(
                fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')
        )
# 添加handler到logger中
logger.addHandler(file_handler)

# 第三步，创建一个handler，用于输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.CRITICAL) # 输出到控制台的log等级的开关
# 创建该handler的formatter
console_handler.setFormatter(
        logging.Formatter(
                fmt='%(asctime)s - %(levelname)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')
        )
logger.addHandler(console_handler)

count = 0

def is_executable(path, user):
    '''判断文件是否有执行权限
    path:执行文件的路径
    user:执行文件的用户名
    '''
    user_info = pwd.getpwnam(user)
    uid = user_info.pw_uid
    gid = user_info.pw_gid
    s = os.stat(path)
    mode = s[stat.ST_MODE]
    return (
        ((s[stat.ST_UID] == uid) and (mode & stat.S_IXUSR > 0)) or
        ((s[stat.ST_GID] == gid) and (mode & stat.S_IXGRP > 0)) or
        (mode & stat.S_IXOTH > 0)
    )

def restart_mons(ppath,pname):
    '''according to ppath and procedure name restart the procedure
    ppath:程序的路径
    pname:执行的程序名
    '''
    proceName = "/home/cmons/netmonS/bin/bin/" + "netmonS &"
    if is_executable(proceName,'sysoperator'):
        os.system(proceName)
        logging.info("start the procedure %s" % proceName)
    else:
        os.chmod(proceName,stat.S_IRWXU)
        os.system(proceName)

def check_mons_existe():
    '''检查进程是否存在，连续检查三次，如果不存在就启动新的程序；
    如果有超过两个以上的进程，就杀掉多余的进程
    '''
    pids = psutil.pids()
    global count
    for id in pids:
        try:
            p = psutil.Process(id)
            if p.name() == "netmonS":
                count = 0
                logging.info("procedure is running ,pid:%d" % id)
                return
        except psutil.NoSuchProcess:
            pass
    count = count + 1
    logging.info("check netmonS %d" % count)
    if count > 3:
        count = 0
        logging.info("restart the cmons procedure....")
        restart_mons('/home/cmons/netmonS/bin/bin/','netmonS &')

if __name__ =="__main__":
    while True:
        check_mons_existe()
        logging.info("monitor mons procedure is running....")
        time.sleep(5)



