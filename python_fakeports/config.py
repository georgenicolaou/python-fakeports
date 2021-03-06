import yaml

class Config():
    def __init__(self, connection, general, signatures_tcp, signatures_udp):
        self.connection = connection
        self.general = general
        self.signatures_tcp = signatures_tcp
        self.signatures_udp = signatures_udp
        self.commandline = False

    def is_debug(self):
        return self.general.get("debug", False)

    def get_host(self, default='localhost'):
        if "host" in self.connection:
            return self.connection['host']
        return default

    def get_port(self, default=4444):
        if "port" in self.connection:
            return self.connection['port']
        return default

    def get_interface(self):
        if "interface" in self.connection:
            return self.connection['interface']
        
    def in_commandline(self, val):
        self.commandline = val

    @classmethod
    def _load(cls, yaml_contents):
        yaml_config = yaml.load(yaml_contents, Loader=yaml.SafeLoader)
        if "connection" in yaml_config:
            return Config(yaml_config["connection"], yaml_config.get("general", {}),
                          yaml_config.get("signatures_tcp", {}), yaml_config.get("signatures_udp", {}))
        else:
            raise ValueError("Invalid sections found in config file, ensure that 'connection' and 'signatures' " +
                             "fields exist")

    @classmethod
    def load_config(cls, config_file):
        with open(config_file, "r") as cfile:
            return Config._load(cfile.read())
        return None