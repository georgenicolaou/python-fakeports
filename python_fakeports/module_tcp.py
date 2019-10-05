import time
from twisted.internet import protocol

from .base import FakePortsProtocolBase
from .logger import LogMessages, log


class FakePortsProtocolTCP(protocol.Protocol, FakePortsProtocolBase):

    def __init__(self, factory, signatures):
        self.factory = factory
        self.signatures = signatures
        self.data = ""
        self.signature_send = False

    def connectionMade(self):
        self.dst_addr, self.dst_port = self.get_dest_info(self.transport)
        self.src_addr = self.transport.client[0]
        self.bytes_read = 0
        self.signature = self.signatures.get(self.dst_port, None)
        log.info(LogMessages.CONNECTION.format(src_ip=self.src_addr, dst_port=self.dst_port))
        if self.signature and self.signature.send_on_connect:
            self.probe_received()


    def probe_received(self):
        reply = None
        if self.signature:
            reply = self.compile_reply(self.signature, self.data)
            self.transport.write(reply)
            self.signature_send = True
        self.transport.loseConnection()
        if self.factory.config.is_debug():
            log.info(LogMessages.SERVICE_PROBE.format(src_ip=self.src_addr, dst_port=self.dst_port,
                                                       probe=repr(self.data), reply=repr(reply)))

    def dataReceived(self, data):
        if self.signature:
            self.bytes_read += len(data)
            self.data += data
            if self.bytes_read >= self.signature.send_on_bytes_received(self.factory.config):
                if self.signature.must_sleep():
                    time.sleep(self.signature.get_sleep_time(self.factory.config))
                self.probe_received()
        else:
            self.probe_received()


class FakePortsFactoryTCP(protocol.Factory):
    def __init__(self, service, config):
        self.service = service
        self.config = config

    def buildProtocol(self, addr):
        return FakePortsProtocolTCP(self, self.service._signatures_tcp)