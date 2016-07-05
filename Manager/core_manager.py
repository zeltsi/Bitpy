import os

from Packets.PacketCreator import *
from Packets.control_messages import *
from Packets.data_messages import *

__author__ = 'alexisgallepe'


def get_version_pkt():
    version = Version.EncodeVersion()
    return PacketCreator(version).forge_packet()

def get_verack_pkt():
    verack = Verack.EncodeVerack()
    return PacketCreator(verack).forge_packet()

def get_getAddr_pkt():
    getAddr = GetAddr.EncodeGetaddr()
    return PacketCreator(getAddr).forge_packet()

def get_ping_pkt():
    ping = Ping.EncodePing()
    return PacketCreator(ping).forge_packet()

def get_getBlocks_pkt(hashes=["5c3e6403d40837110a2e8afb602b1c01714bda7ce23bea0a0000000000000000"]):
    getBlocks = GetBlocks.EncodeGetblocks(hashes)
    return PacketCreator(getBlocks).forge_packet()


class Manager:
    def __init__(self, senderQueue):
        self.senderQueue = senderQueue

        print("-- BitPy --")
        print("Choose your UI:")
        print("0: CLI")
        print("1: Tkinter")
        print("2: pyQt 5 (pyQt5 library required)")

        ui = int(input(">"))

        if ui == 0:
            self.CLI_UI()

        elif ui == 1:
            from GUI.tkinter_GUI.tkinter_GUI import start_GUI
            start_GUI()

        elif ui == 2:
            from GUI.pyQt5_GUI.pyQt5_GUI import Ui_manager
            ui = Ui_manager()


    def CLI_UI(self):

        # send first Version + verack
        self.order(0)
        self.order(1)

        cmd = 0

        print("\nVersion & VerAck sent, connected to node.")

        while not cmd == 11:
            print("Enter your command number:")
            print("11: Exit")
            print("(0: Version)")
            print("(1: verack)")
            print("2: getAddr")
            print("3: Ping")
            print("4: GetBlocks (block hash already defined)")

            cmd = int(input(">"))
            self.order(cmd)

        os._exit(0)

    def order(self, cmd):

        if cmd == 0:
            packet = get_version_pkt()

        elif cmd == 1:
            packet = get_verack_pkt()

        elif cmd == 2:
            packet = get_getAddr_pkt()

        elif cmd == 3:
            packet = get_ping_pkt()

        elif cmd == 4:
            print("Enter your block Hash(es): (you can write as many blocks as you want, separated by a coma)")
            print("i.e: 5c3e6403d40837110a2e8afb602b1c01714bda7ce23bea0a0000000000000000,951b7b286867a7e074865cd08a1ed99783bdfb189c90e6400000000000000000")
            hashes = input(">")
            hashes = [ hash.strip() for hash in hashes.split(',') ]
            print(hashes)
            packet = get_getBlocks_pkt(hashes)

        else:
            return

        self.senderQueue.put(packet)
