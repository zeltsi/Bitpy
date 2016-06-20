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

                # get only the header of the message
                header = self.sock.recv(24)

                if len(header) <= 0:
                    raise Exception("Node disconnected (received 0bit length message)")

                headerStream = BytesIO(header)
                headerParsed = HeaderParser(headerStream)

                # get the payload
                payload = self.recvall(headerParsed.payload_size)
                payloadStream = BytesIO(payload)

                self.manager(headerParsed, payloadStream)

            except Exception as e:
                print e
                break

        print "Exit receiver Thread"

    def manager(self, headerParsed, payloadStream):

        self.log(headerParsed.to_string())

        if headerParsed.command.startswith('ping'):
            ping = Ping.DecodePing(payloadStream)

            pong = Pong.EncodePong(ping.nonce)
            packet = PacketCreator(pong)

            self.senderQueue.put(packet.forge_packet())

        elif headerParsed.command.startswith('inv'):
            inv = Inv.DecodeInv(payloadStream)
            self.log("size:: " + str(inv.size))

        elif headerParsed.command.startswith('addr'):
            addr = Addr.DecodeAddr(payloadStream)
            self.log(addr.get_decoded_info())

        elif headerParsed.command.startswith('pong'):
            pong = Pong.DecodedPong(payloadStream)
            self.log(pong.get_decoded_info())

        elif headerParsed.command.startswith('version'):
            version = Version.DecodedVersion(payloadStream)
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
