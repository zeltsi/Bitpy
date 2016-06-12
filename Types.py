import struct

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

def to_hexa(v):
    return v.decode("hex")

def to_uchar(v):
    return struct.pack("B", v)

def to_bool(v):
    return struct.pack("?", v)

