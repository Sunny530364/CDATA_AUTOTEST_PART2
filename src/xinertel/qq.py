#!/usr/bin/python
# -*- coding UTF-8 -*-

#author: ZHONGQI

import os,sys
# import scapy
# from scapy.all import *
# from scapy.utils import PcapReader

current_dir = os.getcwd()

from os import path
print(os.path.abspath('.'))

print(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

# print(current_dir)
print(current_dir.index('xinertel'))
packet_dir = current_dir[:current_dir.index('xinertel')] + 'data'
print(packet_dir)
# packet_path1 = (packet_dir + '\\'+ '_'.join(port_location[0][2:].replace('/','.').split('.'))+ '\\')
# packet_path2 = (packet_dir + '\\'+ '_'.join(port_location[1][2:].replace('/','.').split('.'))+ '\\')

#
# print(packet_path1)
# print(packet_path2)


# 当前文件的绝对路径
script_path = os.path.abspath(sys.argv[0])
print(script_path)

if os.path.isfile(script_path):
    current_path, current_file_name_ext = os.path.split(script_path)
    print(current_path, current_file_name_ext)
    current_file_name, extention_name = current_file_name_ext.split('.')

log_folder_path = os.path.join(current_path, "packets")
#如果不存在logs文件夹，则在当前目录下创建logs文件夹
if not os.path.exists(log_folder_path):
    os.makedirs(log_folder_path)

port_location=['//192.168.0.180/1/9', '//192.168.0.180/1/10']
#log的文件名称
file_name = "%s_%s.pcap" % (current_file_name, '_'.join(port_location[1].split('/')[2:]))
log_file_path = os.path.join(log_folder_path, file_name)
print(log_file_path)

# print('_'.join(port_location[1].split('/')[2:]))