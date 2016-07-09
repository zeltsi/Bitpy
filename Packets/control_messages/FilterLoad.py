# import random
# from Utils.dataTypes import *
# import bitarray
# import mmh3
# import sys
#
# import math
# import struct
#
# LN2SQUARED = 0.4804530139182014246671025263266649717305529515945455
# LN2 = 0.6931471805599453094172321214581765680755001343602552
# nElements = 5
# nFPRate = 0.0001
#
#
# def filter_size_required(element_count, false_positive_probability):
#     # The size S of the filter in bytes is given by
#     # (-1 / pow(log(2), 2) * N * log(P)) / 8
#     # Of course you must ensure it does not go over the maximum size
#     # (36,000: selected as it represents a filter of 20,000 items with false
#     # positive rate of < 0.1% or 10,000 items and a false positive rate of < 0.0001%).
#     lfpp = math.log(false_positive_probability)
#     return min(36000, int(((-1 / pow(LOG_2, 2) * element_count * lfpp)+7) // 8))
#
#
# def hash_function_count_required(filter_size, element_count):
#     # The number of hash functions required is given by S * 8 / N * log(2).
#     return int(filter_size * 8 / element_count * LOG_2 + 0.5)
#
#
# class BloomFilter(object):
#     def __init__(self, nFPRate, nElements, tweak):
#         self.size = int(min((-1  / LN2SQUARED * nElements * math.log(nFPRate)/8), 36000))
#         self.HashFuncs = int(min(self.size * 8 / nElements * LN2, 50))
#         self.bytes_array = bytearray(self.size)
#         self.bit_count = 8 * self.size
#         self.tweak = tweak
#
#     def add(self, item_bytes):
#         for hash_index in range(self.HashFuncs):
#             seed = hash_index * 0xFBA4C795 + self.tweak
#             self.set_bit(murmur3(item_bytes, seed=seed) % self.bit_count)
#
#     def _index_for_bit(self, v):
#         v %= self.bit_count
#         byte_index, mask_index = divmod(v, 8)
#         mask = [1, 2, 4, 8, 16, 32, 64, 128][mask_index]
#         return byte_index, mask
#
#     def set_bit(self, v):
#         byte_index, mask = self._index_for_bit(v)
#         self.bytes_array[byte_index] |= mask
#
#     def check_bit(self, v):
#         byte_index, mask = self._index_for_bit(v)
#         return (self.bytes_array[byte_index] & mask) == mask
#
#     def filter_load_params(self):
#         return self.bytes_array, self.HashFuncs, self.tweak
#
#
# # http://stackoverflow.com/questions/13305290/is-there-a-pure-python-implementation-of-murmurhash
#
# def murmur3(data, seed=0):
#     c1 = 0xcc9e2d51
#     c2 = 0x1b873593
#
#     length = len(data)
#     h1 = seed
#     roundedEnd = (length & 0xfffffffc)  # round down to 4 byte block
#     for i in range(0, roundedEnd, 4):
#         # little endian load order
#         k1 = (data[i] & 0xff) | ((data[i + 1] & 0xff) << 8) | \
#             ((data[i + 2] & 0xff) << 16) | (data[i + 3] << 24)
#         k1 *= c1
#         k1 = (k1 << 15) | ((k1 & 0xffffffff) >> 17)  # ROTL32(k1,15)
#         k1 *= c2
#
#         h1 ^= k1
#         h1 = (h1 << 13) | ((h1 & 0xffffffff) >> 19)  # ROTL32(h1,13)
#         h1 = h1 * 5 + 0xe6546b64
#
#     # tail
#     k1 = 0
#
#     val = length & 0x03
#     if val == 3:
#         k1 = (data[roundedEnd + 2] & 0xff) << 16
#     # fallthrough
#     if val in [2, 3]:
#         k1 |= (data[roundedEnd + 1] & 0xff) << 8
#     # fallthrough
#     if val in [1, 2, 3]:
#         k1 |= data[roundedEnd] & 0xff
#         k1 *= c1
#         k1 = (k1 << 15) | ((k1 & 0xffffffff) >> 17)  # ROTL32(k1,15)
#         k1 *= c2
#         h1 ^= k1
#
#     # finalization
#     h1 ^= length
#
#     # fmix(h1)
#     h1 ^= ((h1 & 0xffffffff) >> 16)
#     h1 *= 0x85ebca6b
#     h1 ^= ((h1 & 0xffffffff) >> 13)
#     h1 *= 0xc2b2ae35
#     h1 ^= ((h1 & 0xffffffff) >> 16)
#
#     return h1 & 0xffffffff
#
# bf = BloomFilter(0.01, 6, 6666)
# bf.add()
#
# class DecodeFilterLoad:
#     def __init__(self):
#         pass