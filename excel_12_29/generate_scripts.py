#-*- encoding: utf-8 -*-
#-*- encoding: gb2312 -*-

"""
@author: zhou.xuqi
@contact: 527898116@qq.com
@time: 2018/12/22
"""

import xlrd
import os
import re
import time
import zipfile
from script import LTE
import logging
from log_conf import configure_logging
import shutil

CUR_PATH = os.path.dirname(__file__)
logger = logging.getLogger("get_mail")

def zip_ya(name):
    zp_file = re.search("(.*?)\.", name).groups()[0]
    file_news = zp_file + '.zip'  # 压缩后文件夹的名字
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
    dirs = os.listdir()
    startdirs = []
    for dir in dirs:
        if "Delete" in dir:
            startdirs.append(dir)
    for startdir in startdirs:
        for dirpath, dirnames, filenames in os.walk(startdir):
            fpath = dirpath.replace(startdir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
            fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
    z.close()

def generate_scriipte(worksheet,sheet_name,num_list,sheet_num):
    print(num_list)
    sheet = worksheet.sheet_by_name(sheet_name) # 获取对应sheet的内容
    nrows = sheet.nrows #获取全部行数
    row_values = []
    for i in range(0, nrows): #一个一个单元格读取
       # print(sheet.row_values(i))
        if i == 0: #获取表格第一行
            continue
        status = "0"
        item = {} #创建空字典
        message = {}
        lists = []#创建空列表
        sheet_item = sheet.row_values(i) #获取单行数据 返回为list

        item["id%s" % str(num_list[0])] = sheet_item[int(num_list[0])] #name_list[0] 为site_id 类型的，也就是说name_list[0] 就是id,sheet_item[id_list[0]]就是当前行的id对应的值，写入字典
        message_num = len(num_list) #name_list 里面就是需要匹配的的单元格，这个就是查看有多少个需要匹配的单元格

        if len(row_values) == 0: #row_values 是总的list，如果当前list里面还没有数据插入，则运行if status==0部分的代码
            pass
        else: #如果已经有row_values
            num = 0
            for r in row_values: #遍历总list
                print(sheet_item[int(num_list[0])],r["id%s" % num_list[0]])
                if sheet_item[int(num_list[0])] == r["id%s" % num_list[0]]:  #如果有id 是相同的 则取出来
                    status = "1"
                    list_ = r["lists"] #去除他的list
                    for m_n in range(0, int(message_num)):
                        message["id%s" % num_list[m_n]] = str(sheet_item[int(num_list[m_n])])
                    list_.append(message)
                    item["lists"] = list_
                    del row_values[num] #在list中删除刚在获取的数据
                    row_values.append(item) #重新插入合并后的数据
                    break
                num += 1
        #status == 0的写法与上面的基本相同
        if status == "0":
            for m_n in range(0,int(message_num)):
                message["id%s" % num_list[m_n]] = str(sheet_item[int(num_list[m_n])])

            print("xxxxx",message)
            lists.append(message)
            item["lists"] = lists
            #print("@wwwww",item)
            row_values.append(item) # 插入总表

            # row_values.append()
    if "sheet_name" =="LTE":
        LTE.Spider.LTE(row_values,sheet_num,num_list)
    return "ok"

def excel(name):
    if not os.path.exists(name): #判断本地是否存在附件
        print("没有找到这个文件")#没有就报错
        return "error"
    sheet_conf=[]
    sheet_txt = open("conf/sheet.txt","r",encoding="utf-8") #读取配置文件sheet.txt
    sheet_result =  sheet_txt.readlines()
    for sheet_res in sheet_result:
        sheet_conf.append(sheet_res.strip()) # 写入sheet_conf
    sheet_txt.close()
    worksheet = xlrd.open_workbook(name) # 打开文件
    sheets_name = worksheet.sheet_names() #读取所有sheet
    #print(sheets_name)
    s_num =1
    for sheet_name in sheets_name: #遍历所有的sheet
        for sc in sheet_conf: #获取sheet的规则
            if sheet_name in sc: # 根据同的sheet 来获取单元格 ，如果当前的sheet名在sheet规则里面
                scs=sc.split(";") # 将sheet里面获取到的规则以分号切成list
                scs_num_list = scs[1].split(",") #获取list中下标为1的以逗号切割成list

                generate_scriipte(worksheet,sheet_name,scs_num_list,s_num) # 开始生成mos脚本
        s_num += 1
    zip_ya(name)
    time.sleep(1)
    for dir in os.listdir():
        if "Delete" in dir:
            for root, dirs, files in os.walk(dir):
                for name_ in files:
                    del_file = os.path.join(root, name_)
                    os.remove(del_file)
            shutil.rmtree(dir)
    os.remove(name)
    logger.info("end")

def run():
    configure_logging("log/scripts.log") # 创建log 文件
    email_message_end = open("conf/message_end.txt", "w", encoding="utf-8") #创建文件
    while 1: # 实测while True 比while 1 运行速度要慢
        if not os.path.exists("conf/mail_name.txt"): #如果 mail_name 不在当前目录则每隔1s扫描一次当前目录
            time.sleep(1)
            return ""
        f=open("conf/mail_name.txt","r",encoding="utf-8") # 打开文件
        result =  f.readlines()#逐行读取返回list
        #print(result)
        if len(result) == 0: # 如果文件存在，但是里面内容为空的，关闭文件每隔1s再次扫描
            f.close()
            time.sleep(1)
            continue
        for res in result: #遍历
            file_name = res.strip().split(";") # 去掉前后空格，以分号切割成list
            if '-----' in file_name[0]: #如果 ----- 存在
                filenames =  file_name[0].split("-----") #已-----切割成list
                for filename in filenames:
                    excel(filename) #调用excel函数，传入filename
            else:
                filename = file_name[0]
                excel(filename)
            email_message_end.write(res.strip()+"\n")
        break
            # filleThread = threading.Thread(target=excel,args=file_name)
            # filleThread.start()


if __name__ == '__main__':
    run()
