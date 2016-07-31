import os
import ecdsa
import hashlib
import base58
import binascii


class Key(object):

    def __init__(self, private_key=0):
        if private_key == 0:
            self.private_key = os.urandom(32)
            self.printable_pk = str(binascii.hexlify(self.private_key), "ascii")
        else:
            self.printable_pk = private_key
            self.private_key = binascii.unhexlify(private_key.encode('ascii'))


        self.sk = ecdsa.SigningKey.from_string(self.private_key, curve = ecdsa.SECP256k1)
        self.vk = self.sk.verifying_key
        self.public_key =  b"04" + binascii.hexlify(self.vk.to_string())
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(hashlib.sha256(binascii.unhexlify(self.public_key)).digest())
        self.hashed_public_key = b"00" + binascii.hexlify(ripemd160.digest())
        self.checksum = binascii.hexlify(hashlib.sha256(hashlib.sha256(binascii.unhexlify(self.hashed_public_key)).digest()).digest()[:4])
        self.binary_addr = binascii.unhexlify(self.hashed_public_key + self.checksum)
        self.addr = base58.b58encode(self.binary_addr)

    def get_addr(self):
        return self.addr


def get_private_key(private_key):
    return private_key

def generate_new_private_key():
    return os.urandom(32)

def generate_sk(private_key):
    return ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)

def generate_vk(sk):
    return sk.verifying_key

def generate_public_key(vk):
    return b"04" + binascii.hexlify(vk.to_string())

def generate_hashed_public_key(public_key):
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashlib.sha256(binascii.unhexlify(public_key)).digest())
    return ripemd160.digest()


def generate_hashed_public_key_string(public_key):
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashlib.sha256(binascii.unhexlify(public_key)).digest())
    return binascii.hexlify(ripemd160.digest()).decode('ascii')
    #return ripemd160.digest()


def generate_checksum(hashed_public_key):
    return binascii.hexlify(hashlib.sha256(hashlib.sha256(binascii.unhexlify(hashed_public_key)).digest()).digest()[:4])

def generate_address(private_key):
    sk = generate_sk(binascii.unhexlify(private_key.encode('ascii')))
    vk = generate_vk(sk)
    public_key = generate_public_key(vk)
    hashed_public_key = generate_hashed_public_key(public_key)
    checksum = generate_checksum(hashed_public_key)
    binary_address = binascii.unhexlify(hashed_public_key + checksum)
    addr = base58.b58encode(binary_address)
    return addr

