import struct

# 16
def to_big_endian_16char(v):
    return struct.pack(">16s", v)

def to_big_endian_uint16(v):
    return struct.pack(">H", v)


def read_int16(v):
    return struct.unpack("h", v)[0]

def read_uint16(v):
    return struct.unpack("H", v)[0]

def read_big_endian_uint16(v):
    return struct.unpack(">H", v)[0]

def read_big_endian_16char(v):
    return struct.unpack(">16s", v)[0]



# 32
def to_int32(v):
    return struct.pack("i", v)

def to_uint32(v):
    return struct.pack("I", v)


def read_int32(v):
    return struct.unpack("i", v)[0]

def read_uint32(v):
    return struct.unpack("I", v)[0]


# 64
def to_int64(v):
    return struct.pack("q", v)

def to_uint64(v):
    return struct.pack("Q", v)


def read_int64(v):
    return struct.unpack("q", v)[0]

def read_uint64(v):
    return struct.unpack("Q", v)[0]


# _uchar
def to_uchar(v):
    return struct.pack("B", v)

def read_uchar(v):
    return struct.unpack("B", v)[0]


# _chars
def to_chars(v, length=-1):
    if length == -1:
        length = len(v)

    return struct.pack(">%ss" % length, v)

def read_chars(v, length= -1):
    if length == -1:
        length = len(v)

    return struct.unpack(">%ss" % length, v)[0]


# _hexa
def to_hexa(v):
    return bytes.fromhex(v)

def read_hexa(v):
    return v.hex()


# _bool
def to_bool(v):
    return struct.pack("?", v)

def read_bool(v):
    return struct.unpack("?", v)[0]

# _compactSize_uint
def to_compactSize_uint(v):  # New type which is required by the bitcoin protocol
    if 0xfd > v:
        return struct.pack("<B", v)
    elif 0xffff > v:
        return to_hexa("FD") + struct.pack("<H", v)
    elif 0xffffffff > v:
        return to_hexa("FE") + struct.pack("<I", v)
    else:
        return to_hexa("FF") + struct.pack("<Q", v)

def read_compactSize_uint(s):  # S is a stream of the payload
    # Read an unsigned char to get the format
    size = ord(s.read(1))

    if size < 0xFD:
        return size
    if size == 0xFD:
        return read_uint16(s.read(2))
    if size == 0xFE:
        return read_uint32(s.read(4))
    if size == 0xFF:
        return read_uint64(s.read(8))


# IP
def parse_ip(ip):
    IPV4_COMPAT = b"\x00" * 10 + b"\xff" * 2

    # IPv4
    if ip[0:12] == IPV4_COMPAT:
        ip = read_hexa(ip[12:])# we remove the first 10 "\x00" an 2 "\xff , and convert bytes to hexa
        ip = "%i.%i.%i.%i" % (int(ip[0:2], 16), int(ip[2:4], 16), int(ip[4:6], 16), int(ip[6:8], 16))

    # IPv6
    else:
        # TODO
        pass

    return ip
