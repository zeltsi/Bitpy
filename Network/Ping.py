import time
import random

from Utils.dataTypes import *


class Ping():
    def __init__(self):
        self.nonce = to_uint64(random.getrandbits(64))

    def forge(self):
        return self.nonce