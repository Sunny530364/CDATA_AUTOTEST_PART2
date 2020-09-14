#!/usr/bin/python
# -*- coding UTF-8 -*-

#author: ZHONGQI

from telnetlib import Telnet
import time
import logging
import sys



def telnet_onu():
    host_ip = '192.168.101.1'
    username = 'root'
    password = 'root626'
    try:
        tn = Telnet(host_ip, port=23)
        Telnet.set_debuglevel(tn, debuglevel=1)
        tn.read_until(b"login: ")
        tn.write(username.encode() + b"\n")
        tn.read_until(b"Password: ")
        tn.write(password.encode() + b"\n")
        tn.read_until(b"#", timeout=2)
        print('登录设备')
        tn.write(b'flash get PON_MODE \n')
        result = tn.read_until(b'#',timeout=2).decode('utf-8')
        if 'PON_MODE=2' in result :
            print('ONU是EPON')
            return 'EPON'
        elif 'PON_MODE=2' in result:
            print('ONU是GPON')
            return 'GPON'
    except:
        print("telnet连接失败,或者配置失败")


telnet_onu()