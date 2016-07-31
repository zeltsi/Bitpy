__author__ = 'alexisgallepe'

from Packets.PacketCreator import *
from Packets.control_messages import *
from Packets.data_messages import *


import Utils.globals
from io import BytesIO
from threading import Thread
import time


class ReceiverManager(Thread):
    def __init__(self, sock):
        Thread.__init__(self)
        self.sendingQueue = Utils.globals.sendingQueue
        self.sock = sock
        self.ping = ""

        self.outfile = open("data_received_from_node.txt", 'w')

    def run(self):
        while True:
            try:

                # get only the header's message
                header = self.sock.recv(24)

                if len(header) <= 0:
                    raise Exception("Node disconnected (received 0bit length message)")

                headerStream = BytesIO(header)
                parsedHeader = HeaderParser(headerStream)

                # get the payload
                payload = self.recvall(parsedHeader.payload_size)
                payloadStream = BytesIO(payload)

                self.manager(parsedHeader, payloadStream)

            except Exception as e:
                print(e)
                break

        print("Exit receiver Thread")


    def manager(self, parsedHeader, payloadStream):

        command = parsedHeader.command.decode("utf-8")
        message = {"timestamp": time.time(), "command": command, "header": parsedHeader.to_string(), "payload": ""}


        if command.startswith('ping'):
            ping = Ping.DecodePing(payloadStream)

            # pong = Pong.EncodePong(ping.nonce)
            # packet = PacketCreator(pong)
            # self.sendingQueue.put(packet.forge_packet())

            message["payload"] = str(ping.nonce)
            self.display(message)

        elif command.startswith('inv'):
            inv = Inv.DecodeInv(payloadStream)
            message["payload"] = inv.get_decoded_info()
            self.display(message)

        elif command.startswith('addr'):
            addr = Addr.DecodeAddr(payloadStream)
            message["payload"] = addr.get_decoded_info()
            self.display(message)

        elif command.startswith('pong'):
            pong = Pong.DecodePong(payloadStream)
            message["payload"] = pong.get_decoded_info()
            self.display(message)

        elif command.startswith('version'):
            version = Version.DecodeVersion(payloadStream)
            message["payload"] = version.get_decoded_info()
            self.display(message)

        elif command.startswith('verack'):
            verack = Verack.DecodeVerack(payloadStream)
            message["payload"] = verack.get_decoded_info()
            self.display(message)



    def display(self, message):
        Utils.globals.node_messages.append(message)

        if Utils.globals.UI == "CLI" or Utils.globals.UI == "tkinter_gui":
            self.outfile.write(message["payload"])
            self.outfile.flush()

        elif Utils.globals.UI == "pyQt5_gui":
            Utils.globals.messages.put(message)


    def recvall(self, length):
        parts = []

        while length > 0:
            part = self.sock.recv(length)
            if not part:
                raise EOFError('socket closed with %d bytes left in this part'.format(length))

            length -= len(part)
            parts.append(part)

        return b''.join(parts)