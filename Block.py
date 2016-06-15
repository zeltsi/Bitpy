__author__ = 'alexisgallepe'

from Utils.dataTypes import *

class BlockHeader:
    def __init__(self, block):

        start = 0
        end = 4
        self.magic = from_hexa( block[start:end] )

        start = end
        end += 12
        self.command = block[start:end]

        start = end
        end += 4
        self.payloadSize = from_uint32( block[start:end] )

        start = end
        end += 4
        self.checksum =  block[start:end]


    def toString(self):
        print "-------------------------------"
        print "Magic:\t %s" % self.magic
        print "Command name	:\t %s" % self.command
        print "Payload size	:\t %s" % self.payloadSize
        print "Checksum	:\t\t %s" % hash_to_string(self.checksum)
