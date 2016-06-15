__author__ = "Shlomi Zeltsinger, Alexis Gallepe"

import Queue

from Manager import ReceiverManager, SenderManager
from Block.PacketCreator import PacketCreator
from Block.control_messages.Version import EncodeVersion
from Network import Connection


def test_send_version(senderQueue):

    version = EncodeVersion()
    packet = PacketCreator(version)

    senderQueue.put(packet.forge_packet())


def main():

    #Queue where we put every messages we want to send to our connected node
    senderQueue = Queue.Queue()

    #Connexion to our node
    sock = Connection.connect()

    #Start receiver Thread that will loop for node messages
    receiver = ReceiverManager.ReceiverManager(sock)
    receiver.start()

    #Start Sender Thread that will loop for messages to send to node
    sender = SenderManager.SenderManager(sock,senderQueue)
    sender.start()

    test_send_version(senderQueue)

if "__main__"  == __name__:
    main()