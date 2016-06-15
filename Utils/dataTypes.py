import struct

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

def to_hexa(v):
    return v.decode("hex")

def to_uchar(v):
    return struct.pack("B", v)

def to_bool(v):
    return struct.pack("?", v)

def to_compactSize_uint(v):  	#New type which is required by the bitcoin protocol
    if 0xfd > v:
        return struct.pack("<B", v)
    elif 0xffff > v:
        return "FD".decode("hex") + struct.pack("<H", v)
    elif 0xffffffff > v:
        return "FE".decode("hex") + struct.pack("<I", v)
    else:
        return "FF".decode("hex") + struct.pack("<Q", v)



###### DECODE ######

def from_int32(v):
    return struct.unpack("i", v)

def from_uint32(v):
    return struct.unpack("I", v)

def from_int64(v):
    return struct.unpack("q", v)

def from_uint64(v):
    return struct.unpack("Q", v)

def from_big_endian_16char(v):
    return struct.unpack(">16s", v)

def from_big_endian_uint16(v):
    return struct.unpack(">H", v)

def from_hexa(v):
    return v.encode("hex")

def from_uchar(v):
    return struct.unpack("B", v)

def from_bool(v):
    return struct.unpack("?", v)

def hash_to_string(bytebuffer):
    return ''.join(('%02x' % ord(a)) for a in bytebuffer)



