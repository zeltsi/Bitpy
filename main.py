__author__ = "Shlomi Zeltsinger, Alexis Gallepe"

import Queue

from Manager import ReceiverManager, SenderManager
from Network import Connection
from Manager import core_manager



def main():

    #Queue where we put every messages we want to send to our connected node
    senderQueue = Queue.Queue()

    #Connexion to our node
    sock = Connection.connect()

    #Start receiver Thread that will loop for node messages
    receiver = ReceiverManager.ReceiverManager(sock,senderQueue)
    receiver.start()

    #Start Sender Thread that will loop for messages to send to node
    sender = SenderManager.SenderManager(sock,senderQueue)
    sender.start()

    core_manager.Manager(senderQueue)

if "__main__"  == __name__:
    main()