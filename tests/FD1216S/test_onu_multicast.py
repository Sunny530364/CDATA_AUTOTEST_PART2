#!/usr/bin/python
# -*- coding UTF-8 -*-

#author: ZHONGQI

from src.xinertel.muticast11 import *
from src.FD1216S.ont_multicast import *
from src.FD1216S.vlan_func import *
from src.FD1216S.ont_auth import *
from src.config.initialization_config import *
import pytest
import allure


@pytest.fixture(scope='function')
def onu_igmp_suit(login):
    tn = login
    yield tn
    #配置onu组播为transparent
    with allure.step('onu恢复组播透传的状态'):
        assert ont_imgp_transparent(tn, Epon_PonID, Epon_OnuID)


@allure.feature("onu 组播测试")
@allure.story("onu 组播透传测试")
@allure.title("测试onu组播透传的情况")
@pytest.mark.run(order=1218)
def test_onu_igmp_transparent(login):
    '''
    用例描述
    测试目的：ont为transparent模式,onu端口模式为transparent，测试onu为transparent模式下组播239.1.1.1是否通(olt为snooping模式，vlan为3000，ip 239.1.1.1）)
    测试步骤：
    步骤1:发现未注册的ONU
    步骤2:在OLT上通过MAC的方式将ONU注册上线。
    步骤3:配置onu组播模式为transparent。
   步骤4:打流测试(组播流应该能通)
    1）服务端发送数据流239.1.1.1，查看onu端口是否收到组播数据流239.1.1.1
    multicaststream_header=('ethernetII_1.destMacAdd=01:00:5e:01:01:01 vlan_1.id=3000 ipv4_1.destination=239.1.1.1')
    预期结果:onu端口无法收到组播数据流
    2）客户端发送report报文加入组播239.1.1.1 ，然后服务端口发送组播239.1.1.1的数据流(带tag3000)，10秒后，停止发流
    预期结果:服务端收到report报文，客户端收到组播数据流239.1.1.1
    3)客户端端口发送离开报文，离开组播组239.1.1.1
    预期结果：客户端接收不到数据
    '''
    renix_info("=========ONU端口组播透传测试=========")
    cdata_info("=========ONU端口组播透传测试=========")
    tn = login
    with allure.step('步骤1:发现未注册的ONU。'):
        assert autofind_onu(tn, Epon_PonID, Epon_OnuID, Epon_ONU_MAC)
    with allure.step('步骤2:在OLT上通过MAC的方式将ONU注册上线。'):
        assert auth_by_mac(tn, Epon_PonID, Epon_OnuID, Ont_Lineprofile_ID, Ont_Srvprofile_ID, Epon_ONU_MAC)
    with allure.step('步骤3:配置onu组播模式为transparent。'):
        assert ont_imgp_transparent(tn,Epon_PonID,Epon_OnuID)
    with allure.step('步骤4:打流测试'):
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
            cdata_info("测试onu组播transparent的情况:打流测试正常")
        else:
            cdata_error("测试onu组播transparent的情况:打流测试失败")

        assert result == 'PASS'


@allure.feature("onu 组播测试")
@allure.story("onu 组播snooping测试")
@allure.title("测试onu组播正常通的情况")
@pytest.mark.run(order=1219)
def test_onu_igmp_snooping(onu_igmp_suit):
    '''
    用例描述
    测试目的：ont为snooping模式,onu端口模式为transparent，测试onu为snooping模式下组播239.1.1.1是否通(olt为snooping模式，vlan为3000，ip 239.1.1.1）)
    测试步骤：
    步骤1:发现未注册的ONU
    步骤2:在OLT上通过MAC的方式将ONU注册上线。
    步骤3:配置onu组播模式为snooping。
    步骤4:打流测试(组播应该不通)
    步骤5:配置onu端口的mvlan
    步步骤6：打流测试(组播应该通)
    1）服务端发送数据流239.1.1.1，查看onu端口是否收到组播数据流239.1.1.1
    multicaststream_header=('ethernetII_1.destMacAdd=01:00:5e:01:01:01 vlan_1.id=3000 ipv4_1.destination=239.1.1.1')
    预期结果:onu端口无法收到组播数据流
    2）客户端发送report报文加入组播239.1.1.1 ，然后服务端口发送组播239.1.1.1的数据流(带tag3000)，10秒后，停止发流
    预期结果:服务端收到report报文，客户端收到组播数据流239.1.1.1
    3)客户端端口发送离开报文，离开组播组239.1.1.1
    预期结果：客户端接收不到数据
    '''
    renix_info("=========ONU端口组播snooping测试=========")
    cdata_info("=========ONU端口组播snooping测试=========")
    tn = onu_igmp_suit
    with allure.step('步骤1:发现未注册的ONU。'):
        assert autofind_onu(tn, Epon_PonID, Epon_OnuID, Epon_ONU_MAC)
    with allure.step('步骤2:在OLT上通过MAC的方式将ONU注册上线。'):
        assert auth_by_mac(tn, Epon_PonID, Epon_OnuID, Ont_Lineprofile_ID, Ont_Srvprofile_ID, Epon_ONU_MAC)
    with allure.step('步骤3:配置onu组播模式为snooping。'):
        assert ont_imgp_snooping(tn, Epon_PonID, Epon_OnuID,Ont_Port_ID)
    with allure.step('步骤4:打流测试(组播应该不通)'):
        time.sleep(3)
        reset_rom_cmd = ResetROMCommand()
        reset_rom_cmd.execute()
        # 发流测试
        result = multicast_test(port_location=port_location,
                                multicaststream_header=(
                                    'ethernetII_1.destMacAdd=01:00:5e:01:01:01 vlan_1.id=3000 ipv4_1.destination=239.1.1.1'),
                                multicastgroupip='239.1.1.1',
                                check='abnormal',
                                duration=10)

        time.sleep(3)
        reset_rom_cmd = ResetROMCommand()
        reset_rom_cmd.execute()
        if result == 'PASS':
            cdata_info("测试onu组播snooping(未配置组播mvlan)不通的情况:打流测试正常")
        else:
            cdata_error("测试onu组播snooping(未配置组播mvlan)不通的情况:打流测试失败")

        assert result == 'PASS'
    with allure.step('步骤5:配置onu端口的mvlan'):
        assert ont_igmp_mvlan(tn, Epon_PonID, Epon_OnuID, Ont_Port_ID, Mvlan='3000')
    with allure.step('步骤6：打流测试(组播应该通)'):
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
            cdata_info("测试onu组播snooping(配置组播mvlan)通的情况:打流测试正常")
        else:
            cdata_error("测试onu组播snooping(配置组播mvlan)通的情况:打流测试失败")

        assert result == 'PASS'


@allure.feature("onu 组播测试")
@allure.story("onu 组播snooping测试")
@allure.title("测试onu跨组播vlan")
@pytest.mark.run(order=1220)
def test_onu_cross_mvlan(onu_igmp_suit):
    '''
    用例描述
    测试目的：ont为snooping模式,onu的native-vlan为2000，测试onu的跨组播vlan是否正常的（olt为snooping ,mvlan3000 ,ip239.1.1.1）
    测试步骤：
    步骤1:发现未注册的ONU
    步骤2:在OLT上通过MAC的方式将ONU注册上线。
    步骤3:配置onu组播模式为snooping。
    步骤4:配置onu端口的mvlan
    步骤5:配置onu端口native-vlan为2000
    步骤6:打流测试
    1）客户端发送report报文加入组播239.1.1.1 ，然后服务端口发送组播239.1.1.1的数据流，10秒后，停止发流
    multicaststream_header=('ethernetII_1.destMacAdd=01:00:5e:01:01:01 vlan_1.id=3000 ipv4_1.destination=239.1.1.1')
    预期结果：服务端收到report报文，客户端收到组播数据流239.1.1.1
    2)服务端发送组播数据流，客户端发送离开报文，离开组播组239.1.1.1
    预期结果：客户端接收不到数据

    '''
    renix_info("=========ONU端口跨vlan组播测试=========")
    cdata_info("=========ONU端口跨vlan组播测试=========")
    tn = onu_igmp_suit
    with allure.step('步骤1:发现未注册的ONU。'):
        assert autofind_onu(tn, Epon_PonID, Epon_OnuID, Epon_ONU_MAC)
    with allure.step('步骤2:在OLT上通过MAC的方式将ONU注册上线。'):
        assert auth_by_mac(tn, Epon_PonID, Epon_OnuID, Ont_Lineprofile_ID, Ont_Srvprofile_ID, Epon_ONU_MAC)
    with allure.step('步骤3:配置onu组播模式为snooping。'):
        assert ont_imgp_snooping(tn, Epon_PonID, Epon_OnuID,Ont_Port_ID)
    with allure.step('步骤4:配置onu端口的mvlan'):
        assert ont_igmp_mvlan(tn, Epon_PonID, Epon_OnuID, Ont_Port_ID, Mvlan='3000')
    with allure.step('步骤5:配置onu端口为tag2000'):
        # assert ont_port_tag_remote(tn,Epon_PonID, Epon_OnuID, Ont_Port_ID)
        assert ont_port_tag_remote(tn, Epon_PonID, Epon_OnuID, Ont_Port_ID, User_Vlan)
    with allure.step('步骤6:打流测试'):
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
            cdata_info("测试onu组播transparent的情况:打流测试正常")
        else:
            cdata_error("测试onu组播transparent的情况:打流测试失败")

        assert result == 'PASS'


if __name__ == '__main__':
    pytest.main(['-s','-x','test_onu_multicast.py::test_onu_cross_mvlan'])