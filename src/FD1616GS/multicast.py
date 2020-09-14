#!/usr/bin/python
# -*- coding UTF-8 -*-

#author: ZHONGQI

import time
from src.config.telnet_client import *
from src.config.Cdata_loggers import *

def ont_multicast(tn,PonID,OnuID,Ont_Port_ID,Ont_Igmpprofile_ID):
    # 进入gpon视图下
    # 判断当前的视图是否正确。
    tn.write(b"interface gpon 0/0" + b"\n")
    result = tn.read_until(b"OLT(config-interface-gpon-0/0)#", timeout=2)
    if result:
        pass
    else:
        cdata_info("===============ERROR!!!===================")
        cdata_error('当前OLT所在的视图不正确，请检查上一个模块的代码。')
        cdata_info("==========================================")
        tn.write(b"exit" + b"\n")
        result = tn.read_until(b"OLT(config)#", timeout=2)
        return False
    tn.read_until(b'OLT(config-interface-gpon-0/0)# ',timeout=2)
    #onu端口绑定组播模板
    tn.write('ont port attribute {} {} eth {} igmp-profile profile-id {} '.format(PonID,OnuID,Ont_Port_ID,Ont_Igmpprofile_ID).encode()+b'\n')
    tn.read_until(b'OLT(config-interface-gpon-0/0)# ',timeout=2)
    #查看onu端口绑定组播模板是否正常
    tn.write('show ont port attribute {} {} eth all  '.format(PonID,OnuID).encode()+b'\n')
    command_result = tn.read_until(b'OLT(config-interface-gpon-0/0)# ',timeout=2).decode()
    #获取相应行
    result = (((command_result.split('-----------------------------------------------------------------------------')[1]).
          split('----------------------------------------------------------------------------'))[1].split('\r\n')[int(Ont_Port_ID)]).split()
    # print(result,result[-1],type(result[-1]),Ont_Igmpprofile_ID,type(Ont_Igmpprofile_ID))
    if str(Ont_Igmpprofile_ID) == result[-1] :
        cdata_info('onu端口绑定组播模板成功')
        tn.write(b'exit'+b'\n')
        tn.read_until(b'OLT(config)# ', timeout=2)
        return True
    else:
        cdata_error('onu端口绑定组播模板失败')
        tn.write(b'exit' + b'\n')
        tn.read_until(b'OLT(config)# ', timeout=2)
        return False



def del_ont_multicast(tn,PonID, OnuID, Ont_Port_ID):
    # 进入gpon视图下
    # 判断当前的视图是否正确。
    tn.write(b"interface gpon 0/0" + b"\n")
    result = tn.read_until(b"OLT(config-interface-gpon-0/0)#", timeout=2)
    if result:
        pass
    else:
        cdata_info("===============ERROR!!!===================")
        cdata_error('当前OLT所在的视图不正确，请检查上一个模块的代码。')
        cdata_info("==========================================")
        tn.write(b"exit" + b"\n")
        result = tn.read_until(b"OLT(config)#", timeout=2)
        return False
    tn.read_until(b'OLT(config-interface-gpon-0/0)# ',timeout=2)
    #onu端口删除绑定的组播模板
    tn.write('no ont port attribute {} {} eth {} igmp-profile  '.format(PonID, OnuID, Ont_Port_ID).encode() + b'\n')
    tn.read_until(b'OLT(config-interface-gpon-0/0)# ',timeout=2)
    tn.write(b'exit' + b'\n')


if __name__ == '__main__':
    host_ip = '192.168.5.164'
    username = 'root'
    password = 'admin'
    tn = telnet_host(host_ip, username, password)[0]
    ont_multicast(tn)