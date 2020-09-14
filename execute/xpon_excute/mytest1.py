#!/usr/bin/python
# -*- coding UTF-8 -*-

#author: ZHONGQI


import xlrd
import os
import sys
import json

test_case_list = []
test_case_id = []
command = ''
# 打开文件夹
# filename = sys.argv[1]
# data = xlrd.open_workbook(filename)
data = xlrd.open_workbook('E:\\CDATA\\自动化测试\\Cdata_part11\\execute\\xpon_excute\\自动化测试用例.xlsx')

# 查看工作表
data.sheet_names()

table1  = data.sheet_by_name('TYPE')
device_type = table1.row_values(1)[1]
if device_type =='GPON':
    # 通过文件名获得工作表,获取工作表2
    table = data.sheet_by_name('GPON')
elif device_type == 'EPON':
    # 通过文件名获得工作表,获取工作表2
    table = data.sheet_by_name('EPON')
elif device_type == 'XPON':
    table = data.sheet_by_name('XPON')

vars = []
for rowNum in range(1, table.nrows):
    if rowNum == 1 :
        vars.append(table.row_values(rowNum)[2] + " = " + (table.row_values(rowNum)[3]) + "\n")
        # print(1,(table.row_values(rowNum)[3]))
    elif isinstance(table.row_values(rowNum)[3], float):
        vars.append(table.row_values(rowNum)[2] + " = " + '"' + str(int(table.row_values(rowNum)[3])) + '"' + "\n")
        # print(2, (table.row_values(rowNum)[3]))
    else:
        vars.append(table.row_values(rowNum)[2] + " = " + '"' + str(table.row_values(rowNum)[3]) + '"' + "\n")
        # print(3, (table.row_values(rowNum)[3]))

#将变量写入初始配置文件中
f = open("E:\\CDATA\\自动化测试\\Cdata_part11\\src\\config\\initialization_config.py", "w",
         encoding='utf-8')
f.writelines(vars)
f.close()
olt_types = table.row_values(2)[3]
print(olt_types.split(','))

# 通过文件名获得工作表,获取工作表1
for i in range(len(olt_types.split(','))):
    olt_type=(olt_types.split(',')[i])
    table = data.sheet_by_name(olt_type)
    # 读取需要执行的用例
    for rowNum in range(table.nrows):
        if table.row_values(rowNum)[3] == '是':
            script = olt_type+'//'+(table.row_values(rowNum)[2])
            test_case_list.append(script)
            test_case_id.append(int(table.row_values(rowNum)[0]))

# 输出需要执行用例的数量
print('执行的用例数量为%s个' % (len(test_case_list)))

# 生成pytest的命令行
for case_name in test_case_list:
    command = command + case_name + ' '

# 进入测试用例的目录
os.chdir('E:\\CDATA\\自动化测试\\Cdata_part11\\tests')

#执行测试用例
pytest_command = 'pytest  '+ command + ' -s  -x   --alluredir ' \
                                        'E:\\CDATA\\自动化测试\\Cdata_part11\\tests\\workspace\\cdata_test1\\allure-results'


os.system(pytest_command)
