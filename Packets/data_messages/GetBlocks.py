from Utils.config import version_number
from Utils.dataTypes import *


class EncodeGetblocks:
    def __init__(self, hashes):
        self.command_name = "getblocks"

        length_hashes = len(hashes)
        assert 0 < length_hashes <= 200

        hashes = sorted(hashes, reverse=True)

        self.version = to_uint32(version_number)
        self.hash_count = to_compactSize_uint(length_hashes)
        self.hashes = ''.join(to_32char(e) for e in hashes)
        self.stop_hash = to_32char("0" * 32)

    def forge(self):
        return self.version + self.hash_count + self.hashes + self.stop_hash


class DecodeGetblocks:
    def __init__(self, getblocks_received):
        pass

    def get_decoded_info(self):
        display = "\n-----GetBlocks-----"

        # TODO

        return display
