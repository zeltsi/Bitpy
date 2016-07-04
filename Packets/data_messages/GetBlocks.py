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
        self.hashes = b''.join(to_chars(to_hexa(e)) for e in hashes)
        self.stop_hash = to_chars(to_hexa("00" * 32))

    def forge(self):
        return self.version + self.hash_count + self.hashes + self.stop_hash


class DecodeGetblocks:
    def __init__(self, payload):
        self.version = read_uint32(payload.read(4))
        self.hash_count = read_compactSize_uint(payload)
        self.hashes = self.parse_hashes(payload)

    def parse_hashes(self,payload):
        hashes = []

        for _ in range(self.hash_count):
            hashes.append(read_chars(payload.read(32)))

        return hashes

    def get_decoded_info(self):
        display = "\n-----GetBlocks-----"
        display += "\nVersion:\t %s" % self.version
        display += "\nHash count	:\t %s" % self.hash_count
        display += "\nHashes	:\n"

        for hash in self.hashes:
            display += str(hash) + "\n"

        return display
