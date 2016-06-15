__author__ = 'alexisgallepe'

from Network.HeaderParser import HeaderParser
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

                print "Message received from node: ", msg
                header = HeaderParser(msg)
                print header.toString()

            except Exception as e:
                print e
                break

        print "Exit receiver Thread"