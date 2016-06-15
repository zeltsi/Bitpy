__author__ = 'alexisgallepe'

from Block.HeaderParser import HeaderParser
from threading import Thread

class ReceiverManager(Thread):

    def __init__(self,sock):
        Thread.__init__(self)
        self.sock = sock

    def run(self):
        while True:
            try:
                msg = self.sock.recv(1024)

                if len(msg) <= 0:
                    raise Exception("Node disconnected (received 0bit length message)")

                header = HeaderParser(msg)
                header.to_string()

            except Exception as e:
                print e
                break

        print "Exit receiver Thread"