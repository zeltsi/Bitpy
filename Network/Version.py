import random
import time
from Utils.config import version_number, latest_known_block
from Utils.dataTypes import *
import PacketCreator

class Version():
    def __init__(self):
        self.version = to_int32(version_number)
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
        self.starting_height = to_int32(latest_known_block)
        self.relay = to_bool(False)

    def forgePayload(self):
        return self.version + self.services + self.timestamp + \
               self.addr_recv_services + self.addr_recv_ip + self.addr_recv_port + \
               self.addr_trans_services + self.addr_trans_ip + self.addr_trans_port + \
               self.nonce + self.user_agent_bytes + self.starting_height + \
               self.relay

verssion_msg = PacketCreator.packet(Version().forgePayload(), "version")
print verssion_msg.forge_packet().encode("hex")