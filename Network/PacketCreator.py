import hashlib
import time
import random
from Utils.dataTypes import *
import Header
import Version

#not really useful

"""
class PacketCreator(): # Takes two arguments: a Header object and a Payload object
    def __init__(self, payload, header):
        self.payload = payload.forge()
        self.header = header.forge()

    def forge(self):
        return self.header +  self.payload
"""



# magic = "F9BEB4D9".decode("hex")
# command = "version" + 5 * "\00"
# length = struct.pack("I", len(payload))
