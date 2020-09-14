import xlrd
import os
import sys

# 获取当前目录路径
curent_path = os.path.abspath('.')
# update_file = ''
# updatefile_path = os.path.join(curent_path,update_file)

# 清除data目录下的升级文件
os.chdir('E:\\CDATA\\自动化测试\\Cdata_part11\\data')
os.system('del .\*.bin  .\*.tar')
os.chdir(curent_path)

# 从个人文件夹中把升级文件复制到data目录下
os.system('copy .\*.bin  E:\\CDATA\\自动化测试\\Cdata_part11\\data')
os.system('copy .\*.tar  E:\\CDATA\\自动化测试\\Cdata_part11\\data')

test_case_list = []
test_case_id = []
command = ''
# 打开文件夹
filename = sys.argv[1]
data = xlrd.open_workbook(filename)

# 查看工作表
data.sheet_names()

# 通过文件名获得工作表,获取工作表2
table = data.sheet_by_name('GPON')
vars = []
for rowNum in range(1, table.nrows):
    if rowNum == 1:
        vars.append(table.row_values(rowNum)[2] + " = " + (table.row_values(rowNum)[3]) + "\n")
    elif isinstance(table.row_values(rowNum)[3], float):
        vars.append(table.row_values(rowNum)[2] + " = " + '"' + str(int(table.row_values(rowNum)[3])) + '"' + "\n")
    else:
        vars.append(table.row_values(rowNum)[2] + " = " + '"' + str(table.row_values(rowNum)[3]) + '"' + "\n")

f = open("E:\\CDATA\\自动化测试\\Cdata_part11\\src\\config\\initialization_config.py", "w",
         encoding='utf-8')
f.writelines(vars)
f.close()

olt_type = table.row_values(2)[3]

# 通过文件名获得工作表,获取工作表1
table = data.sheet_by_name(olt_type)

# 读取需要执行的用例
for rowNum in range(table.nrows):
    if table.row_values(rowNum)[3] == '是':
        test_case_list.append(table.row_values(rowNum)[2])
        test_case_id.append(int(table.row_values(rowNum)[0]))

# 输出需要执行用例的数量
print('执行的用例数量为%s个' % (len(test_case_list)))

# 简化pytest执行的命令行
# if 2 in test_case_id and 3 in test_case_id and 4 in test_case_id and 5 in test_case_id and 6 in test_case_id:
#     test_case_list.remove('test_onu_auth_type.py::test_auth_by_sn')
#     test_case_list.remove('test_onu_auth_type.py::test_auth_by_snpassword')
#     test_case_list.remove('test_onu_auth_type.py::test_auth_by_sn_password')
#     test_case_list.remove('test_onu_auth_type.py::test_auth_by_loid')
#     test_case_list.remove('test_onu_auth_type.py::test_auth_by_loid_password')
#     test_case_list.append('test_onu_auth_type.py')
#
# if 7 in test_case_id and 8 in test_case_id and 9 in test_case_id:
#     test_case_list.remove('test_onu_internet_type.py::test_dhcp')
#     test_case_list.remove('test_onu_internet_type.py::test_static_ip')
#     test_case_list.remove('test_onu_internet_type.py::test_pppoe_connect')
#     test_case_list.append('test_onu_internet_type.py')
#
# if 10 in test_case_id and 11 in test_case_id and 12 in test_case_id:
#     test_case_list.remove('test_onu_mgt.py::test_deactive_onu')
#     test_case_list.remove('test_onu_mgt.py::test_reboot_onu')
#     test_case_list.remove('test_onu_mgt.py::test_upgrade_onu')
#     test_case_list.append('test_onu_mgt.py')

# 生成pytest的命令行
for case_name in test_case_list:
    command = command + case_name + ' '

# exepath = (os.path.join(os.path.dirname(os.path.abspath('.')),'tests\GonSfu'))
# print(exepath)
# os.chdir(exepath)
# reportpath = os.path.join(exepath,'workspace\cdata_test1\\allure-results')
# pytest_command = 'pytest  ' +command+  ' -s   --alluredir '  +reportpath

# 进入测试用例的目录
os.chdir('E:\\CDATA\\自动化测试\\Cdata_part11\\tests\\EponSfu')
# 执行测试用例
# pytest_command = 'pytest  ' +command+  ' -s  -x --count=1 --alluredir ' \
#                  'E:\\CDATA\\自动化测试\\Cdata_part11\\tests\\GponSfu\\workspace\\cdata_test1\\allure-results'

pytest_command = 'pytest  ' + command + ' -s  -x  --alluredir ' \
                                        'E:\\CDATA\\自动化测试\\Cdata_part11\\tests\\workspace\\cdata_test1\\allure-results'

os.system(pytest_command)



