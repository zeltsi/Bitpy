__author__ = "Shlomi Zeltsinger, Alexis Gallèpe"

import queue

from Manager import ReceiverManager, SenderManager
from Network import Connection
from Manager import core_manager


def main():

    # Connexion to our node
    sock = Connection.connect()

    # Start receiver Thread that will loop for incoming node messages
    receiver = ReceiverManager.ReceiverManager(sock)
    receiver.start()

    # Start Sender Thread that will loop for messages to send to node
    sender = SenderManager.SenderManager(sock)
    sender.start()

    core_manager.Manager()


if "__main__" == __name__:
    main()
