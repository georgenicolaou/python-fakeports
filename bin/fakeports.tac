import os
from twisted.application import internet
from twisted.application.service import MultiService, Application
from twisted.python.log import FileLogObserver, ILogObserver
from twisted.python.logfile import DailyLogFile

CONFIG_FILE = "/etc/fakeports/fakeports.yml"
#CONFIG_FILE = "config.yaml"

from python_fakeports import *

config = Config.load_config(CONFIG_FILE)
multiservice = MultiService()

fakeport_service = PortService(config)
fakeport_service.setServiceParent(multiservice)

port = config.get_port()
iface = config.get_host()

factory_tcp = FakePortsFactoryTCP(fakeport_service, config)
factory_udp = FakePortsFactoryUDP(fakeport_service, config)
tcpservice = internet.TCPServer(port, factory_tcp, interface=iface ).setServiceParent(multiservice)
udpservice = internet.UDPServer(port, FakePortsProtocolUDP(factory_udp, fakeport_service.get_udp_signatures()),
                                interface=iface).setServiceParent(multiservice)

application = Application("python_fakeports")
if config.general.has_key("log"):
    log_dir, log_filename = os.path.split(config.general.get("log"))
    logfile = DailyLogFile(log_filename, log_dir)
    application.setComponent(ILogObserver, FileLogObserver(logfile).emit)

multiservice.setServiceParent(application)