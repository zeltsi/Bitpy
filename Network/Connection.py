import socket
import sys

HOST = "216.218.235.90"
PORT = 8333

"""
    We will use this file to connect to one node
    But in the future we will connect to more than one
"""


def connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, PORT))
    except Exception as e:
        print(e)
        sys.exit(0)

    return sock
