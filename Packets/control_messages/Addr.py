from Utils.config import version_number, latest_known_block
from Utils.dataTypes import *

class EncodeAddr():
    def __init__(self):
        self.command_name = "addr"


    def forge(self):
        #TODO
        pass



class DecodeAddr():
    def __init__(self,addr_received):

        self.number_nodes = read_compactSize_uint( addr_received )
        self.nodes = self.decode_nodes(addr_received)



    def decode_nodes(self,payload):
        nodes = []

        for _ in range(self.number_nodes):
            node = {
                    "time": read_uint32( payload.read(4) ),
                    "services": read_uint64( payload.read(8) ),
                    "ip_address": parse_ip( payload.read(16) ),
                    "port": read_big_endian_uint16( payload.read(2) ),
                }
            nodes.append(node)

        return nodes


    def get_decoded_info(self):
        display = "\n-----Addr-----"
        display += "\nNumber IP address                :\t\t %s \n" % self.number_nodes

        for node in self.nodes:
            display += str(node) + "\n"

        return display
