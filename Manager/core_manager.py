import os
from Packets.PacketCreator import *
from Packets.control_messages import *
from Packets.data_messages import *

__author__ = 'alexisgallepe'


class Manager:
    def __init__(self, senderQueue):
        self.senderQueue = senderQueue
        self.get_order_client()

    def get_order_client(self):

        # send first Version + verack
        self.order(0)
        self.order(1)

        print "Version & VerAck sent, connected to node."

        while True:
            print "Enter your command number:"
            print "11: Exit"
            print "(0: Version)"
            print "(1: verack)"
            print "2: getAddr"
            print "3: Ping"
            print "4: GetBlocks (block hash already defined)"

            cmd = int(input(">"))
            self.order(cmd)

    def order(self, cmd):
        packet = ""

        if cmd == 11:
            os._exit(0)

        elif cmd == 0:
            version = Version.EncodeVersion()
            packet = PacketCreator(version).forge_packet()

        elif cmd == 1:
            verack = Verack.EncodeVerack()
            packet = PacketCreator(verack).forge_packet()

        elif cmd == 2:
            getAddr = GetAddr.EncodeGetaddr()
            packet = PacketCreator(getAddr).forge_packet()

        elif cmd == 3:
            ping = Ping.EncodePing()
            packet = PacketCreator(ping).forge_packet()

        elif cmd == 4:
            getBlocks = GetBlocks.EncodeGetblocks(["0000000000000000046e09c981bfdb38799de1a80dc568470e7a768682b7b159"])
            packet = PacketCreator(getBlocks).forge_packet()

        self.senderQueue.put(packet)
