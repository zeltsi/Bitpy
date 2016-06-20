import random
from Utils.dataTypes import *


class EncodePing:
    def __init__(self):
        self.command_name = "ping"
        self.nonce = to_uint64(random.getrandbits(64))

    def forge(self):
        return self.nonce


class DecodePing:
    def __init__(self, payload):
        self.nonce = payload.read(8)
