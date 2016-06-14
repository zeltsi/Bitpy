__author__ = "Shlomi Zeltsinger, Alexis Gallepe"

import socket
import sys
import Receiver_manager
import Sender_manager
import Queue
from Network.PacketCreator import *

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

    payload = Version.Version()
    header = Header.Header(payload, "version")

    forgedPacket = header.forge() + payload.forge()
    senderQueue.put(forgedPacket)


def main():

    #Queue where we put every messages we want to send to our connected node
    senderQueue = Queue.Queue()

    #Connexion to our node
    sock = connect_to_node()

    #Start receiver Thread that will loop for node messages
    receiver = Receiver_manager.Receiver_manager(sock)
    receiver.start()

    #Start Sender Thread that will loop for messages to send to node
    sender = Sender_manager.Sender_manager(sock,senderQueue)
    sender.start()

    test_send_version(senderQueue)

if "__main__"  == __name__:
    main()