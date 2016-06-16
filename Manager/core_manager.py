__author__ = 'alexisgallepe'

from Packets.PacketCreator import *
from Packets.control_messages import *
from Packets.data_messages import *


class Manager:

    def __init__(self,senderQueue):
        self.senderQueue = senderQueue
        self.get_order_client()


    def get_order_client(self):
        while True:
            print "enter order"
            print "0: Version"
            print "1: verack"
            print "2: ping"

            cmd = int(input(">"))
            self.order(cmd)


    def order(self,cmd):
        if cmd == 0:
            version =  Version.EncodeVersion()
            packet = PacketCreator(version)

            self.senderQueue.put( packet.forge_packet() )

        elif cmd == 1:
            verack = Verack.EncodeVerack()
            packet = PacketCreator(verack)

            self.senderQueue.put( packet.forge_packet() )

        elif cmd == 2:
            ping = Ping.EncodePing()
            packet = PacketCreator(ping)

            self.senderQueue.put( packet.forge_packet() )

