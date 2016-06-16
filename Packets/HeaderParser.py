__author__ = 'alexisgallepe'

from Utils.dataTypes import *


class HeaderParser:
    def __init__(self, block): # Packets is a stream

        self.magic = read_hexa( block.read(4) )
        self.command = block.read(12)
        self.payload_size = read_uint32( block.read(4) )
        self.checksum =  block.read(4)

        self.header_size = 4+12+4+4

    def to_string(self):
        display = "\n-------------HEADER-------------"
        display += "\nMagic:\t %s" % self.magic
        display += "\nCommand name	:\t %s" % self.command
        display += "\nPayload size	:\t %s" % self.payload_size
        display += "\nChecksum	:\t\t %s" % hash_to_string(self.checksum)
        display += "\nheader Size:\t\t %s" % self.header_size
        display += "\n"
        return display