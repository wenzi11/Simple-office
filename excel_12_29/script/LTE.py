#-*- encoding: utf-8 -*-
#-*- encoding: gb2312 -*-

import time
import os
import datetime

class Spider(object):
    # LTE
    def LTE(self,row_values,sheet_num,num_list):
        name_list_num = len(num_list)
        for row in row_values: #遍历row_values
            if not os.path.exists("Delete%s" % str(sheet_num)):  # 判断是否有Delets文件夹
                os.makedirs("Delete%s" % str(sheet_num))

            today1 = datetime.datetime.now()
            today2 = datetime.datetime.strftime(today1, "%Y%m%d")  # 获取当前日期
            timearry = str(int(time.time()))[0:6]  # 获取当前时间时间戳，并切片
            time_text = today2 + "_" + timearry  # 拼接成字符串
            site_id = row["id%s" % num_list[0]]  # 获取表格中的id名
            mos_file_name = site_id + ".mos"  # 拼接文件名
            message_lists = row["lists"]  # 获取需要写入的内容
            message_text = ""
            for message_list in message_lists: # 遍历messa_lists 里面的内容 
                m_text = "set"
                for x in range(0, int(name_list_num)):
                    print(message_list["id%s" % num_list[x]])
                    m_text += "   " + str(message_list["id%s" % num_list[x]])
                message_text += m_text + "\n"  # 拼接成set xxxx xxx xxx xxx xxx 格式 for循环遍历，你有多少个单元格都会拼接处一条
            text1 = """uv use_complete_mom=1
lt all
confb+
gs+
st cell
alt
"""
            text2 = """

wait 20
st cell
alt
gs -
confb-

cvrm %s_GML
cvms %s_GML_%s GML  modify_parameter""" % (site_id, site_id, time_text)

            mos_scripts = open("Delete%s/%s" % (sheet_num, mos_file_name), "w", encoding="utf-8")
            mos_scripts.write(text1)  # 讲text1写入脚本
            print("wwwwwwwwww", message_text)
            mos_scripts.write(message_text)  # 讲生成的set 写入脚本
            mos_scripts.write(text2)  # 将text2 写入脚本
            mos_scripts.close()
            # 以下是备份

        return "ok"

