__author__ = 'alexisgallepe'

import sys
from threading import Thread

class Receiver_manager(Thread):

    def __init__(self,sock):
        Thread.__init__(self)
        self.sock = sock

    def run(self):
        while True:
            try:
                msg = self.sock.recv(1024)
                print "Message received from node: ", msg

            except Exception as e:
                print e
                sys.exit(0)