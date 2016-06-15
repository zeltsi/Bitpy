__author__ = "Shlomi Zeltsinger, Alexis Gallepe"

import socket
import sys
import Queue

import ReceiverManager
import SenderManager
from Network.PacketCreator import PacketCreator
from Network.control_messages.Version import EncodeVersion

HOST = "66.90.137.89"
PORT = 8333

def connect_to_node():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, PORT))
    except Exception as e:
        print e
        sys.exit(0)

    return sock


def test_send_version(senderQueue):

    version = EncodeVersion()
    packet = PacketCreator(version)

    senderQueue.put(packet.forge_packet())


def main():

    #Queue where we put every messages we want to send to our connected node
    senderQueue = Queue.Queue()

    #Connexion to our node
    sock = connect_to_node()

    #Start receiver Thread that will loop for node messages
    receiver = ReceiverManager.ReceiverManager(sock)
    receiver.start()

    #Start Sender Thread that will loop for messages to send to node
    sender = SenderManager.SenderManager(sock,senderQueue)
    sender.start()

    test_send_version(senderQueue)

if "__main__"  == __name__:
    main()