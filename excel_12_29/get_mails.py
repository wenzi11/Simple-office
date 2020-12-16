#-*- encoding: utf-8 -*-
#-*- encoding: gb2312 -*-

"""
@author: zhou.xuqi
@qq: 527898116
@mail:527898116@qq.com
"""

import configparser
import os
import re
from imapclient import IMAPClient,SEEN
import logging
from email.header import decode_header
from log_conf import configure_logging
import email

CUR_PATH = os.path.dirname(__file__)
logger = logging.getLogger("get_mail")

class Imapmail(object):
    def __init__(self):  # 初始化数据
        self.serveraddress = None
        self.user = None
        self.passwd = None
        self.prot = None
        self.ssl = None
        self.timeout = None
        self.savepath = None
        self.server = None

    def client(self):  # 链接
        try:
            self.server = IMAPClient(self.serveraddress, self.prot, self.ssl, timeout=self.timeout)
            return self.server
        except BaseException as e:
            logger.error("ERROR:>>> %s" % str(e))
            return "ERROR: >>> " + str(e)

    def login(self):  # 认证
        try:
            self.server.login(self.user, self.passwd)
        except BaseException as e:
            logger.error("ERROR:>>> %s" % str(e))
            return "ERROR: >>> " + str(e)

    def getallmail(self):  #
        email_message = open("conf/email_message.txt","w",encoding="utf-8") # 创建email_message.txt
        self.server.select_folder('INBOX')  # 选择目录 readonly=True 只读,不修改,这里只选择了 收件箱
        result = self.server.search('UNSEEN')  # 获取未度邮件总数目 [1,2,3,....]
        if len(result)==0:
            print(u"暂时没有邮件")
            return "no mails"
        logger.info("邮件列表:>>> %s" % str(result)) # 打印日志
        out_file=open('conf/mail_name.txt',"w",encoding="utf-8") #创建mail_name.txt
        for _sm in result: # 遍历未读邮件

            data = self.server.fetch(_sm, ['ENVELOPE']) # 获取整个邮件的所有信息
            envelope = data[_sm][b'ENVELOPE'] #获取邮件头
            print(envelope)
            subject = envelope.subject.decode() #获取邮件标题
            if subject: #存在邮件标题
                subject, de = decode_header(subject)[0]  #解码邮件标题
                subject = subject if not de else subject.decode(de) #解码邮件标题
            to_lists =  re.findall("(Address\(.*?\))",str(data)) # 获取搜索的收件人、发件人、抄送人、密抄人邮箱
            to_list =""
            for to in to_lists:
                print(to)
                mailbox =re.search("mailbox=b'(.*?)'",str(to)).groups()[0] #获取邮箱的名字
                host = re.search("host=b'(.*?)'",to).groups()[0]# 获取邮箱的域名
                mail_adders = mailbox+"@"+host #拼接邮箱地址
                if len(to_list) == 0:
                    to_list += mail_adders
                else:
                    if mail_adders in to_list:
                        continue
                    to_list +=","+ mail_adders # 写入to_list

            msgdict = self.server.fetch(_sm, ['BODY[]'])  # 获取邮件内容
            mailbody = msgdict[_sm][b'BODY[]']  # 获取邮件内容
            try:
                e = email.message_from_string(mailbody.decode()) # 解析邮箱内容
            except Exception:
                e = email.message_from_string(str(mailbody))
            maintype = e.get_content_maintype() #获取主要内容
            if maintype =="multipart": # 如果是附件内容
                filenames =""
                for part in e.get_payload():
                    #print(part)
                    name = part.get_filename() #出现filename的 即为存在的附件
                    if name:
                        fdh = decode_header(name) #解码附件名

                        try:
                            filename = fdh[0][0].decode("gbk") # 修改附件名编码
                        except:
                            filename = fdh[0][0]
                        if '.xls' not in str(filename) or '.xlsx' not in str(filename):
                            continue
                        data = part.get_payload(decode=True)
                        f = open(filename, 'wb') #创建附件，二进制写入
                        f.write(data)
                        f.close()
                        print(str(filename)+";"+str(subject)+"\n" )
                        out_file.write(str(filename)+";"+str(subject)+"\n" )
                        if len(filenames)==0:
                            filenames +=str(filename)
                        else:
                            filenames +="-----" +str(filename)
                message = str(subject) + ";"+str(filenames)+";"+ str(to_list)
                email_message.write(message)
            msgdict = self.server.fetch(_sm, ['BODY.PEEK[]'])
            for message_id, message in msgdict.items():
                print(message_id)
            self.server.set_flags(_sm,[SEEN]) # 将获取过的邮件放入已读
        out_file.close()
        email_message.close()
        logger.info("end")
        return "end"

def run():
    if not os.path.exists("conf"): # 如果当前目录没有conf文件夹，就创建文件夹
        os.makedirs("conf")
    conf =  configparser.ConfigParser()
    conf.read("conf/mail.conf") # 加载 conf文件夹下的mail.conf配置文件
    server_address = conf.get('message','serveraddress') #获取serveraddress
    mail_address= conf.get('message','mailaddress')#获取mailaddress
    password = conf.get('message','password')#password

    configure_logging("log/get_mails.log") #设置log日志文件路径和名称
    imap = Imapmail() #实例化
    imap.serveraddress = server_address  # 邮箱地址
    imap.user = mail_address# 邮箱密码
    imap.passwd = password # 邮箱账号
    imap.client() #链接
    imap.login() #登陆邮箱
    status = imap.getallmail() # 获取附件
    return status

if __name__ == '__main__':
    status = run() #调用 run 函数