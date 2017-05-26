from twisted.logger import Logger
log = Logger("fakeports")

class LogMessages:
    PORT_PROBE = "[PROBE] {src_ip}:{dst_port}"
    SERVICE_PROBE = "[SERVICE_PROBE] {src_ip}:{dst_port} Probe: {probe} Reply: {reply}"
    SERVICE_STARTED = "[SERVICE] Started"
    CONNECTION = "[CONNECTION] {src_ip}:{dst_port}"