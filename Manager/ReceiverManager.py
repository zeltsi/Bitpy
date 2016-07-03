__author__ = 'alexisgallepe'

from Packets.HeaderParser import HeaderParser
from Packets.PacketCreator import *
from Packets.control_messages import *
from Packets.data_messages import *

from io import BytesIO
from threading import Thread

class ReceiverManager(Thread):
    def __init__(self, sock, senderQueue):
        Thread.__init__(self)
        self.senderQueue = senderQueue
        self.sock = sock
        self.ping = ""

        self.outfile = open("data_received_from_node.txt", 'w')

    def run(self):
        while True:
            try:

                # get only the header's message
                header = self.sock.recv(24)

                if len(header) <= 0:
                    raise Exception("Node disconnected (received 0bit length message)")

                headerStream = BytesIO(header)
                parsedHeader = HeaderParser(headerStream)

                # get the payload
                payload = self.recvall(parsedHeader.payload_size)
                payloadStream = BytesIO(payload)

                self.manager(parsedHeader, payloadStream)

            except Exception as e:
                print e
                break

        print "Exit receiver Thread"

    def manager(self, parsedHeader, payloadStream):

        self.log(parsedHeader.to_string())

        if parsedHeader.command.startswith('ping'):
            ping = Ping.DecodePing(payloadStream)

            pong = Pong.EncodePong(ping.nonce)
            packet = PacketCreator(pong)

            self.senderQueue.put(packet.forge_packet())

        elif parsedHeader.command.startswith('inv'):
            inv = Inv.DecodeInv(payloadStream)
            self.log(inv.get_decoded_info())

        elif parsedHeader.command.startswith('addr'):
            addr = Addr.DecodeAddr(payloadStream)
            self.log(addr.get_decoded_info())

        elif parsedHeader.command.startswith('pong'):
            pong = Pong.DecodePong(payloadStream)
            self.log(pong.get_decoded_info())

        elif parsedHeader.command.startswith('version'):
            version = Version.DecodeVersion(payloadStream)
            self.log(version.get_decoded_info())

    def recvall(self, length):
        blocks = []

        while length > 0:
            block = self.sock.recv(length)
            if not block:
                raise EOFError('socket closed with %d bytes left in this block'.format(length))

            length -= len(block)
            blocks.append(block)

        return b''.join(blocks)

    def log(self, messages):
        self.outfile.write(messages)
        self.outfile.flush()
