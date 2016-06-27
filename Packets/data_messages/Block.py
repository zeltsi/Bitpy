import random
import time

from Utils.config import version_number, latest_known_block
from Utils.dataTypes import *


class EncodeBlock:
    def __init__(self):
        self.command_name = "block"



    def forge(self):
        # TODO
        return ""


class DecodedBlock:
    def __init__(self, payload):

        # Block header
        self.version = read_uint32(payload.read(4))
        self.previous_block_header_hash = read_32char(payload.read(32))
        self.merkle_root_hash = read_32char(payload.read(32))
        self.time = read_uint32(payload.read(4))
        self.bits = read_uint32(payload.read(4))
        self.nounce = read_uint32(payload.read(4))

        # Transactions
        self.txn_count = read_compactSize_uint(payload)
        self.txns = self.get_transactions(payload)


    def get_transactions(self, payload):
        transactions = []

        for _ in range(self.txn_count):

            version = read_uint32(payload.read(4))

            tx_in_count = read_compactSize_uint(payload)
            tx_in = self.get_txIn(payload,tx_in_count)

            tx_out_count = read_compactSize_uint(payload)
            tx_out = self.get_txOut(payload,tx_out_count)

            lock_time = read_uint32(payload.read(4))

            tx = {
                "version": version,
                "tx_in_count": tx_in_count,
                "tx_in": tx_in,
                "tx_out_count": tx_out_count,
                "tx_out": tx_out,
                "lock_time": lock_time,
            }

            transactions.append(tx)

        return transactions



    def get_txIn(self,payload,tx_in_count):
        tx_in = []

        for _ in range(tx_in_count):

            # previous_output
            hash = read_32char(payload.read(32))
            index = read_uint32(payload.read(4))

            script_bytes = read_compactSize_uint(payload)
            signature_script = read_char(payload,script_bytes)

            sequence = read_uint32(payload.read(4))

            tx_in.append({
                "hash":hash,
                "index":index,
                "script_bytes": script_bytes,
                "signature_script": signature_script,
                "sequence": sequence,
            })

        return tx_in


    def get_txOut(self,payload,tx_out_count):
        tx_out = []

        for _ in range(tx_out_count):

            value = read_uint64(payload.read(8))
            pub_key_script_bytes = read_compactSize_uint(payload)
            pk_script = read_char(payload, pub_key_script_bytes)

            tx_out.append({
                "value": value,
                "pub_key_script_bytes": pub_key_script_bytes,
                "pk_script": pk_script,
            })

        return tx_out


    def get_decoded_info(self):
        display = "\n-----Block-----"
        display += "\nversion                :\t\t %s" % self.version
        display += "\nprevious_block_header_hash  	         :\t\t %s" % self.previous_block_header_hash
        display += "\nmerkle_root_hash              :\t\t %s" % self.merkle_root_hash

        display += "\ntime	 :\t\t %s" % self.time
        display += "\nbits           :\t\t %s" % self.bits
        display += "\nnounce         :\t\t %s" % self.nounce
        display += "\ntxn_count         :\t\t %s" % self.txn_count

        display += "\nTransactions: -----\n"

        for tx in self.txns:
            display += str(tx) + "\n"

        return display
