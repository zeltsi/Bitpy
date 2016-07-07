import Utils.globals

__author__ = 'alexisgallepe'

from threading import Thread


class SenderManager(Thread):
    def __init__(self, sock):
        Thread.__init__(self)
        self.sock = sock
        self.sendingQueue = Utils.globals.sendingQueue

    def run(self):
        while True:
            order = self.sendingQueue.get()
            self.sock.sendall(order)

        print("Exit sender Thread")
