import sys
import time
import pytest
from os.path import dirname, abspath

base_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, base_path)
from src.FD1616GS.internet_type import *
# from page.telnet_client import *
from src.FD1616GS.ont_auth import *
from src.config.initialization_config import *
from src.xinertel.renix_test import *
import allure
from src.xinertel.unicast66 import *

@allure.feature("ONU认证")
@allure.story("ONU认证方式")
@allure.title("Gpon_SN认证")
@pytest.mark.run(order=1604)
def test_auth_by_sn(login):
    '''
    用例描述：
    ONU通过Gpon_SN的方式认证。
    例如：
    ont add 1 1 sn-auth TEST12345678 ont-lineprofile-id 1 ont-srvprofile-id 1
    '''
    cdata_info("=========ONT Gpon_SN认证测试=========")
    tn = login
    with allure.step('步骤1:发现未注册的ONU。'):
        assert autofind_onu(tn, Gpon_PonID, Gpon_OnuID, Gpon_SN)
    with allure.step('步骤2:在OLT上通过Gpon_SN的方式将ONU注册上线。'):
        assert auth_by_sn(tn, Gpon_PonID, Gpon_OnuID, Ont_Lineprofile_ID, Ont_Srvprofile_ID, Gpon_SN)
    with allure.step('步骤3:添加service_port'):
        assert add_service_port(tn, Gpon_PonID, Gpon_OnuID, Gemport_ID, [2000, 4001])
    with allure.step('步骤4:ONU的以太网口1添加NATIVE-VLAN'):
        assert ont_native_vlan(tn, Gpon_PonID, Gpon_OnuID, Onu_port_ID='1',User_vlan= '2000')
    with allure.step('步骤5:ONU的以太网口2添加NATIVE-VLAN'):
        assert ont_native_vlan(tn, Gpon_PonID, Gpon_OnuID, Onu_port_ID='2',User_vlan= '4001')
    with allure.step('步骤6:测试仪发送双向100000个报文'):
        assert stream_test(stream_rate, stream_num, download_capture_num, port_location)

    # with  allure.step("步骤5:打流测试"):
    #     # 清除测试仪的对象，防止影响下个用例的执行
    #     time.sleep(5)
    #     reset_rom_cmd = ResetROMCommand()
    #     reset_rom_cmd.execute()
    #
    #     # 发流量测试，onu的Eth1发送两条流2000，和vlan2001
    #     # port_location = ['//192.168.0.180/1/9', '//192.168.0.180/1/10']
    #     duration = 10
    #     down_stream_header = (
    #         'ethernetII_1.sourceMacAdd=00:00:00:11:11:11 vlan_1.id=2000  ethernetII_1.destMacAdd=00:00:00:22:22:21 ipv4_1.source=192.168.0.11 ipv4_1.destination=192.168.0.21',
    #        'ethernetII_1.sourceMacAdd=00:00:00:11:11:12 vlan_1.id=2000  ethernetII_1.destMacAdd=00:00:00:22:22:22 ipv4_1.source=192.168.0.12 ipv4_1.destination=192.168.0.22',
    #     )
    #
    #     up_stream_header = (
    #         'ethernetII_1.sourceMacAdd=00:00:00:22:22:21 vlan_1.id=2000  ethernetII_1.destMacAdd=00:00:00:11:11:11 ipv4_1.source=192.168.0.21 ipv4_1.destination=192.168.0.11',
    #         'ethernetII_1.sourceMacAdd=00:00:00:22:22:22 vlan_1.id=2000  ethernetII_1.destMacAdd=00:00:00:11:11:12 ipv4_1.source=192.168.0.22 ipv4_1.destination=192.168.0.12',
    #     )
    #     result_stats = unicast_test(port_location=port_location, down_stream_header=down_stream_header,
    #                                 up_stream_header=up_stream_header, num=2, dataclassname=StreamBlockStats,
    #                                 stream_header=['Ethernet.ethernetII', 'VLAN.vlan', 'IPv4.ipv4', 'UDP.udp'],
    #                                 duration=duration)
    #
    #     # # 判断vlan2000的上下行流量是否都是通的，如果是返回PASS，否则返回FAIL
    #     # result1 = check_stream_static(result_stats[0], result_stats[2])
    #     # # 判断vlan2001的上下行流量是否都是不通的，如果是返回PASS，否则返回FAIL
    #     # result2 = check_stream_static(result_stats[1], result_stats[3])
    #
    #     for i in range(4):
    #         if (result_stats[i].__dict__)['_StreamBlockID'] == 'sourceMacAdd=00:00:00:11:11:11':
    #             result11 = check_stream_static1(result_stats[i])
    #         elif (result_stats[i].__dict__)['_StreamBlockID'] == 'sourceMacAdd=00:00:00:11:11:12':
    #             result12 = check_stream_static1(result_stats[i])
    #
    #         elif (result_stats[i].__dict__)['_StreamBlockID'] == 'sourceMacAdd=00:00:00:22:22:21':
    #             result21 = check_stream_static1(result_stats[i])
    #         elif (result_stats[i].__dict__)['_StreamBlockID'] == 'sourceMacAdd=00:00:00:22:22:22':
    #             result22 = check_stream_static1(result_stats[i])
    #
    #     # 正确的结果vlan2000的能通，vlan2001的不通
    #     if result11 == 'PASS' and result12 == 'PASS' and result21 == 'PASS' and result22 == 'PASS':
    #         result = 'PASS'
    #         cdata_info("ONU端口为transparent:打流测试正常")
    #     else:
    #         result = 'FAIL'
    #         cdata_error("ONU端口为transparent:打流测试失败")
    #     assert result == 'PASS'


@allure.feature("ONU认证")
@allure.story("ONU认证方式")
@allure.title("Gpon_SN的PASSWORD认证")
@pytest.mark.run(order=1605)
def test_auth_by_snpassword(login):
    '''
    用例描述：
    Gpon_SN的PASSWORD认证。
    例如：
    ont add 1 1 password-auth 12345678 ont-lineprofile-id 1 ont-srvprofile-id 1
    '''
    cdata_info("=========ONT Gpon_SNPASSWORD认证测试=========")
    tn = login
    with allure.step('步骤1:发现未注册的ONU。'):
        assert autofind_onu(tn, Gpon_PonID, Gpon_OnuID, Gpon_SN)
    with allure.step('步骤2:在OLT上通过Gpon_SN的PASSWORD的方式将ONU注册上线。'):
        assert auth_by_snpassword(tn, Gpon_PonID, Gpon_OnuID, Ont_Lineprofile_ID, Ont_Srvprofile_ID, Gpon_SN, Gpon_SN_PASSWORD)
    with allure.step('步骤3:添加service_port'):
        assert add_service_port(tn, Gpon_PonID, Gpon_OnuID, Gemport_ID, [2000, 4001])
    with allure.step('步骤4:ONU的以太网口1添加NATIVE-VLAN'):
        assert ont_native_vlan(tn, Gpon_PonID, Gpon_OnuID, '1', '2000')
    with allure.step('步骤5:ONU的以太网口2添加NATIVE-VLAN'):
        assert ont_native_vlan(tn, Gpon_PonID, Gpon_OnuID, '2', '4001')
    with allure.step('步骤6:测试仪发送双向100000个报文'):
        assert stream_test(stream_rate, stream_num, download_capture_num, port_location)



@allure.feature("ONU认证")
@allure.story("ONU认证方式")
@allure.title("Gpon_SN+PASSWORD认证")
@pytest.mark.run(order=1606)
def test_auth_by_sn_password(login):
    '''
    用例描述：
    ONU通过Gpon_SN+PASSWORD的方式认证。
    例如：
    ont add 1 1 sn-auth TEST12345678 password-auth 12345678 ont-lineprofile-id 1 ont-srvprofile-id 1
    '''
    cdata_info("=========ONT Gpon_SN+PASSWORD认证测试=========")
    tn = login
    with allure.step('步骤1:发现未注册的ONU。'):
        assert autofind_onu(tn, Gpon_PonID, Gpon_OnuID, Gpon_SN)
    with allure.step('步骤2:在OLT上通过Gpon_SN+PASSWORD的方式将ONU注册上线。'):
        assert auth_by_sn_password(tn, Gpon_PonID, Gpon_OnuID, Ont_Lineprofile_ID, Ont_Srvprofile_ID, Gpon_SN, Gpon_SN_PASSWORD)
    with allure.step('步骤3:添加service_port'):
        assert add_service_port(tn, Gpon_PonID, Gpon_OnuID, Gemport_ID, [2000, 4001])
    with allure.step('步骤4:ONU的以太网口1添加NATIVE-VLAN'):
        assert ont_native_vlan(tn, Gpon_PonID, Gpon_OnuID, '1', '2000')
    with allure.step('步骤5:ONU的以太网口2添加NATIVE-VLAN'):
        assert ont_native_vlan(tn, Gpon_PonID, Gpon_OnuID, '2', '4001')
    with allure.step('步骤6:测试仪发送双向100000个报文'):
        assert stream_test(stream_rate, stream_num, download_capture_num, port_location)


@allure.feature("ONU认证")
@allure.story("ONU认证方式")
@allure.title("LOID认证")
@pytest.mark.run(order=1607)
def test_auth_by_loid(login):
    '''
    用例描述：
    ONU通过LOID的方式认证。
    例如：
    ont add 1 1 loid-auth 12345678 ont-lineprofile-id 1 ont-srvprofile-id 1
    '''
    cdata_info("=========ONT LOID认证测试=========")
    tn = login
    with allure.step('步骤1:发现未注册的ONU。'):
        assert autofind_onu(tn, Gpon_PonID, Gpon_OnuID, Gpon_SN)
    with allure.step('步骤2:在OLT上通过LOID的方式将ONU注册上线。'):
        assert auth_by_loid(tn, Gpon_PonID, Gpon_OnuID, Ont_Lineprofile_ID, Ont_Srvprofile_ID, Gpon_LOID, Gpon_SN)
    with allure.step('步骤3:添加service_port'):
        assert add_service_port(tn, Gpon_PonID, Gpon_OnuID, Gemport_ID, [2000, 4001])
    with allure.step('步骤4:ONU的以太网口1添加NATIVE-VLAN'):
        assert ont_native_vlan(tn, Gpon_PonID, Gpon_OnuID, '1', '2000')
    with allure.step('步骤5:ONU的以太网口2添加NATIVE-VLAN'):
        assert ont_native_vlan(tn, Gpon_PonID, Gpon_OnuID, '2', '4001')
    with allure.step('步骤6:测试仪发送双向100000个报文'):
        assert stream_test(stream_rate, stream_num, download_capture_num, port_location)


@allure.feature("ONU认证")
@allure.story("ONU认证方式")
@allure.title("LOID+PASSWORD认证")
@pytest.mark.run(order=1608)
def test_auth_by_loid_password(login):
    '''
    用例描述：
    ONU通过Gpon_SN的方式认证。
    例如：
    ont add 1 1 loid-auth 12345678 password-auth 12345678 ont-lineprofile-id 1 ont-srvprofile-id 1
    '''
    cdata_info("=========ONT LOID+PASSWORD认证测试=========")
    tn = login
    with allure.step('步骤1:发现未注册的ONU。'):
        assert autofind_onu(tn, Gpon_PonID, Gpon_OnuID, Gpon_SN)
    with allure.step('步骤2:在OLT上通过LOID+PASSWORD的方式将ONU注册上线。'):
        assert auth_by_loid_password(tn, Gpon_PonID, Gpon_OnuID, Ont_Lineprofile_ID, Ont_Srvprofile_ID, Gpon_LOID, Gpon_LOID_PASSWORD, Gpon_SN)
    with allure.step('步骤3:添加service_port'):
        assert add_service_port(tn, Gpon_PonID, Gpon_OnuID, Gemport_ID, [2000, 4001])
    with allure.step('步骤4:ONU的以太网口1添加NATIVE-VLAN'):
        assert ont_native_vlan(tn, Gpon_PonID, Gpon_OnuID, '1', '2000')
    with allure.step('步骤5:ONU的以太网口2添加NATIVE-VLAN'):
        assert ont_native_vlan(tn, Gpon_PonID, Gpon_OnuID, '2', '4001')
    with allure.step('步骤6:测试仪发送双向100000个报文'):
        assert stream_test(stream_rate, stream_num, download_capture_num, port_location)


if __name__ == '__main__':
    # case_1()
    pytest.main(["-v",'-s',"test_onu_auth_type.py"])




