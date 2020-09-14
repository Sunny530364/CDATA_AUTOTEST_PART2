#!/usr/bin/python
# -*- coding UTF-8 -*-

#author: ZHONGQI



from src.config.telnet_client import *
from src.config.Cdata_loggers import *


#配置onu的组播模式为transparent
def ont_imgp_transparent(tn,PonID,OnuID):
    # 判断当前的视图是否正确。
    tn.write(b"interface epon 0/0" + b"\n")
    result = tn.read_until(b"OLT(config-interface-epon-0/0)#", timeout=2)
    if result:
        pass
    else:
        cdata_info("==========================================")
        cdata_info("===============ERROR!!!===================")
        cdata_error('当前OLT所在的视图不正确，请检查上一个模块的代码。')
        cdata_info("==========================================")
        tn.write(b"exit" + b"\n")
        result = tn.read_until(b"OLT(config)#", timeout=2)
        return False
    result = tn.read_until(b'OLT(config-interface-epon-0/0)# ', timeout=2)
    tn.write(('ont multicast-mode %s %s transparent '%(PonID,OnuID)).encode() + b'\n')
    result = tn.read_until(b'OLT(config-interface-epon-0/0)# ', timeout=2)
    tn.write(('show ont multicast-mode %s %s'%(PonID,OnuID)).encode()+b'\n')
    result = tn.read_until(b'OLT(config-interface-epon-0/0)# ', timeout=2).decode('utf-8')
    if ' Multicast mode     : Transparent' in result :
        cdata_info('onu配置组播模式为transparent正常')
        tn.write(b'exit \n')
        return True
    else:
        cdata_error('onu配置组播模式为transparent失败')
        tn.write(b'exit \n')
        return False

#配置onu的组播模式为snooping
def ont_imgp_snooping(tn,PonID,OnuID,Ont_Port_ID,Mvlan='3000'):
    # 判断当前的视图是否正确。
    tn.write(b"interface epon 0/0" + b"\n")
    result = tn.read_until(b"OLT(config-interface-epon-0/0)#", timeout=2)
    if result:
        pass
    else:
        cdata_info("==========================================")
        cdata_info("===============ERROR!!!===================")
        cdata_error('当前OLT所在的视图不正确，请检查上一个模块的代码。')
        cdata_info("==========================================")
        tn.write(b"exit" + b"\n")
        result = tn.read_until(b"OLT(config)#", timeout=2)
        return False
    result = tn.read_until(b'OLT(config-interface-epon-0/0)# ', timeout=2)
    tn.write(('ont multicast-mode %s %s  igmp-snooping '%(PonID,OnuID)).encode() + b'\n')
    result = tn.read_until(b'OLT(config-interface-epon-0/0)# ', timeout=2)
    tn.write(('show ont multicast-mode %s %s'%(PonID,OnuID)).encode()+b'\n')
    result = tn.read_until(b'OLT(config-interface-epon-0/0)# ', timeout=2).decode('utf-8')
    if 'Multicast mode     : IGMP/MLD Snooping' in result :
        cdata_info('onu配置组播模式为imgp-snooping正常')
        tn.write(b'exit \n')
        return True

    else:
        cdata_error('onu配置组播模式为igmp_snooping失败')
        tn.write(b'exit \n')
        return False

#配置onu端口组播vlan
def ont_igmp_mvlan(tn,PonID,OnuID,Ont_Port_ID,Mvlan):
    # 判断当前的视图是否正确。
    tn.write(b"interface epon 0/0" + b"\n")
    result = tn.read_until(b"OLT(config-interface-epon-0/0)#", timeout=2)
    if result:
        pass
    else:
        cdata_info("==========================================")
        cdata_info("===============ERROR!!!===================")
        cdata_error('当前OLT所在的视图不正确，请检查上一个模块的代码。')
        cdata_info("==========================================")
        tn.write(b"exit" + b"\n")
        result = tn.read_until(b"OLT(config)#", timeout=2)
        return False
    result = tn.read_until(b'OLT(config-interface-epon-0/0)# ', timeout=2)
    tn.write(('ont port multicast-vlan %s %s eth %s %s' % (PonID, OnuID, Ont_Port_ID, Mvlan)).encode() + b'\n')
    result = tn.read_until(b'OLT(config-interface-epon-0/0)# ', timeout=2).decode('utf-8')
    tn.write(('show ont  port multicast-vlan %s %s  eth %s' % (PonID, OnuID, Ont_Port_ID)).encode() + b'\n')
    result = tn.read_until(b'OLT(config-interface-epon-0/0)# ', timeout=2).decode('utf-8')
    if 'Multicast vlan       : %s,'%Mvlan in result:
        cdata_info('onu端口配置组播mvlan正常')
        tn.write(b'exit \n')
        return True
    else:
        cdata_error('onu端口配置组播mvlan失败')
        tn.write(b'exit \n')
        return False

#废弃
def ont_igmp_ctc_mode(PonID, OnuID):
    # 判断当前的视图是否正确。
    tn.write(b"interface epon 0/0" + b"\n")
    result = tn.read_until(b"OLT(config-interface-epon-0/0)#", timeout=2)
    if result:
        pass
    else:
        cdata_info("==========================================")
        cdata_info("===============ERROR!!!===================")
        cdata_error('当前OLT所在的视图不正确，请检查上一个模块的代码。')
        cdata_info("==========================================")
        tn.write(b"exit" + b"\n")
        result = tn.read_until(b"OLT(config)#", timeout=2)
        return False
    result = tn.read_until(b'OLT(config-interface-epon-0/0)# ', timeout=2)
    tn.write(('ont multicast-mode %s %s  ctc ' % (PonID, OnuID)).encode() + b'\n')
    result = tn.read_until(b'OLT(config-interface-epon-0/0)# ', timeout=2)
    tn.write(('show ont multicast-mode %s %s' % (PonID, OnuID)).encode() + b'\n')
    result = tn.read_until(b'OLT(config-interface-epon-0/0)# ', timeout=2).decode('utf-8')
    if 'Multicast mode     : CTC control' in result:
        cdata_info('onu配置组播模式为ctc正常')
        tn.write(b'exit \n')
        return True
    else:
        cdata_info('onu配置组播模式为ctc失败')
        tn.write(b'exit \n')
        return False

#废弃
def olt_igmp_ctc_mode():
    tn.write(b'igmp mode ctc \n')
    tn.read_until(b'OLT(config)# ',timeout=2)

#废弃
def olt_igmp_profile(tn,profile_index,program_index,preview_mode):
    try:
        tn.write(b'btv \n')
        tn.read_until(b'OLT(config-btv)#',timeout=2)
        tn.write(('igmp profile add profile-index %d'%program_index).encode()+b'\n')
        tn.read_until(b'OLT(config-btv)#', timeout=2)
        tn.write(('igmp profile profile-index %s add program-index %s %s '%(profile_index ,program_index,preview_mode)).encode()+b'\n')
        tn.read_until(b'OLT(config-btv)#', timeout=2)
    except:
        raise Exception("配置btv失败")

#废弃
def olt_multicast_vlan():
    tn.write(b'multicast-vlan 3000 \n')
    tn.read_until(b'OLT(config-multicast-vlan-3000)# ',timeout=2)
    tn.write(b'igmp program add program-index 1 ip 239.1.1.1'+b'\n')
    tn.read_until(b'OLT(config-multicast-vlan-3000)# ', timeout=2)
    tn.write(b'igmp program add program-index 1 ip 239.2.2.2' + b'\n')
    tn.read_until(b'OLT(config-multicast-vlan-3000)# ', timeout=2)
    tn.write(b'igmp program add program-index 1 ip 239.2.2.2' + b'\n')
    tn.read_until(b'OLT(config-multicast-vlan-3000)# ', timeout=2)

#废弃
def onu_igmp_ctc_watch(PonID, OnuID):
    #配置onu的组播模式为ctc
    ont_igmp_ctc_mode(PonID, OnuID)
    #配置btv,program_index1 = 239.1.1.1
    olt_igmp_profile(tn,profile_index=1,program_index=1,preview_mode='watch')

#废弃
def onu_igmp_ctc_forbidden():
    # 配置onu的组播模式为ctc
    ont_igmp_ctc_mode(PonID, OnuID)
    # 配置btv,program_index1 = 239.1.1.1
    olt_igmp_profile(tn, profile_index=1, program_index=1, preview_mode='forbidden')

#废弃
def onu_igmp_ctc_preview():
    # 配置onu的组播模式为ctc
    ont_igmp_ctc_mode(PonID, OnuID)
    # 配置btv,program_index1 = 239.1.1.1
    olt_igmp_profile(tn, profile_index=1, program_index=1, preview_mode='forbidden')

#废弃
def imgp_ctc_config():
    # 配置onu的组播模式为ctc
    ont_igmp_ctc_mode(PonID, OnuID)
    #配置olt的组播模式为ctc
    olt_igmp_ctc_mode()
    #配置btv




if __name__ == '__main__':
    host_ip = '192.168.3.138'
    username = 'root'
    password = 'admin'
    ponid = '5'
    ontid = '1'
    ethid = '1'
    tn = telnet_host(host_ip, username, password)[0]
    ont_imgp_snooping(tn,ponid,ontid,ethid)

