#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import logging
import time


save_time = 3600
del_path = ['/usr/sipadprg/trace']

# 禁止apscheduler相关信息屏幕输出
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("scan_disc.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def remove_all_file(del_path):
    for file_path in del_path :
        remove_expend_file(file_path)
        print(file_path)

def remove_expend_file(file_path):
    '''
    删除对应的文件
    :param file_path:
    :return:
    '''
    os.chdir(file_path)
    filename_list = os.listdir(os.getcwd())
    for file in filename_list :
        if  'CALL1' in file:
            logger.info("delete file name: %s" % file)
            result = file.split('_')
            date_str = result[-1]  #取最后一个字符串为文件生成日期
            year = date_str[0:4]
            month = date_str[4:6]
            day = date_str[6:8]
            hour = date_str[8:10]
            min_str = date_str[10:12]
            sec_str = date_str[12:14]
            time_str = "%s-%s-%s %s:%s:%s" %(year,month,day,hour,min_str,sec_str)
            total_sec = time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S"))
            current_sec = time.time()
            if current_sec - total_sec > save_time :
                os.remove(file)
        if 'CALL2' in file :
            logger.info("delete file name: %s" % file)
            result = file.split('_')
            date_str = result[-1]  # 取最后一个字符串为文件生成日期
            year = date_str[0:4]
            month = date_str[4:6]
            day = date_str[6:8]
            hour = date_str[8:10]
            min_str = date_str[10:12]
            sec_str = date_str[12:14]
            time_str = "%s-%s-%s %s:%s:%s" % (year, month, day, hour, min_str, sec_str)
            print(time_str)
            total_sec = time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S"))
            current_sec = time.time()
            if current_sec - total_sec > save_time:
                os.remove(file)
        if 'SIPALL' in file :
            logger.info("delete file name: %s" % file)
            date_str = file[6:]
            year = date_str[0:4]
            month = date_str[4:6]
            day = date_str[6:8]
            hour = date_str[8:10]
            min_str = date_str[10:12]
            sec_str = '00'
            time_str = "%s-%s-%s %s:%s:%s" % (year, month, day, hour, min_str, sec_str)
            total_sec = time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S"))
            current_sec = time.time()
            if current_sec - total_sec > save_time:
                os.remove(file)



def spaceMonitorJob():
    '''
    当磁盘(切片存储的目录)利用率超过90%,程序退出
    :return:
    '''
    #print('spaceMonitorJob..')
    try:
        st = os.statvfs('/')
        total = float(st.f_blocks * st.f_frsize)
        used = float((st.f_blocks - st.f_bfree) * st.f_frsize)
        #logger.info('total:%d,used:%d' % (total, used))
    except IOError:
        print('check webroot space error.')
        logger.error('check webroot space error.')
        return

    aa = used/total
    if aa > 0.7:
        #print('No enough space.')
        #logger.info('No enough space.per %f' % aa)
        #删除文件
        remove_all_file(del_path)
    else:
        logger.info('used/total:%f' %(used/total))


if __name__=='__main__':
    while True:
        spaceMonitorJob()
        logger.debug('script is running...')
        time.sleep(5)

