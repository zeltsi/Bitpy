__author__ = 'alexisgallepe'

from Block.HeaderParser import HeaderParser
from Block.PacketCreator import *
from Block.control_messages import *
from Block.data_messages import *

from threading import Thread

class ReceiverManager(Thread):

    def __init__(self,sock,senderQueue):
        Thread.__init__(self)
        self.senderQueue = senderQueue
        self.sock = sock
        self.ping = ""

    def run(self):
        while True:
            try:
                msg = self.sock.recv(1024)

                if len(msg) <= 0:
                    raise Exception("Node disconnected (received 0bit length message)")

                header = HeaderParser(msg)
                header.to_string()

                self.manager(header,msg)

            except Exception as e:
                print e
                break

        print "Exit receiver Thread"


    def manager(self,header,msg):

        if header.command.startswith( 'ping' ):
            ping_nounce = msg[header.header_size:]

            pong = Pong.EncodePong(ping_nounce)
            packet = PacketCreator(pong)

            self.senderQueue.put( packet.forge_packet() )
            print 'pong sent'

