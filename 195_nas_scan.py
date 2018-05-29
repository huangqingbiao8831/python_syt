#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import logging
import time
import shutil

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.DEBUG)
#print to file...
handler = logging.FileHandler("195_nas_scan.log")
#print to
#handler = logging.StreamHandler()
#handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def remove_uctal_by_serv(server_name):
    logger.debug('enter remove_uctal_by_serv() server_name:%s' % server_name)
    os.chdir(server_name)
    sub_path_name_list = os.listdir(os.getcwd())
    for tmp_sub_path in sub_path_name_list:
        if tmp_sub_path == 'pcap':
            tmp2_sub_path = server_name + '/'+tmp_sub_path
            logger.info('pcap path:%s' % tmp2_sub_path)
            os.chdir(tmp2_sub_path)
            pcap_name_list = os.listdir(os.getcwd())
            for tmp_pcap_name in pcap_name_list: # year deal...
                if not tmp_pcap_name.isdigit():
                    logger.debug('tmp_pcap_name is not digit dir:%s ,not deal' % tmp_pcap_name)
                    continue
                logger.debug('after continue:....')
                current_time = time.strftime('%Y-%m-%d')
                year_moth_day = current_time.split('-')
                logger.debug(year_moth_day)
                logger.debug('tmp_pcap_name:%s' % tmp_pcap_name)
                if int(tmp_pcap_name) < map(int,year_moth_day)[0]:
                    logger.info('remove file :%s' % tmp_pcap_name)
                    shutil.rmtree(tmp_pcap_name)
                elif int(tmp_pcap_name) > map(int,year_moth_day)[0]:
                    pass
                elif int(tmp_pcap_name) == map(int,year_moth_day)[0]:
                    tmp3_sub_path = tmp2_sub_path + '/' + tmp_pcap_name
                    os.chdir(tmp3_sub_path)
                    month_sub_path = os.listdir(os.getcwd())
                    for tmp_month in month_sub_path :   #month deal...
                        if not tmp_month.isdigit():
                            logger.debug('tmp_month is not digit dir:%s,not deal' % tmp_month)
                            continue
                        if int(tmp_month) < map(int,year_moth_day)[1]:
                            remove_month_dir = tmp3_sub_path + '/' + tmp_month
                            logger.info('remove month director :%s' % remove_month_dir)
                            shutil.rmtree(remove_month_dir)
                        elif int(tmp_month) > map(int,year_moth_day)[1]:
                            pass
                        elif int(tmp_month) == map(int,year_moth_day)[1]:
                            day_tmp_path = tmp3_sub_path + '/' + tmp_month
                            os.chdir(day_tmp_path)
                            tmp_day_list = os.listdir(os.getcwd())
                            for tmp_day_dir in tmp_day_list : #day_deal...
                                if not tmp_day_dir.isdigit():
                                    logger.debug('tmp_day_dir is not digit dir:%s,not deal' % tmp_day_dir)
                                    continue
                                if map(int,year_moth_day)[2] - int(tmp_day_dir) > 4:
                                    remove_day_path_dir = day_tmp_path + '/' + tmp_day_dir
                                    shutil.rmtree(remove_day_path_dir)
                                elif map(int,year_moth_day)[2] == int(tmp_day_dir):
                                    logger.debug('int(year_moth_day[2]) == int(tmp_day_dir)')
                                    pass
                                else:
                                    logger.debug("int(year_moth_day[2]) - int(tmp_day_dir) > 4")
                                    pass
                        else:
                            logger.debug("int(tmp_month) == int(year_month_day[1])")
                            pass
                else:
                    logger.debug("int(tmp_pcap_name) < int(year_moth_day[0])")
                    pass
        else:
            logger.debug("tmp_sub_path == pcap")
            pass

def remove_all_file():
    logger.info('Enter remove all file')
    sub_path = '/mnt/nas/uctal'
    os.chdir(sub_path)
    path_name_list = os.listdir(os.getcwd())
    for tmp_sub_path in path_name_list :
        logger.info('remove_all_file function() tmp_sub_path:%s' % tmp_sub_path)
        if tmp_sub_path == '208':
            sub2_path = sub_path + '/208'
            remove_uctal_by_serv(sub2_path)
        elif tmp_sub_path == '209':
            sub3_path = sub_path + '/209'
            remove_uctal_by_serv(sub3_path)
        elif tmp_sub_path == '210':
            sub4_path = sub_path + '/210'
            remove_uctal_by_serv(sub4_path)
        elif tmp_sub_path == '211':
            sub5_path = sub_path + '/210'
            remove_uctal_by_serv(sub5_path)
        elif tmp_sub_path == '215':
            sub6_path = sub_path + '/215'
            remove_uctal_by_serv(sub6_path)
        elif tmp_sub_path == '216':
            sub7_path = sub_path + '/216'
            remove_uctal_by_serv(sub7_path)
        else:
            logging.info("not deal director")

def spaceMonitorJob():
    '''
    当磁盘(切片存储的目录)利用率超过90%,程序退出
    :return:
    '''
    #print('spaceMonitorJob..')
    try:
        st = os.statvfs('/mnt/nas')
        total = float(st.f_blocks * st.f_frsize)
        used = float((st.f_blocks - st.f_bfree) * st.f_frsize)
        logger.info('total:%d,used:%d ,ratio:%f' % (total, used,used/total))
    except IOError:
        print('check webroot space error.')
        logger.error('check webroot space error.')
        return

    aa = used/total
    if aa > 0.7:
        #删除文件
        remove_all_file()
    else:
        logger.info('used/total:%f' %(used/total))

if __name__ == '__main__':
    while True:
        spaceMonitorJob()
        logger.info('the nas monitor is running...')
        time.sleep(7200)
