__author__ = 'alexisgallepe'

from Packets.HeaderParser import HeaderParser
from Packets.PacketCreator import *
from Packets.control_messages import *
from Packets.data_messages import *

from io import BytesIO
from threading import Thread
import sys

class ReceiverManager(Thread):

    def __init__(self,sock,senderQueue):
        Thread.__init__(self)
        self.senderQueue = senderQueue
        self.sock = sock
        self.ping = ""

        self.outfile = open("data_received_from_node.txt", 'w')

    def run(self):
        while True:
            try:
                messageReceived = self.sock.recv(1024)

                if len(messageReceived) <= 0:
                    raise Exception("Node disconnected (received 0bit length message)")

                messageStream = BytesIO(messageReceived)
                headerParsed = HeaderParser(messageStream)

                self.manager(headerParsed,messageStream)

            except Exception as e:
                print e
                break

        print "Exit receiver Thread"


    def manager(self,headerParsed,payloadStream):

        self.log(headerParsed.to_string())

        if headerParsed.command.startswith( 'ping' ):
            ping = Ping.DecodePing(payloadStream)

            pong = Pong.EncodePong(ping.nonce)
            packet = PacketCreator(pong)

            self.senderQueue.put( packet.forge_packet() )

        elif headerParsed.command.startswith( 'inv' ):
            inv = Inv.DecodeInv(payloadStream)
            self.log( "size:: "+str(inv.size) )

        elif headerParsed.command.startswith( 'addr' ):
            addr = Addr.DecodeAddr(payloadStream)
            self.log(addr.get_decoded_info())

        elif headerParsed.command.startswith('pong'):
            pong = Pong.DecodedPong(payloadStream)
            self.log(pong.get_decoded_info())

        elif headerParsed.command.startswith('version'):
            version = Version.DecodedVersion(payloadStream)
            self.log(version.get_decoded_info())




    def log(self,messages):
        self.outfile.write(messages)
        self.outfile.flush()