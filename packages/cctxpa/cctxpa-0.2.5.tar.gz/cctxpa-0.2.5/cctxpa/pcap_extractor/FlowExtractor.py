import gc

from dpkt import ethernet, ip, tcp

from .TCPFlow import TCPFlow
from .FlowBase import FlowBase
from .Extractor import Extractor


class FlowExtractor(Extractor):
    # 6-192.168.1.4:13853-192.168.1.5:80 => Flow1
    # 6-192.168.1.5:80-192.168.1.4:13853 => Flow1
    flowMap = {}

    def __init__(self, valueCallback):
        super().__init__(valueCallback)
        self.lastCleanTime = 0
        self.flowMap = {}

    def addPacket(self, ethPacket: ethernet.Ethernet, timestamp: float):
        # 只处理 TCP 和 UDP 包，其它包直接忽略（同时支持处理 IPv4 和 IPv6）
        if not FlowBase.canBeMarkAsFlow(ethPacket):
            return
        # 用四元组（源IP，源端口，目的IP，目的端口标识一条流）
        key = FlowBase.encodeToStr(ethPacket)
        reverseKey = FlowBase.encodeToReverseStr(ethPacket)

        ipPacket = ethPacket.data
        protocol = FlowBase.getProtocol(ethPacket)
        if protocol == ip.IP_PROTO_TCP:
            tcpPacket = ipPacket.data

            # 判断是否已经前面有该流量的记录
            if key in self.flowMap:
                tcpFlow = self.flowMap[key]
                forward = key == tcpFlow.forwardStr
                if forward:
                    tcpFlow.addForwardPacket(ethPacket, timestamp)
                    # check if flow needs to be closed due to fin flag and verify stream
                    if tcpPacket.flags & tcp.TH_FIN:
                        if tcpFlow.isForwardValid():
                            tcpFlow.forwardClosed = True
                        del self.flowMap[key]
                else:
                    tcpFlow.addReversePacket(ethPacket, timestamp)
                    # check if flow needs to be closed due to fin flag and verify stream
                    if tcpPacket.flags & tcp.TH_FIN:
                        if tcpFlow.isReverseValid():
                            tcpFlow.reverseClosed = True
                        del self.flowMap[key]
                if tcpFlow.isValid():
                    self.valueCallback(tcpFlow)

            else:
                # TCP 流不存在的情况下，收到一个 SYN 包创建一个新的 TCP 流
                if not tcpPacket.flags & tcp.TH_SYN:
                    return
                self.flowMap[key] = TCPFlow(ethPacket, timestamp)
                self.flowMap[reverseKey] = self.flowMap[key]

        elif protocol == ip.IP_PROTO_UDP:
            # 处理 UDP 包
            udpPacket = ipPacket.data
            pass

        # 30s清理一次
        if timestamp - self.lastCleanTime > 30:
            self.lastCleanTime = timestamp
            # 清理所有5分钟内没有收到新的包的连接
            needCleanKeys = []
            for key in self.flowMap.keys():
                if timestamp - self.flowMap[key].lastTime > 15:
                    needCleanKeys.append(key)
                elif timestamp - self.flowMap[key].startTime > 15 and self.flowMap[key].totalPayloadBytes == 0:
                    needCleanKeys.append(key)

            for cleanKey in needCleanKeys:
                del self.flowMap[cleanKey]
            gc.collect()

    def done(self):
        pass
        # for key in self.flowMap:
        #     flow = self.flowMap[key]
        #     self.valueCallback(flow)
