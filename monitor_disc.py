# -*- coding: utf-8 -*-

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

sender = "xxx.xx@xxx.com"
receiver = ["xxx.xx@xxx.com"]
smtpHost = "10.134.xxx.xxx"
smtpPort = "587"


def get_ip():
    hostname = socket.getfqdn(socket.gethostname())
    ip = socket.gethostbyname(hostname)
    return ip


def send_mail(receiver, subject, content):
    ip = get_ip()
    msg = MIMEText(content, _subtype='plain', _charset='utf-8')
    msg['Subject'] = subject
    msg['From'] = 'CLOUD SERVER ' + ip
    msg['To'] = ",".join(receiver)

    try:
        smtp = smtplib.SMTP(smtpHost, smtpPort)
        # smtp.set_debuglevel(1)
        smtp.docmd("HELO Server")
        smtp.ehlo("ismetoad")
        smtp.starttls()
        smtp.helo("ismetoad")
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.close()

    except Exception as error:
        print(error)


def run_cmd(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result_f, error_f = process.stdout, process.stderr
    errors = error_f.read()
    if errors:
        pass
    result = result_f.read().decode()
    if result_f:
        result_f.close()
    if error_f:
        error_f.close()
    return result


def disk_check():
    subject = ''
    result = run_cmd(cmd)
    content = '[root@vm-vc02-SR910 ~]# ' + cmd + '\n' + result
    result = result.split('\n')
    for line in result:
        if 'G ' in line or 'M ' in line:
            line = line.split()
            for i in line:
                if '%' in i and int(i.strip('%')) > 80:
                    subject = '[WARNING] SERVER FILESYSTEM USE% OVER ' + i + ', PLEASE CHECK!'
    if subject:
        #send_mail(receiver, subject, content)
        file_dir = ''
        remove_file()
        print('email sended')
    else:
        print('Everything is ok, keep on monitor.')


def remove_file(dir_tree):




if __name__ == '__main__':
    cmd = 'df -h'
    disk_check()