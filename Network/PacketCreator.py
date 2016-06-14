import hashlib
import time
import random
from dataTypes import *
import Header
import Version


class PacketCreator(): # Takes two arguments: a Header object and a Payload object
    def __init__(self, payload, header):
        self.payload = payload.forge()
        self.header = header.forge()

    def forge(self):
        return self.header +  self.payload



if "__main__"  == __name__:
    payload = Version.Version()
    header = Header.Header(payload, "version")

    packet = PacketCreator(header,payload)

    print packet.forge()




# magic = "F9BEB4D9".decode("hex")
# command = "version" + 5 * "\00"
# length = struct.pack("I", len(payload))
