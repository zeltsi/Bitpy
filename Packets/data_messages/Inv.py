from Utils.dataTypes import *
from Utils.globals import *


class EncodeInv:
    def __init__(self, inventories):
        self.command_name = "inv"

        length_inventories = len(inventories)
        assert length_inventories > 0

        self.number_inventories = to_compactSize_uint(length_inventories)
        self.inventories = self.encode_inventories(inventories)

    def forge(self):
        return self.number_inventories + self.inventories

    def encode_inventories(self, inventories):
        encodeInventories = b""

        for inv in inventories:
            encodeInventories += to_uint32(inv["type"])
            encodeInventories += to_chars(inv["hash"])

        return encodeInventories


class DecodeInv:
    def __init__(self, payload):
        self.count = read_compactSize_uint(payload)
        self.inventories = self.get_inventories(payload)

    def get_inventories(self,payload):
        inventories = []

        for _ in range(self.count):
            type = read_uint32(payload.read(4))
            assert 1 <= type <=3

            inv = {
                "type": type_id[type], #type_id defined in Utils.config
                "hash": read_hexa(payload.read(32))
            }
            inventories.append(inv)

        return inventories


    def get_decoded_info(self):
        display = "\n-----Inv-----"
        display += "\nCount:\t\t %s \n" % self.count
        display += "\nInventories	:\n"

        for inv in self.inventories:
            display += str(inv) + "\n"

        return display
