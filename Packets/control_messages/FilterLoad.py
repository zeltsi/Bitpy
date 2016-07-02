import random
from Utils.dataTypes import *
import math



class BloomFilter:
    def __init__(self, n, p):
        self.size = round((-1/(math.log(2)**2)*n*math.log(p))/8)
        self.hash_count = round((self.size*8)/n*math.log(2))

class EncodeFilterLoad:
    def __init__(self):
        self.command_name = "EncodeFilterLoad"
        self.nonce = to_uint64(random.getrandbits(64))

    def forge(self):
        return""


class DecodeFilterLoad:
    def __init__(self):
        pass


bf = BloomFilter(1000,0.1)
print bf.size
print bf.hash_count