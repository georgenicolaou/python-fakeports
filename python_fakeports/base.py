import socket
from twisted.application.service import Service
from .logger import LogMessages, log
from .signatures import parse_signature


class FakePortsProtocolBase():

    def get_dest_info(self, transport):
        dst_info = transport.socket.getsockopt(socket.SOL_IP, 80, 16)
        dst_port = int(dst_info[2:4].encode("hex"), 16)
        dst_addr = socket.inet_ntoa(dst_info[4:8])
        return dst_addr, dst_port

    def compile_reply(self, signature, data):
        ret = ""
        if signature.type == "match":
            if signature.matches(data):
                ret = signature.compile()
            else:
                ret = signature.compile()
        else:
            ret = signature.compile()
        try:
            return str(ret)
        except:
            return ret

    def send_payload(self, transport, payload):
        transport.write(str(payload))

class PortService(Service):
    def __init__(self, config):
        self.config = config
        self._signatures_tcp = self.load_signatures(self.config.signatures_tcp)
        self._signatures_udp = self.load_signatures(self.config.signatures_udp)

    def load_signatures(self, signatures_dict):
        signatures = {}
        for port, signature in signatures_dict.items():
            sig = parse_signature(signature)
            if sig is None:
                print("[-] Could not parse signature for port %(port)d" % dict(port))
            else:
                signatures[port] = sig
        return signatures

    def get_tcp_signatures(self):
        return self._signatures_tcp

    def get_udp_signatures(self):
        return self._signatures_udp

    def startService(self):
        Service.startService(self)
        log.info(LogMessages.SERVICE_STARTED)
