# -*- coding: utf-8 -*-

import sys
import time
from generate_scripts import run as generate_scripts
from get_mails import run as get_mails
from send_mails import run as send_mails

sys.path.append('../')

def run():
    while 2>1:
        get_status = get_mails()
        if get_status=="no mails": # 判断如果没有获取到邮件，停顿5s之后，再去邮件里面搜索
            time.sleep(5)
            continue
        generate_scripts()
        send_mails()
        time.sleep(10)



if __name__ == '__main__':
    run()