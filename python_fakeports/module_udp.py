from twisted.internet import protocol
from .base import FakePortsProtocolBase
from .logger import LogMessages, log

class FakePortsProtocolUDP(protocol.DatagramProtocol, FakePortsProtocolBase):

    def __init__(self, factory, signatures):
        self.factory = factory
        self.signatures = signatures

    def datagramReceived(self, data, addr):
        dst_addr, dst_port = self.get_dest_info(self.transport)
        log.info(LogMessages.SERVICE_PROBE.format(src_ip=addr[0], dst_port=dst_port))
        signature = self.signatures.get(dst_port)
        if signature:
            self.transport.write(self.compile_reply(signature, data), addr)


class FakePortsFactoryUDP(protocol.Factory):
    def __init__(self, service, config):
        self.service = service
        self.config = config

    def buildProtocol(self, addr):
        return FakePortsProtocolUDP(self, self.service._signatures_udp)