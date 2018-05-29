#!/usr/bin/python
# coding=utf-8

import sys
import psutil
import logging


# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG) # logger的总开关，只有大于Debug的日志才能被logger对象处理


# 第二步，创建一个handler，用于写入日志文件
file_handler = logging.FileHandler('test.log',mode='w')
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

def get_cpu_time():
    hello=psutil.cpu_times(percpu=False)
    logging.debug("%f,%f,%f,%f,%f" % (hello[0],hello[1],hello[2],hello[3],hello[4]))
    print(hello)
    print('user:%f,system:%f,idle:%f,interrupt:%f,dpc:%f' % (hello[0],hello[1],hello[2],hello[3],hello[4]))

def get_cpu_pers():
    number=psutil.cpu_percent(interval=None, percpu=False)
    print("perset:%f" % number)
    logging.debug("cpu percent number:%f" % number)


def scan_sipadprg_proce():
    pids = psutil.pids()
    for id in pids:
        try:
            p=psutil.Process(id)
            if p.name()=='sipadprg':
                logging.info(psutil.cpu_percent(interval=1)
                logging.info(p.name())
                logging.info(id)
                logging.info(p.status())
                logging.info(p.cpu_times())
                logging.info(p.name())
                logging.info(p.cpu_percent())
                logging.info(p.connections())
        except psutil.NoSuchProcess:
            pass


def scan_proce_sipadprg():
    all_pids = psutil.pids()
    for sip_pid in all_pids:
        p = psutil.Process(sip_pid)
        if p.name()=='sipadprg':
            pass
           # logging.info()

            

if __name__ == '__main__':
    while True:
        scan_sipadprg_proce()
        time.sleep(5)
        logging.info("monitor sipadprg is running..........")

