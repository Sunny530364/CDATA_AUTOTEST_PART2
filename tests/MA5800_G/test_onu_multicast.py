#!/usr/bin/python
# -*- coding UTF-8 -*-

#author: ZHONGQI


import pytest,allure
from src.MA5800_G.gemport import *
from src.MA5800_G.multicast import *
from src.MA5800_G.vlan_func import *
from src.xinertel.muticast11 import *
from src.MA5800_G.ont_auth import *
from src.config.initialization_config import *

@pytest.fixture(scope='function')
def onu_igmp_suit(login):
    tn=login
    yield tn
    del_multicast_member(tn, Gpon_PonID, Gpon_OnuID, Gemport_ID)

@allure.feature("onu 组播测试")
@allure.story("onu 组播透传测试")
@allure.title("测试onu组播透传的情况")
@pytest.mark.run(order=5822)
def test_ont_igmp_transparent(onu_igmp_suit):
    cdata_info("=========onu为组播透传测试=========")

    tn = onu_igmp_suit
    with allure.step('步骤1:发现未注册的ONU。'):
        assert autofind_onu(tn, Gpon_PonID, Gpon_OnuID, Gpon_SN)
    with allure.step('步骤2:在OLT上通过Gpon_SN的方式将ONU注册上线。'):
        assert auth_by_sn(tn, Gpon_PonID, Gpon_OnuID, Ont_Lineprofile_ID, Ont_Srvprofile_ID, Gpon_SN)
    with allure.step('步骤3：配置onu端口为transparent'):
        assert ont_port_transparent(tn, Gpon_PonID, Gpon_OnuID, Ont_Port_ID)
    with allure.step('步骤4:ONU的以太网口1添加NATIVE-VLAN。'):
        assert ont_native_vlan(tn, Gpon_PonID, Gpon_OnuID, Ont_Port_ID, User_vlan='3000')
    with allure.step("步骤4:修改gemport配置为vlan"):
        assert gemport_vlan(tn, Ont_Lineprofile_ID, [3000], Gemport_ID)
    with allure.step("步骤5:配置虚端口vlan3000透传"):
        assert add_service_port(tn, Gpon_PonID, Gpon_OnuID, Gemport_ID, Vlan_list=[3000])
    with allure.step('步骤6:配置onu组播模式为transparent'):
        assert onu_imgp_transparent(tn,Ont_Srvprofile_ID,Gpon_PonID, Gpon_OnuID, Gemport_ID,Mvlan='3000', User_Vlan='3000')
    with allure.step("步骤6:打流测试"):
        time.sleep(3)
        reset_rom_cmd = ResetROMCommand()
        reset_rom_cmd.execute()
        # 发流测试
        result = multicast_test(port_location=port_location,
                                multicaststream_header=(
                                    'ethernetII_1.destMacAdd=01:00:5e:01:01:01 vlan_1.id=3000 ipv4_1.destination=239.1.1.1'),
                                multicastgroupip='239.1.1.1',
                                duration=10)

        time.sleep(3)
        reset_rom_cmd = ResetROMCommand()
        reset_rom_cmd.execute()
        if result == 'PASS':
            cdata_info("测试onu组播透传的情况:打流测试正常")
        else:
            cdata_error("测试onu组播透传的情况:打流测试失败")

        assert result == 'PASS'

@allure.feature("onu 组播测试")
@allure.story("onu 组播snooping测试")
@allure.title("测试onu组播正常通的情况")
@pytest.mark.run(order=5823)
def test_ont_igmp_snooping(onu_igmp_suit):
    cdata_info("=========onu为组播snooping测试=========")
    tn = onu_igmp_suit
    with allure.step('步骤1:发现未注册的ONU。'):
        assert autofind_onu(tn, Gpon_PonID, Gpon_OnuID, Gpon_SN)
    with allure.step('步骤2:在OLT上通过Gpon_SN的方式将ONU注册上线。'):
        assert auth_by_sn(tn, Gpon_PonID, Gpon_OnuID, Ont_Lineprofile_ID, Ont_Srvprofile_ID, Gpon_SN)
    with allure.step('步骤3：配置onu端口为transparent'):
        assert ont_port_transparent(tn, Gpon_PonID, Gpon_OnuID, Ont_Port_ID)
    with allure.step('步骤4:ONU的以太网口1添加NATIVE-VLAN。'):
        assert ont_native_vlan(tn, Gpon_PonID, Gpon_OnuID, Ont_Port_ID, User_vlan='3000')
    with allure.step("步骤4:修改gemport配置为vlan"):
        assert gemport_vlan(tn, Ont_Lineprofile_ID, [3000], Gemport_ID)
    with allure.step("步骤5:配置虚端口vlan3000透传"):
        assert add_service_port(tn, Gpon_PonID, Gpon_OnuID, Gemport_ID, Vlan_list=[3000])
    with allure.step('步骤6:配置onu组播模式为snooping'):
        assert ont_igmp_snooping(tn,Ont_Srvprofile_ID,Gpon_PonID, Gpon_OnuID, Gemport_ID,Mvlan='3000', User_Vlan='3000')
    with allure.step("步骤6:打流测试"):
        time.sleep(3)
        reset_rom_cmd = ResetROMCommand()
        reset_rom_cmd.execute()
        # 发流测试
        result = multicast_test(port_location=port_location,
                                multicaststream_header=(
                                    'ethernetII_1.destMacAdd=01:00:5e:01:01:01 vlan_1.id=3000 ipv4_1.destination=239.1.1.1'),
                                multicastgroupip='239.1.1.1',
                                duration=10)

        time.sleep(3)
        reset_rom_cmd = ResetROMCommand()
        reset_rom_cmd.execute()
        if result == 'PASS':
            cdata_info("测试onu组播snooping模式的情况:打流测试正常")
        else:
            cdata_error("测试onu组播snooping模式的情况:打流测试失败")

        assert result == 'PASS'

@allure.feature("onu 组播测试")
@allure.story("onu 组播snooping测试")
@allure.title("测试onu跨组播vlan")
@pytest.mark.run(order=5824)
# @pytest.mark.skip("暂时不执行")
def test_ont_cross_mvlan(onu_igmp_suit):
    cdata_info("=========onu为跨组播vlan测试=========")
    Vlan_list = [2000, 2001]
    tn = onu_igmp_suit
    with allure.step('步骤1:发现未注册的ONU。'):
        assert autofind_onu(tn, Gpon_PonID, Gpon_OnuID, Gpon_SN)
    with allure.step('步骤2:在OLT上通过Gpon_SN的方式将ONU注册上线。'):
        assert auth_by_sn(tn, Gpon_PonID, Gpon_OnuID, Ont_Lineprofile_ID, Ont_Srvprofile_ID, Gpon_SN)
    with allure.step('步骤3：配置onu端口为transparent'):
        assert ont_port_transparent(tn, Gpon_PonID, Gpon_OnuID, Ont_Port_ID)
    with allure.step('步骤4:ONU的以太网口1添加NATIVE-VLAN。'):
        assert ont_native_vlan(tn,Gpon_PonID, Gpon_OnuID, Ont_Port_ID, User_vlan='2000')
    with allure.step("步骤4:修改gemport配置为vlan"):
        assert gemport_vlan(tn, Ont_Lineprofile_ID, [2000,3000], Gemport_ID)
    with allure.step("步骤5:配置虚端口vlan2000透传"):
        assert add_service_port(tn, Gpon_PonID, Gpon_OnuID, Gemport_ID, Vlan_list=[2000])
    with allure.step('步骤6:配置onu组播模式为snooping'):
        assert ont_igmp_snooping(tn,Ont_Srvprofile_ID,Gpon_PonID, Gpon_OnuID, Gemport_ID,Mvlan='3000', User_Vlan='2000')
    with allure.step("步骤6:打流测试"):
        time.sleep(3)
        reset_rom_cmd = ResetROMCommand()
        reset_rom_cmd.execute()
        # 发流测试
        result = multicast_test(port_location=port_location,
                                multicaststream_header=(
                                    'ethernetII_1.destMacAdd=01:00:5e:01:01:01 vlan_1.id=3000 ipv4_1.destination=239.1.1.1'),
                                multicastgroupip='239.1.1.1',
                                duration=10)

        time.sleep(3)
        reset_rom_cmd = ResetROMCommand()
        reset_rom_cmd.execute()
        if result == 'PASS':
            cdata_info("测试onu跨组播vlan的情况:打流测试正常")
        else:
            cdata_error("测试onu跨组播vlan的情况:打流测试失败")

        assert result == 'PASS'

if __name__ == '__main__':
    pytest.main(['-v','-s','-x','test_onu_multicast.py'])