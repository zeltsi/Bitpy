import struct
import socket
import platform


####### ENCODE #######
def to_int32(v):
    return struct.pack("i", v)


def to_uint32(v):
    return struct.pack("I", v)


def to_int64(v):
    return struct.pack("q", v)


def to_uint64(v):
    return struct.pack("Q", v)


def to_big_endian_16char(v):
    return struct.pack(">16s", v)


def to_big_endian_uint16(v):
    return struct.pack(">H", v)


def to_32char(v):
    return struct.pack(">32s", v)


def to_hexa(v):
    return v.decode("hex")


def to_uchar(v):
    return struct.pack("B", v)


def to_bool(v):
    return struct.pack("?", v)


def to_compactSize_uint(v):  # New type which is required by the bitcoin protocol
    if 0xfd > v:
        return struct.pack("<B", v)
    elif 0xffff > v:
        return "FD".decode("hex") + struct.pack("<H", v)
    elif 0xffffffff > v:
        return "FE".decode("hex") + struct.pack("<I", v)
    else:
        return "FF".decode("hex") + struct.pack("<Q", v)


###### DECODE ######

def read_int16(v):
    return struct.unpack("h", v)[0]


def read_uint16(v):
    return struct.unpack("H", v)[0]


def read_big_endian_16char(v):
    return struct.unpack(">16s", v)[0]


def read_big_endian_uint16(v):
    return struct.unpack(">H", v)[0]


def read_int32(v):
    return struct.unpack("i", v)[0]


def read_uint32(v):
    return struct.unpack("I", v)[0]


def read_int64(v):
    return struct.unpack("q", v)[0]


def read_uint64(v):
    return struct.unpack("Q", v)[0]


def read_32char(v):
    return struct.unpack("32s", v)

def read_hexa(v):
    return v.encode("hex")


def read_uchar(v):
    return struct.unpack("B", v)[0]


def read_bool(v):
    return struct.unpack("?", v)[0]


def hash_to_string(bytebuffer):
    return ''.join(('%02x' % ord(a)) for a in bytebuffer)


def read_compactSize_uint(s):  # S is a stream of the payload

    # Read an unsigned char to get the format
    size = ord(s.read(1))

    # Return the value
    if size < 0xFD:
        return size
    if size == 0xFD:
        return read_uint16(s.read(2))
    if size == 0xFE:
        return read_uint32(s.read(4))
    if size == 0xFF:
        return read_uint64(s.read(8))


def read_char(v, length):
    return struct.unpack(">%ss" % length, v)


def parse_ip(ip):
    IPV4_COMPAT = b"\x00" * 10 + b"\xff" * 2

    if platform.system() == "windows":
        return ip

    # IPv4
    if bytes(ip[0:12]) == IPV4_COMPAT:
        return socket.inet_ntop(socket.AF_INET, ip[12:16])

    # IPv6
    else:
        return socket.inet_ntop(socket.AF_INET6, ip)
