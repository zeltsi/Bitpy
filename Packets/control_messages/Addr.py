from Utils.dataTypes import *


class EncodeAddr:
    def __init__(self,nodes):
        self.command_name = "addr"

        length_nodes = len(nodes)
        assert length_nodes > 0
        
        self.number_nodes = to_compactSize_uint(length_nodes)
        self.nodes = self.encode_nodes(nodes)

    def forge(self):
        return self.number_nodes + self.nodes

    def encode_nodes(self,nodes):
        encoded_nodes = b""

        for node in nodes:
            encoded_nodes += to_uint32(node["time"])
            encoded_nodes += to_uint64(node["services"])
            encoded_nodes += to_big_endian_16char(node["ip_address"])
            encoded_nodes += to_big_endian_uint16(node["port"])

        return encoded_nodes



class DecodeAddr:
    def __init__(self, addr_received):

        self.number_nodes = read_compactSize_uint(addr_received)
        self.nodes = self.decode_nodes(addr_received)

    def decode_nodes(self, payload):
        nodes = []

        for _ in range(self.number_nodes):
            node = {
                "time": read_uint32(payload.read(4)),
                "services": read_uint64(payload.read(8)),
                "ip_address": parse_ip(payload.read(16)),
                "port": read_big_endian_uint16(payload.read(2)),
            }
            nodes.append(node)

        return nodes

    def get_decoded_info(self):
        display = "\n-----Addr-----"
        display += "\nNumber IP address                :\t\t %s \n" % self.number_nodes
        display += "\nNodes	:\n"

        for node in self.nodes:
            display += str(node) + "\n"

        return display
