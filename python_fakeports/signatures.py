import re

from . import exrex


class BaseSignature(object):
    def __init__(self):
        self.bytes_before_send = None
        self.sleep_seconds = None

    def send_on_connect(self):
        if self.bytes_before_send is not None and self.bytes_before_send == 0:
            return True
        return False

    def send_on_bytes_received(self, config):
        if self.bytes_before_send is not None:
            return self.bytes_before_send
        return config.general.get('bytes_before_answer', 5)

    def must_sleep(self):
        if self.sleep_seconds is not None and self.sleep_seconds != 0:
            return True
        return False

    def get_sleep_time(self, config):
        if self.sleep_seconds is not None:
            return self.sleep_seconds
        return config.general.get('sleep_before_answer', 0)

    @classmethod
    def final_parse(cls, obj, desc):
        if "bytes_before_answer" in desc:
            obj.bytes_before_send = desc["bytes_before_answer"]
        if "sleep_before_answer" in desc:
            obj.sleep_seconds = desc["sleep_before_answer"]
        return obj

class SimpleSignature(BaseSignature):

    def __init__(self, payload):
        self.type = "simple"
        self._payload = payload
        super(SimpleSignature, self).__init__()


    def compile(self):
        return self._payload

    @classmethod
    def parse(cls, descr):
        assert "payload" in descr
        return BaseSignature.final_parse(SimpleSignature(descr['payload']), descr)

class RegexSignature(BaseSignature):

    def __init__(self, payload, args=None):
        self.type = "regex"
        self._payload = payload
        self._args = args
        super(RegexSignature, self).__init__()

    def compile(self, args=None):
        return exrex.getone(self._payload, args=args or self._args)

    @classmethod
    def parse(cls, descr):
        assert "payload" in descr
        args = descr.get("args", None)
        return BaseSignature.final_parse(RegexSignature(descr['payload'], args), descr)


class MatchSignature(BaseSignature):

    def __init__(self, probe_match, onmatch, onfail ):
        self.type = "match"
        self.probe_match = re.compile(probe_match)
        self.onmatch = parse_signature(onmatch)
        self.onfail = parse_signature(onfail)
        self.match = None
        super(MatchSignature, self).__init__()


    def matches(self, payload):
        self.match = self.probe_match.findall(payload)
        if self.match:
            return True
        return False

    def compile(self):
        if self.match:
            if isinstance(self.onmatch, RegexSignature):
                return self.onmatch.compile(self.match)
            else:
                return self.onmatch.compile()
        else:
            return self.onfail.compile()

    @classmethod
    def parse(cls, descr):
        assert "regex" in descr
        assert "onmatch" in descr
        return BaseSignature.final_parse(MatchSignature( descr.get("regex"), descr.get("onmatch"),
                                                         descr.get("onfail", None)), descr)

def parse_signature(payload_dict):
    ptype = payload_dict['type']
    if ptype == "simple":
        return SimpleSignature.parse(payload_dict)
    elif ptype == "regex":
        return RegexSignature.parse(payload_dict)
    elif ptype == "match":
        return MatchSignature.parse(payload_dict)
    else:
        raise ValueError("Invalid signature type specified: " + ptype)