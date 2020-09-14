#!/usr/bin/python
# -*- coding UTF-8 -*-

#author: ZHONGQI

import pytest
from src.xinertel.muticast11 import *
from src.FD1616GS.ont_auth import *
from src.config.initialization_config import *
from src.FD1616GS.multicast import *
import allure

#
# @pytest.fixture()
# def ont_snooping_suit(login):
#     cdata_info("=========ONU组播snooping测试=========")
#     tn = login
#     Vlan_list=[3000]
#     User_Vlan = "3000"
#     with allure.step('步骤1:发现未注册的ONU。'):
#         assert autofind_onu(tn, Gpon_PonID,  Gpon_PonID, Gpon_SN)
#     with allure.step('步骤2:在OLT上通过Gpon_SN的方式将ONU注册上线。'):
#         assert auth_by_sn(tn ,Gpon_PonID, Gpon_PonID, Ont_Lineprofile_ID, Ont_Srvprofile_ID, Gpon_SN)
#     with allure.step("步骤3：配置onu端口native-vlan为3000"):
#         assert ont_native_vlan(tn, Gpon_PonID, Gpon_PonID, Ont_Port_ID, User_Vlan)
#     with allure.step("步骤4：添加虚端口vlan透传3000"):
#         assert add_service_port(tn, Gpon_PonID, Gpon_PonID, Gemport_ID, Vlan_list)
#     with allure.step("步骤5:onu端口绑定组播模板"):
#         assert ont_multicast(tn, ponid=Gpon_PonID, ontid=Gpon_PonID, ethid=Ont_Port_ID, ont_igmpprofile_id=200)
#
# @pytest.fixture()
# def ont_cross_mvlan_suit(login):
#     cdata_info("=========ONU组播snooping测试:跨组播vlan测试=========")
#     tn = login
#     Vlan_list=[2000]
#     User_Vlan = "2000"
#     with allure.step('步骤1:发现未注册的ONU。'):
#         assert autofind_onu(tn, Gpon_PonID,  Gpon_PonID, Gpon_SN)
#     with allure.step('步骤2:在OLT上通过Gpon_SN的方式将ONU注册上线。'):
#         assert auth_by_sn(tn, Gpon_PonID, Gpon_PonID, Ont_Lineprofile_ID, Ont_Srvprofile_ID, Gpon_SN)
#     with allure.step("步骤3：配置onu端口native-vlan为2000"):
#         assert ont_native_vlan(tn, Gpon_PonID, Gpon_PonID, Ont_Port_ID, User_Vlan)
#     with allure.step("步骤4：添加虚端口vlan透传2000"):
#         assert add_service_port(tn, Gpon_PonID, Gpon_PonID, Gemport_ID, Vlan_list)
#     with allure.step("步骤5:onu端口绑定组播模板"):
#         assert ont_multicast(tn, ponid=Gpon_PonID, ontid=Gpon_PonID, ethid=Ont_Port_ID, ont_igmpprofile_id = Ont_Igmpprofile_ID)

# #class TestMulicast():

@allure.feature("onu 组播测试")
@allure.story("onu 组播snooping测试")
@allure.title("测试onu组播正常通的情况")
@pytest.mark.run(order=1624)
def test_ont_snooping_001(login):
    '''
    用例描述
    测试目的：ont为snooping模式（mvlan为3000，ip 239.1.1.1）,onu的native-vlan为3000，测试onu为snooping模式下组播239.1.1.1是否通
    测试步骤：
    步骤1:发现未注册的ONU
    步骤2:在OLT上通过Gpon_SN的方式将ONU注册上线
    步骤3:配置onu端口native-vlan为3000
    步骤4:添加虚端口vlan透传3000
    步骤5:onu端口绑定组播模板200（mvlan3000 ,ip 239.1.1.1 ,dynamic acl）
    步骤6:打流测试
    1）服务端发送数据流239.1.1.1，查看onu端口是否收到组播数据流239.1.1.1
    multicaststream_header=('ethernetII_1.destMacAdd=01:00:5e:01:01:01 vlan_1.id=3000 ipv4_1.destination=239.1.1.1')
    预期结果:onu端口无法收到组播数据流
    2）客户端发送report报文加入组播239.1.1.1 ，然后服务端口发送组播239.1.1.1的数据流(带tag3000)，10秒后，停止发流
    预期结果:服务端收到report报文，客户端收到组播数据流239.1.1.1
    3)客户端端口发送离开报文，离开组播组239.1.1.1
    预期结果：客户端接收不到数据
    '''
    renix_info("=========ONU组播snooping测试:组播正常通=========")
    cdata_info("=========ONU组播snooping测试:组播正常通=========")
    tn = login
    Vlan_list=[3000]
    User_Vlan = "3000"
    with allure.step('步骤1:发现未注册的ONU。'):
        assert autofind_onu(tn, Gpon_PonID,  Gpon_OnuID, Gpon_SN)
    with allure.step('步骤2:在OLT上通过Gpon_SN的方式将ONU注册上线。'):
        assert auth_by_sn(tn ,Gpon_PonID, Gpon_OnuID, Ont_Lineprofile_ID, Ont_Srvprofile_ID, Gpon_SN)
    with allure.step("步骤3:配置onu端口native-vlan为3000"):
        assert ont_native_vlan(tn, Gpon_PonID, Gpon_OnuID, Ont_Port_ID, User_Vlan)
    with allure.step("步骤4:添加虚端口vlan透传3000"):
        assert add_service_port(tn, Gpon_PonID, Gpon_OnuID, Gemport_ID, Vlan_list)
    with allure.step("步骤5:onu端口绑定组播模板"):
        assert ont_multicast(tn, Gpon_PonID, Gpon_OnuID, Ont_Port_ID, Ont_Igmpprofile_ID)
    # import time
    # time.sleep(3600)
    with allure.step("步骤6:onu组播打流测试"):
        # 配置ont端口native-vlan为3000，onu端口1绑定组播模板（mvlan3000,ip 239.1.1.1）

        time.sleep(3)
        reset_rom_cmd = ResetROMCommand()
        reset_rom_cmd.execute()
        #发流测试
        result = multicast_test(port_location=port_location,
                       multicaststream_header=('ethernetII_1.destMacAdd=01:00:5e:01:01:01 vlan_1.id=3000 ipv4_1.destination=239.1.1.1'),
                       multicastgroupip='239.1.1.1',
                       duration=10)

        time.sleep(3)
        reset_rom_cmd = ResetROMCommand()
        reset_rom_cmd.execute()
        if result == 'PASS':
            cdata_info("测试onu组播正常通的情况:打流测试正常")
        else:
            cdata_error("测试onu组播正常通的情况:打流测试失败")

        assert result == 'PASS'

@allure.feature("onu 组播测试")
@allure.story("onu 组播snooping测试")
@allure.title("测试onu组播正常不通的情况")
@pytest.mark.run(order=1625)
@pytest.mark.skip("暂时不执行")
def test_ont_snooping_002(login):
    '''
    用例描述
    测试目的：ont为snooping模式（mvlan为3000，ip 239.1.1.1）,onu的native-vlan为3000，测试onu为snooping模式下组播239.2.2.2是否不通
    测试步骤：
    步骤1:发现未注册的ONU
    步骤2:在OLT上通过Gpon_SN的方式将ONU注册上线
    步骤3:配置onu端口native-vlan为3000
    步骤4:添加虚端口vlan透传3000
    步骤5:onu端口绑定组播模板200（mvlan3000 ,ip 239.1.1.1 ,dynamic acl）
    步骤6:打流测试
    1）客户端发送report报文加入组播239.2.2.2 ，然后服务端口发送组播239.2.2.2的数据流
    multicaststream_header=('ethernetII_1.destMacAdd=01:00:5e:02:02:02 vlan_1.id=3000 ipv4_1.destination=239.2.2.2')
    预期结果：服务端口收到report报文收不到，客户端接收不到组播239.2.2.2的组播数据流

    '''
    renix_info("=========ONU组播snooping测试:组播正常不通=========")
    cdata_info("=========ONU组播snooping测试:组播正常不通=========")
    tn = login
    Vlan_list = [3000]
    User_Vlan = "3000"
    with allure.step('步骤1:发现未注册的ONU。'):
        assert autofind_onu(tn, Gpon_PonID, Gpon_OnuID, Gpon_SN)
    with allure.step('步骤2:在OLT上通过Gpon_SN的方式将ONU注册上线。'):
        assert auth_by_sn(tn, Gpon_PonID, Gpon_OnuID, Ont_Lineprofile_ID, Ont_Srvprofile_ID, Gpon_SN)
    with allure.step("步骤3:配置onu端口native-vlan为3000"):
        assert ont_native_vlan(tn, Gpon_PonID, Gpon_OnuID, Ont_Port_ID, User_Vlan)
    with allure.step("步骤4:添加虚端口vlan透传3000"):
        assert add_service_port(tn, Gpon_PonID, Gpon_OnuID, Gemport_ID, Vlan_list)
    with allure.step("步骤5:onu端口绑定组播模板"):
        assert ont_multicast(tn, Gpon_PonID, Gpon_OnuID, Ont_Port_ID,Ont_Igmpprofile_ID)
    with allure.step("步骤6:onu组播打流测试"):

        time.sleep(3)
        reset_rom_cmd = ResetROMCommand()
        reset_rom_cmd.execute()

        result = multicast_test(port_location=port_location,
                       multicaststream_header=('ethernetII_1.destMacAdd=01:00:5e:02:02:02 vlan_1.id=3000 ipv4_1.destination=239.2.2.2'),
                       multicastgroupip='239.2.2.2',
                       check='abnormal',
                       duration=10)
        time.sleep(3)
        reset_rom_cmd = ResetROMCommand()
        reset_rom_cmd.execute()
        if result == 'PASS':
            cdata_info("测试onu组播正常不通的情况:打流测试正常")
        else:
            cdata_error("测试onu组播正常不通的情况:打流测试失败")

        assert result == 'PASS'

@allure.feature("onu 组播测试")
@allure.story("onu 组播snooping测试")
@allure.title("测试onu跨组播vlan")
@pytest.mark.run(order=1626)
def test_ont_cross_mvlan(login):
    '''
    用例描述
    测试目的：ont为snooping模式（mvlan为3000，ip 239.1.1.1）,onu的native-vlan为2000，测试onu的跨组播vlan是否正常的
    测试步骤：
    步骤1:发现未注册的ONU
    步骤2:在OLT上通过Gpon_SN的方式将ONU注册上线
    步骤3:配置onu端口native-vlan为2000
    步骤4:添加虚端口vlan透传2000
    步骤5:onu端口绑定组播模板200（mvlan3000 ,ip 239.1.1.1 ,dynamic acl）
    步骤6:打流测试
    1）客户端发送report报文加入组播239.1.1.1 ，然后服务端口发送组播239.1.1.1的数据流，10秒后，停止发流
    multicaststream_header=('ethernetII_1.destMacAdd=01:00:5e:01:01:01 vlan_1.id=3000 ipv4_1.destination=239.1.1.1')
    预期结果：服务端收到report报文，客户端收到组播数据流239.1.1.1
    2)服务端发送组播数据流，客户端发送离开报文，离开组播组239.1.1.1
    预期结果：客户端接收不到数据

    '''
    renix_info("=========ONU组播snooping测试:跨组播vlan测试=========")
    cdata_info("=========ONU组播snooping测试:跨组播vlan测试=========")
    tn = login
    Vlan_list = [2000]
    User_Vlan = "2000"
    with allure.step('步骤1:发现未注册的ONU。'):
        assert autofind_onu(tn, Gpon_PonID, Gpon_OnuID, Gpon_SN)
    with allure.step('步骤2:在OLT上通过Gpon_SN的方式将ONU注册上线。'):
        assert auth_by_sn(tn, Gpon_PonID, Gpon_OnuID, Ont_Lineprofile_ID, Ont_Srvprofile_ID, Gpon_SN)
    with allure.step("步骤3：配置onu端口native-vlan为2000"):
        assert ont_native_vlan(tn, Gpon_PonID, Gpon_OnuID, Ont_Port_ID, User_Vlan)
    with allure.step("步骤4：添加虚端口vlan透传2000"):
        assert add_service_port(tn, Gpon_PonID, Gpon_OnuID, Gemport_ID, Vlan_list)
    with allure.step("步骤5:onu端口绑定组播模板"):
        assert ont_multicast(tn, Gpon_PonID, Gpon_OnuID,Ont_Port_ID,Ont_Igmpprofile_ID)
    with allure.step("步骤6:onu组播打流测试"):

        time.sleep(3)
        reset_rom_cmd = ResetROMCommand()
        reset_rom_cmd.execute()

        # 发流测试
        result = multicast_test(port_location=port_location,
                                multicaststream_header=('ethernetII_1.destMacAdd=01:00:5e:01:01:01 vlan_1.id=3000 ipv4_1.destination=239.1.1.1'),
                                multicastgroupip='239.1.1.1',
                                duration=10)
        time.sleep(3)
        reset_rom_cmd = ResetROMCommand()
        reset_rom_cmd.execute()
        if result == 'PASS':
            cdata_info("测试onu跨组播vlan的情况:打流测试正常")
        else:
            cdata_error("测试onu跨组播vlan的情况:打流测试失败")

        assert result=='PASS'

if __name__ == '__main__':
    pytest.main(['-v','-s','--count=5','test_onu_multicast.py::test_ont_snooping_001'])


