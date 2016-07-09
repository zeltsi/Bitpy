import os
import ecdsa
import hashlib
import base58
import binascii
import codecs

class key():
    def __init__(self, private_key=0):
        if private_key == 0:
            self.private_key = os.urandom(32)
        else:
            self.private_key = binascii.unhexlify(private_key.encode('ascii'))

        self.sk = ecdsa.SigningKey.from_string(self.private_key, curve = ecdsa.SECP256k1)
        self.vk = self.sk.verifying_key
        self.x = b"04" + binascii.hexlify(self.vk.to_string())
        self.public_key = self.x
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(hashlib.sha256(binascii.unhexlify(self.public_key)).digest())
        self.hashed_public_key =b"00" + binascii.hexlify(ripemd160.digest())
        self.checksum = binascii.hexlify(hashlib.sha256(hashlib.sha256(binascii.unhexlify(self.hashed_public_key)).digest()).digest()[:4])
        self.binary_addr = binascii.unhexlify(self.hashed_public_key + self.checksum)
        self.addr = base58.b58encode(self.binary_addr)

nk = key("73356839c2883cdf723b44f329928d5acd51e0b3b9d88ea3e1639e34e1dc6958")
print (type(nk.private_key))
print ((binascii.hexlify(nk.private_key).decode("ascii")))
print (nk.x)
print(nk.hashed_public_key)
print(nk.checksum)
print(nk.binary_addr)
print(nk.addr)