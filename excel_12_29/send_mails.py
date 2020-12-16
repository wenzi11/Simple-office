#-*- encoding: utf-8 -*-
#-*- encoding: gb2312 -*-

"""
@author: zhou.xuqi
@contact: 527898116@qq.com
@time: 2018/12/22
"""


import configparser
import os
import time
import re
import zmail # python3.5以上使用的库

def run():
    while 1:
        message_txt = open("conf/email_message.txt","r",encoding="utf-8")
        message_txt_result =message_txt.readlines()
        if not os.path.exists("conf/message_end.txt"):
            return ""
        f=open("conf/message_end.txt","r",encoding="utf-8")
        result = f.readlines()
        if len(result)==0:
            time.sleep(1)
            return ""
        for res in result:
            message_mails =  res.strip().split(";")
            for mtr in message_txt_result:
                if message_mails[1] in mtr.strip():
                    conf = configparser.ConfigParser()
                    conf.read("conf/mail.conf")
                    smtpserver =  conf.get('message','sendaddress')
                    #EMAIL_PORT = 465
                    fromaddr =conf.get('message','mailaddress') # 管理员的邮箱
                    password = conf.get('message','password') # 管理员的邮箱密码
                    end_message = mtr.strip().split(";")

                    if "," in end_message[2]:
                        to_list =  end_message[2].split(",")
                    else:
                        to_list=[]
                        to_list.append(end_message[2])

                    mail_subject = u"%s" % end_message[0]# 邮件的标题
                    adjunct = end_message[1]
                    fujian =[]
                    if "-----" in adjunct: #这里判断是否有多个附件需要发送
                        adjuncts = adjunct.split("-----")
                        for ad in adjuncts:
                            ad_new =  re.search("(.*?)\.",ad).groups()[0]+".zip"
                            fujian.append(ad_new)
                    else:
                        ad_new = re.search("(.*?)\.", adjunct).groups()[0] + ".zip"
                        fujian.append(ad_new)


                    mail_content ={
                                'subject': mail_subject,  # 邮件标题写在这
                                'content': '',  # 邮件正文写在这
                                'attachments':fujian
                            }

                    try:
                        server = zmail.server(fromaddr,password)
                        server.send_mail(to_list,mail_content)
                        print('success')
                        for fj in fujian:
                            os.remove(fj)
                    except Exception as e:
                        print('error:', e)
        break
    os.remove("conf/mail_name.txt")


if __name__ == '__main__':
    run()