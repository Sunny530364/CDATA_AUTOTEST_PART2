from renix_py_api.renix import *
import logging, time

initialize(log_level=logging.INFO)
from renix_py_api.api_gen import *
from renix_py_api.core import EnumRelationDirection
from renix_py_api.rom_manager import *
from src.config.initialization_config import *
from src.config.Cdata_loggers import *

# 占用测试仪接口
def create_ports(sys_entry, locations):
    renix_info('Create ports with locations:{}'.format(locations))
    port1 = Port(upper=sys_entry, location=locations[0])
    port2 = Port(upper=sys_entry, location=locations[1])
    assert port1.handle
    assert port2.handle
    bring_port_online_cmd = BringPortsOnlineCommand(portlist=[port1.handle, port2.handle])
    bring_port_online_cmd.execute()
    print(wait_port_online(port1))
    if not wait_port_online(port1):
        raise Exception('bring online port({}) failed'.format(port1.handle))
    if not wait_port_online(port2):
        raise Exception('bring online port({}) failed'.format(port2.handle))
    return port1, port2


# 创建带VLAN的数据量
def create_stream_vlan(port, packet_length=128):
    renix_info('port({}) create streams'.format(port_location))
    stream = StreamTemplate(upper=port)
    assert stream.handle
    create_stream_header_cmd = CreateHeaderCommand(stream.handle,
                                                   ['Ethernet.ethernetII', 'VLAN.vlan', 'IPv4.ipv4', 'UDP.udp'])
    create_stream_header_cmd.execute()
    if len(create_stream_header_cmd.HeaderNames) != 4:
        raise Exception('{} create EthernetII and IPv4 header failed'.format(stream.handle))
    stream.FixedLength = packet_length
    stream.get()
    return stream


# 创建不带VLAN的数据量
def create_stream(port, packet_length=128):
    renix_info('port({}) create streams'.format(port_location))
    stream = StreamTemplate(upper=port)
    assert stream.handle
    create_stream_header_cmd = CreateHeaderCommand(stream.handle, ['Ethernet.ethernetII', 'IPv4.ipv4', 'UDP.udp'])
    create_stream_header_cmd.execute()
    if len(create_stream_header_cmd.HeaderNames) != 3:
        raise Exception('{} create EthernetII and IPv4 header failed'.format(stream.handle))
    stream.FixedLength = packet_length
    stream.get()
    return stream


# 编辑数据流
def edit_stream(stream, parameter):
    update_header_cmd = UpdateHeaderCommand(Stream=stream.handle, Parameter=parameter)
    update_header_cmd.execute()
    stream.get()


# 等待测试仪端口上线
def wait_port_online(port, times=30):
    while times:
        if port.Online:
            return True
        else:
            times -= 1
            time.sleep(1)
    else:
        return False


# 发送数据流测试
def stream_test(stream_rate, stream_num, download_capture_num, port_location):
    time.sleep(3)
    reset_rom_cmd = ResetROMCommand()
    reset_rom_cmd.execute()
    # service-port配置完成后，需要等待一段时间流才能通
    time.sleep(10)
    sys_entry = get_sys_entry()

    # 占用测试仪端口
    port1, port2 = create_ports(sys_entry, port_location)

    # 插卡测试仪接口当前的双工速率
    cdata_info("===========================================================================")
    cdata_info("当前端口1的协商速率为：%s" % ((port1.get_children('EthCopper')[0].LineSpeed._name_)))
    cdata_info("当前端口2的协商速率为：%s" % ((port2.get_children('EthCopper')[0].LineSpeed._name_)))
    cdata_info("===========================================================================")

    # 配置测试仪Load Profiles模板(速率为10%，打流方式为突发方式，双向发送100000个报文)
    stream_port_cfg_1 = port1.get_children(StreamPortConfig.cls_name())[0]
    inter_frame_gap_cfg_1 = stream_port_cfg_1.get_children(InterFrameGapProfile.cls_name())[0]
    inter_frame_gap_cfg_1.edit(Rate=int(stream_rate))
    stream_port_cfg_2 = port2.get_children(StreamPortConfig.cls_name())[0]
    inter_frame_gap_cfg_2 = stream_port_cfg_2.get_children(InterFrameGapProfile.cls_name())[0]
    inter_frame_gap_cfg_2.edit(Rate=int(stream_rate))
    stream_port_cfg_1.edit(TransmitMode=EnumTransmitMode.BURST)
    stream_port_cfg_2.edit(TransmitMode=EnumTransmitMode.BURST)
    stream_port_cfg_1.get()
    stream_port_cfg_2.get()
    Burst_transmit_config_1 = stream_port_cfg_1.get_children('BurstTransmitConfig')[0]
    Burst_transmit_config_2 = stream_port_cfg_2.get_children('BurstTransmitConfig')[0]
    Burst_transmit_config_1.edit(FramePerBurst=int(stream_num))
    Burst_transmit_config_2.edit(FramePerBurst=int(stream_num))

    # 创建数据流
    stream1_2 = create_stream(port1)
    stream2_1 = create_stream(port2)
    edit_stream(stream1_2, 'ethernetII_1.sourceMacAdd=00:00:00:22:11:11 ethernetII_1.destMacAdd=00:00:00:11:22:22')
    edit_stream(stream2_1, 'ethernetII_1.sourceMacAdd=00:00:00:11:22:22 ethernetII_1.destMacAdd=00:00:00:22:11:11')
    # edit_stream(stream1_2,'vlan_1.id.XetModifier.StreamType=InterModifier vlan_1.id.XetModifier.Type=Increment vlan_1.id.XetModifier.Start=1001 vlan_1.id.XetModifier.Step=1 vlan_1.id.XetModifier.Count=5')
    # edit_stream(stream2_1,'vlan_1.id.XetModifier.StreamType=InterModifier vlan_1.id.XetModifier.Type=Increment vlan_1.id.XetModifier.Start=1001 vlan_1.id.XetModifier.Step=1 vlan_1.id.XetModifier.Count=5')
    edit_stream(stream1_2,
                'ipv4_1.destination.XetModifier.StreamType=InterModifier ipv4_1.destination.XetModifier.Type=Increment ipv4_1.destination.XetModifier.Start=192.168.111.222 ipv4_1.destination.XetModifier.Step=1 ipv4_1.destination.XetModifier.Count=1')
    edit_stream(stream2_1,
                'ipv4_1.destination.XetModifier.StreamType=InterModifier ipv4_1.destination.XetModifier.Type=Increment ipv4_1.destination.XetModifier.Start=192.168.111.111 ipv4_1.destination.XetModifier.Step=1 ipv4_1.destination.XetModifier.Count=1')
    edit_stream(stream1_2,
                'ipv4_1.source.XetModifier.StreamType=InterModifier ipv4_1.source.XetModifier.Type=Increment ipv4_1.source.XetModifier.Start=192.168.111.111 ipv4_1.source.XetModifier.Step=1 ipv4_1.source.XetModifier.Count=1')
    edit_stream(stream2_1,
                'ipv4_1.source.XetModifier.StreamType=InterModifier ipv4_1.source.XetModifier.Type=Increment ipv4_1.source.XetModifier.Start=192.168.111.222 ipv4_1.source.XetModifier.Step=1 ipv4_1.source.XetModifier.Count=1')
    stream1_2.set_relatives('RxPort', port2, EnumRelationDirection.TARGET)
    stream2_1.set_relatives('RxPort', port1, EnumRelationDirection.TARGET)

    # 配置测试仪查看测试结果的视图
    resultView_create = CreateResultViewCommand(DataClassName=StreamBlockStats.cls_name())
    resultView_create.execute()
    resultView_create = ROMManager.get_object(resultView_create.ResultViewHandle)
    subscribe_result_cmd = SubscribeResultCommand(ResultViewHandles=resultView_create.handle)
    subscribe_result_cmd.execute()
    # cap_conf_1 = port1.get_children('CaptureConfig')[0]
    # cap_conf_2 = port2.get_children('CaptureConfig')[0]

    # 开始测试仪抓包
    # start_all_cap_cmd = StartAllCaptureCommand()
    # start_all_cap_cmd.execute()
    sys_entry.get()
    page_result_view = sys_entry.get_children(PageResultView.cls_name())[0]

    # 开始测试仪发包
    for i in range(0, 5):
        cdata_info(
            '第%d次查看状态：port1的端口状态：%s ;port2的端口状态：%s' % ((i + 1), port1.get_children('EthCopper')[0]._LinkStatus._name_,
                                                       port2.get_children('EthCopper')[0]._LinkStatus._name_))
        # 开始测试仪发包
        if port2.get_children('EthCopper')[0]._LinkStatus._name_ == 'UP' and port1.get_children('EthCopper')[0]._LinkStatus._name_ == 'UP':
            start_all_stream_cmd = StartAllStreamCommand()
            start_all_stream_cmd.execute()
            time.sleep(10)
            result_query = page_result_view.get_children()[0]
            # 读取测试仪接口的发包和收包数据
            stream1_2_stats = result_query.get_children()[0]
            stream2_1_stats = result_query.get_children()[1]

            cdata_info('上行收到的报文数量为：'+str(stream2_1_stats.RxStreamFrames))
            cdata_info('下行收到的报文数量为：'+str(stream1_2_stats.RxStreamFrames))
        else:
            time.sleep(10)
            continue
        # 判断是否丢包
        if stream1_2_stats.RxStreamFrames == int(stream_num) and stream2_1_stats.RxStreamFrames == int(stream_num) and stream1_2_stats.RxLossStreamFrames == 0 and stream2_1_stats.RxLossStreamFrames == 0:
            print("测试仪发流成功")
            release_port_cmd = ReleasePortCommand(LocationList=port_location)
            release_port_cmd.execute()
            chassis = DisconnectChassisCommand('HardwareChassis_1')
            chassis.execute()
            time.sleep(3)
            reset_rom_cmd = ResetROMCommand()
            reset_rom_cmd.execute()
            return True
        else:
            result_clear_cmd = ClearAllResultCommand()
            result_clear_cmd.execute()

    else:
        print("测试仪发流失败")
        release_port_cmd = ReleasePortCommand(LocationList=port_location)
        release_port_cmd.execute()
        chassis = DisconnectChassisCommand('HardwareChassis_1')
        chassis.execute()
        time.sleep(3)
        reset_rom_cmd = ResetROMCommand()
        reset_rom_cmd.execute()
        return False


if __name__ == '__main__':
    for i in range(1, 100):
        if stream_test('10', '100000', '100000', ['//192.168.0.180/1/1', '//192.168.0.180/1/2']):
            print("===========================================================================")
            print("第%s次测试成功" % (i))
            print("===========================================================================")
        else:
            print("===========================================================================")
            print("第%s次测试失败" % (i))
            exit
