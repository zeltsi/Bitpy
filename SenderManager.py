__author__ = 'alexisgallepe'

from threading import Thread

class SenderManager(Thread):

    def __init__(self,sock, queue):
        Thread.__init__(self)
        self.sock = sock
        self.queue = queue

    def run(self):
        while True:
            if not self.queue.empty():
                order = self.queue.get()
                self.sock.send(order)
                print "Message sent to node"

        print "Exit sender Thread"