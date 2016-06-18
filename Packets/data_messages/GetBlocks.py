from Utils.config import version_number, latest_known_block
from Utils.dataTypes import *

class EncodeGetblocks():
    def __init__(self,hashes):
        self.command_name = "getblocks"

        self.version = to_int32(version_number) #ou alors: to_uint32
        self.hash_count = len(hashes)

        assert self.hash_count > 0 and self.hash_count <= 200

        self.hashes = hashes.sort(reverse=True)
        self.stop_hash = "0" * 32


    def forge(self):
        return self.version + str(self.hash_count) + b''.join(self.hashes)



class DecodeGetblocks():
    def __init__(self,getblocks_received):
        pass


    def get_decoded_info(self):
        display = "\n-----GetBlocks-----"

        #TODO

        return display
