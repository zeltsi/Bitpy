from Utils.dataTypes import *

class EncodeInv():
    def __init__(self):
        self.command_name = "inv"


    def forge(self):
        return self.nonce


class DecodeInv():
    def __init__(self,payload):
        self.size = read_compactSize_uint(payload)

