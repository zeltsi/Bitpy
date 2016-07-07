import os
import Utils.globals
from Manager import core_manager

class CLI:
    def __init__(self):
        self.sendingQueue = Utils.globals.sendingQueue

        cmd = -1
        while not cmd == 0:
            print("Enter your command number:")
            print("0: Exit")
            print("1: Version")
            print("2: verack")
            print("3: getAddr")
            print("4: Ping")
            print("5: GetBlocks (block hash already defined)")

            cmd = int(input(">"))
            self.order(cmd)

        os._exit(0)

    def order(self, cmd):
        if cmd == 1:
            packet = core_manager.get_version_pkt()

        elif cmd == 2:
            packet = core_manager.get_verack_pkt()

        elif cmd == 3:
            packet = core_manager.get_getAddr_pkt()

        elif cmd == 4:
            packet = core_manager.get_ping_pkt()

        elif cmd == 5:
            print("Enter your block Hash(es): (you can write as many blocks as you want, separated by a coma)")
            print("i.e: 5c3e6403d40837110a2e8afb602b1c01714bda7ce23bea0a0000000000000000,951b7b286867a7e074865cd08a1ed99783bdfb189c90e6400000000000000000")
            hashes = input(">")
            hashes = [ hash.strip() for hash in hashes.split(',') ]
            packet = core_manager.get_getBlocks_pkt(hashes)

        else:
            return

        self.sendingQueue.put(packet)