#!/usr/bin/python
# -*- coding UTF-8 -*-

#author: ZHONGQI

from renix_py_api.renix import *

initialize()


def create_stream(port,name, rate=10,stream_header = ['Ethernet.ethernetII', 'VLAN.vlan', 'IPv4.ipv4', 'UDP.udp'], packet_length=1024):
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

def start_stream(duration):
    # Start stream and stop stream
    startallstream = StartAllStreamCommand()
    startallstream.execute()
    time.sleep(duration)
    stopallstream = StopAllStreamCommand()
    stopallstream.execute()

sys_entry=get_sys_entry()

#Reserve port1 and port2 in card1 of chassis 192.168.10.1

port_location = ('//192.168.10.1/1/1', '//192.168.10.1/1/2')

port1 = Port(upper=sys_entry, Location=port_location[0])

port2 = Port(upper=sys_entry, Location=port_location[1])

bring_port_online_cmd = BringPortsOnlineCommand(PortList=[port1.handle,port2.handle])

bring_port_online_cmd.execute()

#Create StreamTemplate on Port_1
#
# s1 = StreamTemplate(upper=port1)


stream = StreamTemplate(upper=port1,Name='mytest_demo1')
assert stream.handle
# 配置每条流的速率
# print(stream.get_children('StreamTemplateLoadProfile'))
# stream_template_load_profile = stream.get_children('StreamTemplateLoadProfile')[0]
#
# stream_template_load_profile.edit(Unit=EnumFrameLoadUnit.PERCENT, Rate=10)
# 配置流的报头

# create_stream_header_cmd = CreateHeaderCommand(stream.handle,stream_header= ['Ethernet.ethernetII', 'VLAN.vlan', 'IPv4.ipv4', 'UDP.udp'])
# create_stream_header_cmd.execute()


down_stream_header = (
    'ethernetII_1.sourceMacAdd=00:00:00:11:11:11 vlan_1.id=2000  ethernetII_1.destMacAdd=00:00:00:22:22:21 ipv4_1.source=192.168.1.11 ipv4_1.destination=192.168.1.21',)

edit_stream(stream, parameter=down_stream_header)
cap_conf_1 = port1.get_children('CaptureConfig')[0]
cap_conf_1.edit(CaptureMode=EnumCaptureMode.CTRL_PLANE, CacheCapacity=EnumCacheCapacity.Cache_64KB, FilterMode=EnumFilterMode.NONE, BufferFullAction=EnumBufferFullAction.WRAP, StartingFrameIndex=10, AttemptDownloadPacketCount=1000)

print(cap_conf_1.__dict__)

start_all_cap_cmd = StartAllCaptureCommand()
start_all_cap_cmd.execute()
print( cap_conf_1.__dict__)

start_stream(duration=10)
#View detailed information of Port_1

# port1.get()
#
# print(port1.__dict__)


stop_all_stream_cmd = StopAllStreamCommand()

stop_all_stream_cmd.execute()
print( cap_conf_1.__dict__)

release_port_cmd = ReleasePortCommand(LocationList=port_location)
release_port_cmd.execute()
chassis = DisconnectChassisCommand('HardwareChassis_1')
chassis.execute()




