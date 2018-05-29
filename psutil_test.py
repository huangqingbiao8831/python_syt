#!/usr/bin/python
# coding=utf-8

import psutil
import os
import time
import logging
#import winsound

logger = logging.getLogger(__name__)
#logger.setLevel(level = logging.DEBUG)
#print to file...
#handler = logging.FileHandler("monitor_sipadprg.log")
#print to
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

#磁盘使用率
def get_disk_partitions():
    disk = psutil.disk_partitions()
    for i in disk:
        logging.INFO("磁盘：%s   分区格式:%s"%(i.device,i.fstype))
        disk_use = psutil.disk_usage(i.device)
        logging.INFO("使用了：%sM,空闲：%sM,总共：%sM,使用率\033[1;31;42m%s%%\033[0m,"%(disk_use.used/1024/1024,disk_use.free/1024/1024,disk_use.total/1024/1024,disk_use.percent))

    # 网络使用率

#监控服务器cpu使用率
#def baojing():
#    i = 0
#    while i < 10:
#        i += 1
#       time.sleep(0.5)
#        winsound.PlaySound("ALARM8", winsound.SND_ALIAS)

def get_cpu():
    count = 0
    while count < 1:
        count = count+1
        time.sleep(1)
        cpu_liyonglv = psutil.cpu_percent( )
        logging.INFO("当前cpu利用率：\033[1;31;42m%s%%\033[0m" % cpu_liyonglv)
#       if cpu_liyonglv > 15.0:
#            baojing()

#get memory
def get_memory():
    ls=[]
    memory = psutil.virtual_memory()
    print(memory.used)
    print(memory.total)
    ab = float(memory.used)/float(memory.total)*100
    #logging.INFO("%.2f%%"% ab)
    #logging.INFO(psutil.swap_memory())

def get_network():
    count = psutil.net_io_counters( )
    logging.INFO("发送字节数：\033[1;31;42m%s\033[0mbytes,接收字节数：" \
          "\033[1;31;42m%s\033[0mbytes,发送包数：%s,接收包数%s" \
          % (count.bytes_sent, count.bytes_recv, count.packets_sent, \
             count.packets_recv))
    users = psutil.users( )
    logging.INFO("当前登录用户:%s" % users[0].name)
    # 时间
    curent_time = psutil.boot_time( )
    curent_time_1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(curent_time))
    print(curent_time_1)

def get_procedurce():
    # 读取进程pid，名称，可执行路径
    pid = psutil.pids( )
    for k, i in enumerate(pid):
        try:
            proc = psutil.Process(i)
            if proc.name()=='sipadprg':
                logging.INFO(k, i, "%.2f%%" % (proc.memory_percent( )), "%", proc.name( ), proc.exe( ))
        except psutil.AccessDenied:
            logging.INFO("psutil.AccessDenied")

if __name__=="__main__":
    #get_disk_partitions()
    get_cpu()
    get_memory()
    #get_network()
    get_procedurce()



