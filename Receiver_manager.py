__author__ = 'alexisgallepe'

import sys
import Block
from threading import Thread

class Receiver_manager(Thread):

    def __init__(self,sock):
        Thread.__init__(self)
        self.sock = sock

    def run(self):
        while True:
            try:
                msg = self.sock.recv(1024)

                if len(msg) <= 0:
                    raise Exception("Node disconnected (received 0bit length message)")

                print "Message received from node: ", msg
                header = Block.BlockHeader(msg)
                print header.toString()

            except Exception as e:
                print e
                break

        print "Exit receiver Thread"