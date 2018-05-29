#!/usr/bin/python
# coding=utf-8

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


import socket
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM

import psutil


AD = "-"
AF_INET6 = getattr(socket, 'AF_INET6', object())
proto_map = {
    (AF_INET, SOCK_STREAM): 'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET, SOCK_DGRAM): 'udp',
    (AF_INET6, SOCK_DGRAM): 'udp6',
}


def main():
    templ = "%-5s %-30s %-30s %-13s %-6s %s"
    templ1="%5s %-30s %-13s"
    logging.debug(templ % (
        "Proto", "Local address", "Remote address", "Status", "PID",
        "Program name"))
    proc_names = {}
    for p in psutil.process_iter(attrs=['pid', 'name']):
        proc_names[p.info['pid']] = p.info['name']
    for c in psutil.net_connections(kind='inet'):
        laddr = "%s:%s" % (c.laddr)
        raddr = ""
        if c.raddr:
            raddr = "%s:%s" % (c.raddr)
        logging.debug(templ % (
            proto_map[(c.family, c.type)],
            laddr,
            raddr or AD,
            c.status,
            c.pid or AD,
            proc_names.get(c.pid, '?')[:15],
        ))
    ll=['hello','world','test hello world']
    logging.debug(templ1 % (ll[0],ll[1],ll[2]))


if __name__ == '__main__':
    main()