import random
from Utils.dataTypes import *


class EncodePing:
    def __init__(self, nonce=0):
        self.command_name = "ping"
        if nonce == 0:
            self.nonce = to_uint64(random.getrandbits(64))
        else:
            self.nonce = to_uint64(nonce)

    def forge(self):
        return self.nonce

    def get_decoded_info(self):
        return "\npong   :\t\t %s" % self.nonce


class DecodePing:
    def __init__(self, payload):
        self.nonce = read_uint64(payload.read(8))
        self.command_name = "ping"

    def get_decoded_info(self):
        return "\nping   :\t\t %s" % self.nonce