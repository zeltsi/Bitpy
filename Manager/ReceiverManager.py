__author__ = 'alexisgallepe'

from Packets.HeaderParser import HeaderParser
from Packets.PacketCreator import *
from Packets.control_messages import *
from Packets.data_messages import *

from io import BytesIO
from threading import Thread

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

                message = BytesIO(messageReceived)

                headerParsed = HeaderParser(message)
                payloadStream = message.read(headerParsed.header_size)

                self.manager(headerParsed,payloadStream)

            except Exception as e:
                print e
                break

        print "Exit receiver Thread"


    def manager(self,headerParsed,payloadStream):

        self.log(headerParsed.to_string())

        if headerParsed.command.startswith( 'ping' ):
            ping = Ping.DecodePing(payloadStream)

            pong = Pong.EncodePong(ping.nounce)
            packet = PacketCreator(pong)

            self.senderQueue.put( packet.forge_packet() )





    def log(self,messages):
        self.outfile.write(messages)
        self.outfile.flush()