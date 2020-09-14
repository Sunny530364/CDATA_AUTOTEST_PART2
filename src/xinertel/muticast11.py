#!/usr/bin/python
# -*- coding UTF-8 -*-

#author: ZHONGQI

from renix_py_api import renix
import logging
import time
import re
from src.config.Cdata_loggers import *


renix.initialize(log_level=logging.INFO)
from renix_py_api.api_gen import *
from renix_py_api.rom_manager import *
from renix_py_api.core import EnumRelationDirection

def create_ports(sys_entry, location):
    '''
    连接测试仪，预约端口并且使端口上线
    :param sys_entry:创建测试仪的根节点
    :param location: 存放端口
    :return:port
    '''
    renix_info('create ports with location:'.format(location))
    port1 = Port(upper=sys_entry, location=location[0])
    port2 = Port(upper=sys_entry, location=location[1])
    assert port1.handle
    assert port2.handle
    bring_port_online_cmd = BringPortsOnlineCommand(portlist=[port1.handle, port2.handle])
    bring_port_online_cmd.execute()
    if not wait_port_online(port1):
        raise Exception('bring online port({}) failed'.format(port1.handle))
    if not wait_port_online(port2):
        raise Exception('bring online port({}) failed'.format(port2.handle))
    return port1, port2

def create_stream(port,name, rate=10, packet_length=128,stream_header= ['Ethernet.ethernetII', 'VLAN.vlan', 'IPv4.ipv4', 'UDP.udp']):
    '''
    create stream,add header,'_HeaderTypes': ['ARP.arp', 'Custom.custom', 'DHCPv4.dhcpv4Client', 'DHCPv4.dhcpv4Server',
    'DHCPv6.dhcpv6Client', 'DHCPv6.dhcpv6Server', 'Ethernet.ethernetII', 'Ethernet.8023', 'Goose.goose', 'GRE.gre',
     'GTPv1.gtpv1', 'GTPv1.gtpv1Opt', 'GTPv1Ext.gtpv1Ext', 'GTPv1Ext.gtpv1ExtHdr', 'IGMP.igmpv1', 'IGMP.igmpv2',
     'IGMP.igmpv3Report', 'IGMP.igmpv3Query', 'IGMP.igmpv1Query', 'IGMP.igmpv2Query', 'IPv4.ipv4', 'IPv6.ipv6',
     'ICMPv4.destUnreach', 'ICMPv4.echoReply', 'ICMPv4.echoRequest', 'ICMPv4.informationReply',
      'ICMPv4.informationRequest', 'ICMPv4.parameterProblem', 'ICMPv4.redirect', 'ICMPv4.sourceQuench',
      'ICMPv4.timeExceeded', 'ICMPv4.timestampReply', 'ICMPv4.timestampRequest', 'ICMPv4.icmpMaskRequest',
      'ICMPv4.icmpMaskReply', 'ICMPv6.destinationUnreachable', 'ICMPv6.echoReply', 'ICMPv6.echoRequest',
      'ICMPv6.packetTooBig', 'ICMPv6.parameterProblem', 'ICMPv6.timeExceed', 'ICMPv6.routerSolicit',
      'ICMPv6.routerAdvertise', 'ICMPv6.neighborSolicit', 'ICMPv6.neighborAdvertise', 'L2TPv3.l2tpv3ControlOverIp',
       'L2TPv3.l2tpv3ControlOverUdp', 'L2TPv3.l2tpv3DataOverIp', 'L2TPv3.l2tpv3DataOverUdp', 'L2TPv2.l2tpv2Control',
       'L2TPv2.l2tpv2Data', 'MPLS.mpls', 'Pause.pause', 'PPP.ppp', 'PPPoE.pppoeDiscovery', 'PPPoE.pppoe', 'TCP.tcp',
        'UDP.udp', 'VLAN.vlan', 'VXLAN.vxlan', 'CHDLC.chdlc']
    :param port: 在port上创建数据流
    :param packet_length: 报文的长度
    :return: stream
    '''
    renix_info('port({}) create streams'.format(port.Location))

    stream = StreamTemplate(upper=port,Name=name)
    assert stream.handle
    # 配置每条流的速率
    stream_template_load_profile = stream.get_children('StreamTemplateLoadProfile')[0]

    stream_template_load_profile.edit(Unit=EnumFrameLoadUnit.PERCENT, Rate=rate)
    # 配置流的报头
    create_stream_header_cmd = CreateHeaderCommand(stream.handle,stream_header)
    create_stream_header_cmd.execute()
    # 获取header的配置方法
    # list_instance_leaf_cmd = ListInstanceLeafCommand(stream.handle, Deep=True)
    # list_instance_leaf_cmd.execute()
    # print(list_instance_leaf_cmd.__dict__)
    if len(create_stream_header_cmd.HeaderNames) != len(stream_header):
        raise Exception('{} create EthernetII and IPv4 header failed'.format(stream.handle))
    stream.FixedLength = packet_length
    stream.get()

    return stream

def edit_stream(stream, parameter):
    '''
    编辑流量，
    :param stream:
    :param parameter:需要修改的数据流的参数，字符串类型，举例：'ethernetII_1.destMacAdd=01:00:5e:02:02:02 ipv4_1.destination=239.2.2.2'
    '_Stream': 'StreamTemplate_1', '_ParentName': None, '_Deep': True, '_Leaves': ['ethernetII_1', 'ethernetII_1.destMacAdd',
    'ethernetII_1.sourceMacAdd', 'ethernetII_1.protocolType', 'vlan_1', 'vlan_1.priority', 'vlan_1.cfi', 'vlan_1.id', 'vlan_1.protocol',
    'ipv4_1', 'ipv4_1.version', 'ipv4_1.headLen', 'ipv4_1.tos', 'ipv4_1.tos.tos', 'ipv4_1.tos.tos.precedence', 'ipv4_1.tos.tos.delay',
    'ipv4_1.tos.tos.throughput', 'ipv4_1.tos.tos.reliability', 'ipv4_1.tos.tos.monetaryCost', 'ipv4_1.tos.tos.reserved', 'ipv4_1.tos.diffServe',
     'ipv4_1.tos.diffServe.dscp', 'ipv4_1.tos.diffServe.dscp.codePoint', 'ipv4_1.tos.diffServe.dscp.codePoint.precedence',
     'ipv4_1.tos.diffServe.dscp.classSelector', 'ipv4_1.tos.diffServe.dscp.classSelector.precedence', 'ipv4_1.tos.diffServe.dscp.classSelector.drop',
      'ipv4_1.tos.diffServe.dscp.classSelector.undefine', 'ipv4_1.tos.diffServe.ecnSetting', 'ipv4_1.totalLength', 'ipv4_1.id', 'ipv4_1.flags',
       'ipv4_1.offset', 'ipv4_1.ttl', 'ipv4_1.protocol', 'ipv4_1.checksum', 'ipv4_1.source', 'ipv4_1.destination', 'ipv4_1.ipv4HeaderOption',
       'ipv4_1.padding', 'ipv4_1.gateway', 'udp_1', 'udp_1.sourcePort', 'udp_1.destPort', 'udp_1.length', 'udp_1.checksum'],
       '_CommandState': <ROMCommandStateEnum.INIT: 0>, '_AutoDelete': None, '_StartTime': '', '_ElapsedTime': '', '_Name': None,
       '_Enable': None, '_ROMTag': None, 'force_auto_sync': False, 'args': ['-Stream StreamTemplate_1', '-Deep True'], 'show_return_value': False
    :return:
    '''
    update_header_cmd = UpdateHeaderCommand(Stream=stream.handle, Parameter=parameter)
    update_header_cmd.execute()
    stream.get()
    return stream

def wait_port_online(port, times=10):
    '''
    判断端口是否上线
    :param port:
    :param times:
    :return: True or False
    '''
    port.set_force_auto_sync(True)
    while times:
        if port.Online:
            return True
        else:
            times -= 1
            time.sleep(1)
    else:
        return False

def add_interface(port):
    '''
    add interface
    :param port: 添加port的interface，这里添加的是ipv4接口,也可以添加以太网接口，或者ipv6接口
    :return: interface
    '''
    interface = Interface(upper=port)
    build_ipv4 = BuildInterfaceCommand(InterfaceList=interface.Name, NetworkLayers=['eth', 'ipv4'])
    build_ipv4.execute()
    interface.get()
    return interface

def edit_streamconfig(port):
    '''
    编辑流分类模式
    :param port:
    :return: None
    '''
    stream_port_config = port.get_children('StreamPortConfig')[0]
    stream_port_config.edit(LoadProfileType=EnumLoadProfileType.STREAM_BASE)
    stream_load_profile = stream_port_config.get_children('StreamLoadProfile')[0]
    stream_load_profile.edit(Unit=EnumRateUnit.FRAME_PER_SEC)
    return  stream_load_profile

def add_view(dataclassname):
    '''
    添加统计视图
    :param dataclassname:
    :return:
    '''
    resultview = ResultView(upper=sys_entry, DataClassName=dataclassname)
    resultquery = ResultQuery(upper=resultview)
    SubscribeResultCommand(ResultViewHandles=resultview.handle).execute()
    CommitCommand().execute()
    return resultquery

def creat_view(sys_entry,dataclassname=StreamBlockStats):
    # create result view
    #DataClassName can be PortStats|StreamStats|StreamTxStats|StreamRxStats|StreamblockStats|StreamblockTxStats|StreamblockRxStats
    resultView_create = CreateResultViewCommand(DataClassName=dataclassname.cls_name())
    resultView_create.execute()
    resultView_create = ROMManager.get_object(resultView_create.ResultViewHandle)
    subscribe_result_cmd = SubscribeResultCommand(ResultViewHandles=resultView_create.handle)
    subscribe_result_cmd.execute()
    sys_entry.get()
    page_result_view = sys_entry.get_children(PageResultView.cls_name())[0]
    return page_result_view

def pre_start_stream():
    # Pre-Start stream
    startallstream = StartAllStreamCommand()
    startallstream.execute()
    time.sleep(2)
    stopallstream = StopAllStreamCommand()
    stopallstream.execute()

def start_stream(duration):
    # Start stream and stop stream
    startallstream = StartAllStreamCommand()
    startallstream.execute()
    time.sleep(duration)
    stopallstream = StopAllStreamCommand()
    stopallstream.execute()

def check_port_static(port1_stats,port2_stats):
    # check  port1_stats rx equal to tx
    verdict = 'PASS'
    errInfo =[]
    port1 = (port1_stats.__dict__)['_Name']
    port2 = (port2_stats.__dict__)['_Name']
    if port1_stats.RxTotalFrames == 0 or port1_stats.TxTotalFrames == 0:
        verdict = 'FAIL'
        renix_error(
            '[test fail] {} rx packet ({}) or tx packets ({}) is 0'.format(port1,port1_stats.RxTotalFrames,
                                                                                    port1_stats.TxTotalFrames))
    elif port1_stats.RxTotalFrames / port2_stats.TxTotalFrames < 0.99:
        verdict = 'FAIL'
        renix_error(
            '[test fail] {} rx packet ({})is not equal to  port2_stats tx packets ({})'.format(port1,
                port1_stats.RxTotalFrames, port2_stats.TxTotalFrames))
    else:
        renix_info('[test pass] {} rx packet ({})is  equal to port2_stats tx packets ({})'.format(port1,
            port1_stats.RxTotalFrames,
            port2_stats.TxTotalFrames))

    # check  port2_stats rx equal to tx
    if port2_stats.TxTotalFrames == 0 or port2_stats.RxTotalFrames == 0:
        verdict = 'FAIL'
        renix_error(
            '[test fail] {} rx packet ({}) or tx packets ({}) is 0'.format(port2,port2_stats.RxTotalFrames,
                                                                                    port2_stats.TxTotalFrames))
    elif port2_stats.RxTotalFrames / port1_stats.TxTotalFrames < 0.99:
        verdict = 'fail'
        renix_error(
            '[test fail] {} rx packet ({})is not equal to  port1_stats tx packets ({})'.format(port2,
                port2_stats.RxTotalFrames,
                port1_stats.TxTotalFrames))
    else:
        renix_info('[test pass] {} rx packet ({})is equal to  port1_stats tx packets ({})'.format(port2,
            port2_stats.RxTotalFrames,port1_stats.TxTotalFrames))

    # if verdict == 'FAIL':
    #     for i in errInfo:
    #         renix_error(i)
    return verdict

def check_stream_loss(stream1_2_stats,stream2_1_stats):
    '''
    验证报文不通的情况
    '''
    verdict = 'PASS'
    errInfo=[]
    name1_2 = (stream1_2_stats.__dict__)['_Name']
    name2_1 = (stream2_1_stats.__dict__)['_Name']
    # check  loss packet
    #如果发送报文不为0，接收报文的丢包等于发送报文的个数，则判断改报文不通
    if stream1_2_stats.TxStreamFrames!=0 and stream1_2_stats.RxLossStreamFrames == stream1_2_stats.TxStreamFrames:
        renix_info(
            '[test Pass] {} realtime loss packet ({})is  equal to ({})'.format(name1_2,stream1_2_stats.RxLossStreamFrames,stream1_2_stats.TxStreamFrames))
    else:
        verdict = 'FAIL'
        renix_error('[test Fail] {} realtime loss packet ({})is not equal to ({}) '.format(name1_2,
            stream1_2_stats.RxLossStreamFrames, stream1_2_stats.TxStreamFrames))

    if stream2_1_stats.TxStreamFrames!=0 and stream2_1_stats.RxLossStreamFrames == stream1_2_stats.TxStreamFrames:
        renix_info(
            '[test Pass] {} realtime loss packet ({})is  equal to ({})'.format(name2_1,stream2_1_stats.RxLossStreamFrames,stream2_1_stats.TxStreamFrames))
    else:
        verdict = 'FAIL'
        renix_error('[test Fail] {} realtime loss packet ({})is not equal to ({}) '.format(name2_1,
            stream2_1_stats.RxLossStreamFrames, stream2_1_stats.TxStreamFrames))

    # if verdict == 'FAIL':
    #     for i in errInfo:
    #         renix_error(i)
    return verdict

def check_stream_static(stream1_2_stats,stream2_1_stats):
    verdict='PASS'
    errInfo = []
    # print(stream1_2_stats.__dict__)
    # print(((stream1_2_stats.__dict__)['_Name']).__dict__)
    name1_2 = (stream1_2_stats.__dict__)['_Name']
    name2_1 = (stream2_1_stats.__dict__)['_Name']
    #如果流量发送和接收都不为0，and 接收报文达到发送报文的99%以上，丢包为0，则判断流量正常
    # check rx equal to tx
    if stream1_2_stats.RxStreamFrames == 0 or stream1_2_stats.TxStreamFrames == 0:
        verdict = 'FAIL'
        renix_error(
            '[test fail] {} rx packet ({}) or tx packets ({}) is 0'.format(name1_2,stream1_2_stats.RxStreamFrames,
                                                                                  stream1_2_stats.TxStreamFrames))
    elif stream1_2_stats.RxStreamFrames / stream1_2_stats.TxStreamFrames < 0.99:
        verdict = 'FAIL'
        renix_error(
            '[test fail] {} rx packet ({})is not equal to  tx packets ({})'.format(name,
                stream1_2_stats.RxStreamFrames, stream1_2_stats.TxStreamFrames))
    else:
        renix_info('[test pass] {} rx packet ({})is  equal to tx packets ({})'.format(name1_2,stream1_2_stats.RxStreamFrames,
                                                                                        stream1_2_stats.TxStreamFrames))

    if stream2_1_stats.RxStreamFrames == 0 or stream2_1_stats.TxStreamFrames == 0:
        verdict = 'FAIL'
        renix_error(
            '[test fail] {} rx packet ({}) or tx packets ({}) is 0'.format(name2_1,stream2_1_stats.RxStreamFrames,
                                                                                  stream2_1_stats.TxStreamFrames))
    elif stream2_1_stats.RxStreamFrames / stream2_1_stats.TxStreamFrames < 0.99:
        verdict = 'FAIL'
        renix_error(
            '[test fail] {} rx packet ({})is not equal to  tx packets ({})'.format(name2_1,
                stream2_1_stats.RxStreamFrames, stream2_1_stats.TxStreamFrames))
    else:
        renix_info('[test pass] {} rx packet ({})is  equal to tx packets ({})'.format(name2_1,stream2_1_stats.RxStreamFrames,
                                                                                        stream2_1_stats.TxStreamFrames))
    # if verdict == 'FAIL':
    #     for i in errInfo:
    #         renix_error(i)
    return verdict

def multicast_test(port_location,multicaststream_header,multicastgroupip,check='normal',duration=60,stream_header= ['Ethernet.ethernetII', 'VLAN.vlan', 'IPv4.ipv4' ,'UDP.udp']):
    '''

    multicast test
    :param port_loction: 类型为列表,指的是测试仪端口,举例:port_location=['//192.168.0.180/1/1','//192.168.0.180/1/2']，
    port1为'//192.168.0.180/1/1',port2为'//192.168.0.180/1/2'，port1指的是组播服务端，port2为组播客户器
    :param multicaststream_header:指的是组播数据流的目的ip,目的ip，参数配置可以参考函数edit_stream()中的parameter
    :param multicastgroupip: 指的是组播客户端加入和离开的组播组ip
    :param duration 指的是组播流测试时长,默认为60s
    :return:verdict
    '''
    sys_entry = get_sys_entry()
    verdict = 'PASS'
    errInfo = []

    #创建端口
    port1,port2 = create_ports(sys_entry,port_location)

    # ————————————————创建组播服务器：port1为组播服务器————————————————————————
    # 创建接口
    interface1 = add_interface(port1)
    # 修改端口流发送模式为基于流
    edit_streamconfig(port1)
    # port1添加组播数据流
    #修改流量的目的mac为组播mac,目的ip为组播ip地址
    #multicaststream_header=('ethernetII_1.destMacAdd=01:00:5e:01:01:01 vlan_1.id=3000 ipv4_1.destination=239.1.1.1')

    #获取报文源ip地址，re.findall()返回list列表
    name_ip = re.findall(r'\d+\.\d+\.\d+\.\d+',multicaststream_header)[0]
    name = 'Stream_'+name_ip
    # 创建流模板,并且配置流的名称
    streams_port1 = create_stream(port1, name=name,stream_header=stream_header)
    #编辑流的报文结构
    edit_stream(streams_port1, multicaststream_header)


    #创建组播查询器
    igmpquerierprotocolconfig1 = IgmpQuerierProtocolConfig(upper=port1)
    SelectInterfaceCommand(ProtocolList=[igmpquerierprotocolconfig1.handle], InterfaceList=[interface1.handle]).execute()

    # ————————————————创建组播客户端：port2为客户端——————————————————————————

    #配置组播客户的组播

    #创建接口
    interface2 = add_interface(port2)
    # 添加组播协议
    igmpprotocolconfig1 = IgmpProtocolConfig(upper=port2)
    igmpmembershipsconfig1 = IgmpMembershipsConfig(upper=igmpprotocolconfig1)
    #添加组播节目
    ipv4_multicastgroup = Ipv4MulticastGroup(upper=sys_entry)
    ipv4_multicastgroup.edit(StartIpAddress=multicastgroupip, NumberOfGroups=1)
    # igmp_selectmulticastgroup_cmd = IgmpSelectMulticastGroupCommand(IgmpMemberships='IgmpMembershipsConfig_1', IgmpMulticastGroup='Ipv4MulticastGroup_1')
    # igmp_selectmulticastgroup_cmd.execute()

    #组播协议绑定组播节目
    igmp_selectmulticastgroup_cmd = IgmpSelectMulticastGroupCommand(IgmpMemberships=igmpmembershipsconfig1.Name,IgmpMulticastGroup = ipv4_multicastgroup.Name)
    igmp_selectmulticastgroup_cmd.execute()

    #将组播客户端绑定到接口,用IgmpSelectSourceFilterCommand命令会有问题
    # igmp_selectSourceFilter_cmd = IgmpSelectSourceFilterCommand(IgmpMemberships='IgmpMembershipsConfig_1', IgmpSourceFilter='Interface_1')
    # igmp_selectSourceFilter_cmd.execute()

    #组播协议选择接口
    SelectInterfaceCommand(ProtocolList=[igmpprotocolconfig1.handle], InterfaceList=[interface2.handle]).execute()
    CommitCommand().execute()
    #配置客户端igmp的名称
    (igmpprotocolconfig1.__dict__)['_Name']='igmp_protocol'+multicastgroupip

    # ————————————————创建统计视图———————————————————————————————————
    #创建组播查询统计视图
    resultquery_igmpquerier = add_view('IgmpQuerierResults')

    #创建组播客户端的统计视图
    resultquery_igmpclient = add_view('IgmpPortAggregatedResults')

    # #创建端口统计视图
    # result_query_port = add_view('PortStats')

    #创建组播数据流统计视图
    page_result_view = creat_view(sys_entry)
    result_query_stream = page_result_view.get_children()[0]
    for i in range(5):
        cdata_info('第%d次查看状态：port1的端口状态：%s ;port2的端口状态：%s' % ((i+1),port1.get_children('EthCopper')[0]._LinkStatus._name_,
                                                     port2.get_children('EthCopper')[0]._LinkStatus._name_))
        if port2.get_children('EthCopper')[0]._LinkStatus._name_ == 'UP' and port1.get_children('EthCopper')[
            0]._LinkStatus._name_ == 'UP':

            if check=='normal':
                # ————————————————test1 执行操作 —————————————————————————————————————
                #开始组播查询器
                StartProtocolCommand(ProtocolList=[igmpquerierprotocolconfig1.handle]).execute()

                #发送组播report报文
                IgmpSendReportCommand(IgmpConfigs=[igmpprotocolconfig1.handle]).execute()
                time.sleep(3)

                # 发送组播数据流
                start_stream1 = StartStreamCommand(StreamList=streams_port1.handle)
                start_stream1.execute()
                #发送组播数据流时长
                time.sleep(duration)

                #停止组播数据流
                stop_stream1 = StopStreamCommand(StreamList=streams_port1.handle)
                stop_stream1.execute()
                time.sleep(3)


                # ——————————————查看统计值——————————————————————————————————————
                renix_info('——————————————report test————————————')
                #查看客户端的统计值
                igmpclient_result = resultquery_igmpclient.get_children('IgmpPortAggregatedResults')[0]
                renix_info('igmp_client: IgmpTxFrames is {0}，IgmpTxV2Reports is {1}，IgmpTxLeaveGroups is {2}'.format(igmpclient_result.IgmpTxFrames,igmpclient_result.IgmpTxV2Reports,igmpclient_result.IgmpTxLeaveGroups))
                renix_info('imgp_client: IgmpRxFrame is {0},IgmpRxGeneralQueries is {1},IgmpRxGroupSpecificQueries is {2}'.format(igmpclient_result.IgmpRxFrames,igmpclient_result.IgmpRxGeneralQueries,igmpclient_result.IgmpRxGroupSpecificQueries))

                #查看组播查询器的报文统计
                igmpqueries_result = resultquery_igmpquerier.get_children('IgmpQuerierResults')[0]
                renix_info('igmp_server:  QuerierTxFrames is {0},QuerierRxFrames is {1}'.format(igmpqueries_result.QuerierTxFrames,igmpqueries_result.QuerierRxFrames))


                # 查看组播数据流发送统计
                stream1_stats2 = result_query_stream.get_children('StreamBlockStats')[0]
                name_stream = (stream1_stats2.__dict__)['_StreamBlockID']

                if stream1_stats2.TxStreamFrames!=0 and stream1_stats2.RxStreamFrames!=0 and stream1_stats2.RxStreamFrames/stream1_stats2.TxStreamFrames>=0.99:
                    renix_info('[igmp_report test pass][{}] igmp_server tx igmp packet:{},igmp_client rx igmp packet:{}'.format(
                        name_stream,stream1_stats2.TxStreamFrames, stream1_stats2.RxStreamFrames))
                else:
                    verdict = 'FAIL'
                    renix_error(
                        '[igmp_report test fail][{}] igmp_server tx igmp packet:{},igmp_client rx igmp packet:{}'.format(
                            name_stream,stream1_stats2.TxStreamFrames, stream1_stats2.RxStreamFrames))

                #————————————————组播离开报文的测试————————————————————————————————
                renix_info('——————————————leave test————————————')
                #清除组播数据流统计
                result_clear_cmd = ClearResultCommand(ResultViewHandles=page_result_view.handle)
                result_clear_cmd.execute()
                time.sleep(3)

                #发送组播离开报文
                IgmpSendLeaveCommand(IgmpConfigs=[igmpprotocolconfig1.handle]).execute()
                time.sleep(10)

                # 发送组播数据流
                start_stream1 = StartStreamCommand(StreamList=streams_port1.handle)
                start_stream1.execute()
                time.sleep(5)

                # 停止组播数据流
                stop_stream1 = StopStreamCommand(StreamList=streams_port1.handle)
                stop_stream1.execute()
                time.sleep(3)

                #查看组播客户端发送的协议报文
                igmpclient_result = resultquery_igmpclient.get_children('IgmpPortAggregatedResults')[0]
                renix_info('igmp_client: IgmpTxFrames is {0}，IgmpTxV2Reports is {1}，IgmpTxLeaveGroups is {2}'.format(
                    igmpclient_result.IgmpTxFrames, igmpclient_result.IgmpTxV2Reports, igmpclient_result.IgmpTxLeaveGroups))

                # 查看组播数据流发送统计

                stream1_stats2 = result_query_stream.get_children('StreamBlockStats')[0]
                # print('组播数据流发送：{0}，接收到组播数据流：{1}'.format(stream1_stats2.TxStreamFrames, stream1_stats2.RxStreamFrames))
                if stream1_stats2.RxStreamFrames>2:
                    verdict = 'FAIL'
                    renix_error('[igmp_leave test fail]{} igmp_client tx leave packet ,result:igmp_server tx:{},igmp_client rx：{}'.format(name_stream,stream1_stats2.TxStreamFrames,stream1_stats2.RxStreamFrames))
                else:
                    renix_info('[igmp_leave test pass]{} igmp_client tx leave packet ,result:igmp_server tx:{},igmp_client rx：{}'.format(name_stream,stream1_stats2.TxStreamFrames,stream1_stats2.RxStreamFrames))

            elif check=='abnormal':
                # ————————————————组播不通的执行操作 —————————————————————————————————————
                # 开始组播查询器
                StartProtocolCommand(ProtocolList=[igmpquerierprotocolconfig1.handle]).execute()
                # 发送组播report报文
                IgmpSendReportCommand(IgmpConfigs=[igmpprotocolconfig1.handle]).execute()
                time.sleep(3)
                # 发送组播数据流
                start_stream1 = StartStreamCommand(StreamList=streams_port1.handle)
                start_stream1.execute()
                # 发送组播数据流时长
                time.sleep(duration)

                # 停止组播数据流
                stop_stream1 = StopStreamCommand(StreamList=streams_port1.handle)
                stop_stream1.execute()
                time.sleep(3)

                # ——————————————查看统计值——————————————————————————————————————
                renix_info('——————————————report test————————————')
                # 查看客户端的统计值
                igmpclient_result = resultquery_igmpclient.get_children('IgmpPortAggregatedResults')[0]
                renix_info('igmp_client: IgmpTxFrames is {0}，IgmpTxV2Reports is {1}，IgmpTxLeaveGroups is {2}'.format(
                    igmpclient_result.IgmpTxFrames, igmpclient_result.IgmpTxV2Reports, igmpclient_result.IgmpTxLeaveGroups))
                renix_info('imgp_client: IgmpRxFrame is {0},IgmpRxGeneralQueries is {1},IgmpRxGroupSpecificQueries is {2}'.format(
                    igmpclient_result.IgmpRxFrames, igmpclient_result.IgmpRxGeneralQueries,
                    igmpclient_result.IgmpRxGroupSpecificQueries))

                # 查看组播查询器的报文统计
                igmpqueries_result = resultquery_igmpquerier.get_children('IgmpQuerierResults')[0]
                renix_info('igmp_server:  QuerierTxFrames is {0},QuerierRxFrames is {1}'.format(igmpqueries_result.QuerierTxFrames,
                                                                                           igmpqueries_result.QuerierRxFrames))

                # 查看组播数据流发送统计
                stream1_stats2 = result_query_stream.get_children('StreamBlockStats')[0]
                name_stream = (stream1_stats2.__dict__)['_StreamBlockID']

                if stream1_stats2.RxStreamFrames==0 and stream1_stats2.TxStreamFrames!=0:
                    renix_info('[igmp_report test pass][{}] igmp_server tx igmp packet:{},igmp_client rx igmp packet:{}'.format(
                        name_stream,stream1_stats2.TxStreamFrames, stream1_stats2.RxStreamFrames))

                else:
                    verdict = 'FAIL'
                    renix_error(
                        '[igmp_report test fail][{}] igmp_server tx igmp packet:{},igmp_client rx igmp packet:{}'.format(
                            name_stream,
                            stream1_stats2.TxStreamFrames, stream1_stats2.RxStreamFrames))

                # ————————————————组播离开报文的测试————————————————————————————————
                renix_info('——————————————leave test————————————')
                # 清除流统计
                result_clear_cmd = ClearResultCommand(ResultViewHandles=page_result_view.handle)
                result_clear_cmd.execute()
                time.sleep(3)

                # 发送组播离开报文
                IgmpSendLeaveCommand(IgmpConfigs=[igmpprotocolconfig1.handle]).execute()
                time.sleep(10)

                # 发送组播数据流
                start_stream1 = StartStreamCommand(StreamList=streams_port1.handle)
                start_stream1.execute()
                time.sleep(5)

                # 停止组播数据流
                stop_stream1 = StopStreamCommand(StreamList=streams_port1.handle)
                stop_stream1.execute()
                time.sleep(3)

                # 查看组播客户端发送的协议报文
                igmpclient_result = resultquery_igmpclient.get_children('IgmpPortAggregatedResults')[0]
                renix_info('igmp_client: IgmpTxFrames is {0}，IgmpTxV2Reports is {1}，IgmpTxLeaveGroups is {2}'.format(
                    igmpclient_result.IgmpTxFrames, igmpclient_result.IgmpTxV2Reports, igmpclient_result.IgmpTxLeaveGroups))

                # 查看组播数据流发送统计

                stream1_stats2 = result_query_stream.get_children('StreamBlockStats')[0]
                # print('组播数据流发送：{0}，接收到组播数据流：{1}'.format(stream1_stats2.TxStreamFrames, stream1_stats2.RxStreamFrames))
                if stream1_stats2.RxStreamFrames > 2:
                    verdict = 'FAIL'
                    renix_error(
                        '[igmp_leave test fail]{} igmp_client tx leave packet ,result:igmp_server tx:{},igmp_client rx：{}'.format(
                            name_stream, stream1_stats2.TxStreamFrames, stream1_stats2.RxStreamFrames))
                else:
                    renix_info(
                        '[igmp_leave test pass]{} igmp_client tx leave packet ,result:igmp_server tx:{},igmp_client rx：{}'.format(
                            name_stream, stream1_stats2.TxStreamFrames, stream1_stats2.RxStreamFrames))
            break
        else:
            time.sleep(5)
            continue

    # ———————————————判断测试结果————————————————————————————————————

    print('verdict:',verdict)
    print('errInfo:')
    if verdict == 'FAIL':
        for i in errInfo:
            renix_error(i)

    #释放端口，断开连接
    release_port_cmd = ReleasePortCommand(LocationList=port_location).execute()
    chassis = DisconnectChassisCommand('HardwareChassis_1').execute()
    return verdict


if __name__=='__main__':
    port_location = ['//192.168.0.180/1/9', '//192.168.0.180/1/10']
    multicaststream_header = ('ethernetII_1.destMacAdd=01:00:5e:01:01:01 vlan_1.id=3000 ipv4_1.destination=239.1.1.1')
    multicastgroupip ='239.1.1.1'
    duration = 20
    # unicaststream_header = ('ethernetII_1.sourceMacAdd=00:00:00:11:11:11 ethernetII_1.destMacAdd=00:00:00:22:22:22',
    #                         'ethernetII_1.sourceMacAdd=00:00:00:22:22:22 ethernetII_1.destMacAdd=00:00:00:11:11:11')
    # unicast_test(port_location=port_location)

    multicast_test(port_location=port_location,multicaststream_header=multicaststream_header,multicastgroupip=multicastgroupip)
    time.sleep(3)
    reset_rom_cmd = ResetROMCommand()
    reset_rom_cmd.execute()
