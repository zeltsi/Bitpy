import hashlib
import time
import random
from dataTypes import *


class PacketCreator(): # Takes two arguments: a Header object and a Payload object
    def __init__(self, payload, header):
        self.payload = payload.forge()
        self.header = header.forge()

    def forge(self):
        return self.header +  self.payload


class Header(): # Takes two arguments, the payload of the message and the message command
    def __init__(self, payload, command):
        self.payload = payload.forge()  # The message payload
        self.magic = to_hexa("F9BEB4D9")  # The Magic number of the Main network -> This message will be accepted by the main network
        self.command = self.command_padding(command)
        self.checksum = self.checksum()
        self.length = to_uint32(len(self.payload))

    def command_padding(self, command):  # The message command should be padded to be 12 bytes long.
        command = command + (12 - len(command)) * "\00"
        return command

    def checksum(self):
        check = hashlib.sha256(hashlib.sha256(self.payload).digest()).digest()[:4]
        return check

    def forge(self):
        return self.magic + self.command + self.length + self.checksum + self.payload



class Payload():
    def __init__(self):
        self.version = to_int32(70002)
        self.services = to_uint64(0)
        self.timestamp = to_int64(time.time())

        self.addr_recv_services = to_uint64(0) #services
        self.addr_recv_ip = to_big_endian_16char("127.0.0.1")
        self.addr_recv_port = to_big_endian_uint16(8333)

        self.addr_trans_services = to_uint64(0) #services
        self.addr_trans_ip = to_big_endian_16char("127.0.0.1")
        self.addr_trans_port = to_big_endian_uint16(8333)

        self.nonce = to_uint64(random.getrandbits(64))
        self.user_agent_bytes = to_uchar(0)
        self.starting_height = to_int32(395292)
        self.relay = to_bool(False)

    def forge(self):
        return self.version + self.services + self.timestamp + \
               self.addr_recv_services + self.addr_recv_ip + self.addr_recv_port + \
               self.addr_trans_services + self.addr_trans_ip + self.addr_trans_port + \
               self.nonce + self.user_agent_bytes + self.starting_height + \
               self.relay

if "__main__"  == __name__:
    payload = Payload()
    header = Header(payload, "version")

    packet = PacketCreator(header,payload)

    print packet.forge()










# magic = "F9BEB4D9".decode("hex")
# command = "version" + 5 * "\00"
# length = struct.pack("I", len(payload))
