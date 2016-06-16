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

                header = HeaderParser(message)
                payload = message.read(header.header_size)

                self.manager(header,payload)

            except Exception as e:
                print e
                break

        print "Exit receiver Thread"


    def manager(self,header,payload):

        self.log(header.to_string())

        if header.command.startswith( 'ping' ):

            ping = Ping.DecodePing(payload)
            pong = Pong.EncodePong(ping.nounce)
            packet = PacketCreator(pong)

            self.senderQueue.put( packet.forge_packet() )





    def log(self,messages):
        self.outfile.write(messages)
        self.outfile.flush()