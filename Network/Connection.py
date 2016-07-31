import socket
import sys
import Utils.globals
from Manager import ReceiverManager, SenderManager

"""
    We will use this file to connect to one node
    But in the future we will connect to more than one
"""


def connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((Utils.globals.HOST, Utils.globals.PORT))

    # Start receiver Thread that will loop for incoming node messages
        receiver = ReceiverManager.ReceiverManager(sock)
        receiver.start()

        # Start Sender Thread that will loop for messages to send to node
        sender = SenderManager.SenderManager(sock)
        sender.start()

    except Exception as e:
        print(e)
        sys.exit(0)

    return sock


