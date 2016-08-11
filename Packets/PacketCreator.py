__author__ = 'alexisgallepe and Shlomi Zeltsinger'

import Utils.globals
import hashlib
from Utils.globals import *
import time
from Packets.HeaderParser import HeaderParser
from Packets.control_messages import Verack, Version, GetAddr, Ping, Pong, Addr
from  Packets.data_messages import GetBlocks, Inv
from io import BytesIO

class PacketCreator:
    def __init__(self, payload):

        try:
            self.payload = str.encode(payload.forge())  # The message payload forged
        except:
            self.payload = payload.forge()

        # Create the header
        self.magic = to_hexa("F9BEB4D9")  # The Magic number of the Main network -> This message will be accepted by the main network
        self.command = self.command_padding(payload.command_name)
        self.length = to_uint32(len(self.payload))
        self.checksum = self.get_checksum()

        self.command_name =str(payload.command_name) #for dispaly only

    # The message command should be padded to be 12 bytes long.
    def command_padding(self, cmd):
        command = str(cmd)
        command = command.ljust(12, '\00')
        return str.encode(command)

    def get_checksum(self):
        return hashlib.sha256(hashlib.sha256( self.payload ).digest()).digest()[:4]

    def forge_header(self):
        return self.magic + self.command + self.length + self.checksum

    def forge_packet(self):
        self.encode()
        return self.forge_header() + self.payload


    def encode(self):
        header = self.forge_header()

        headerStream = BytesIO(header)
        parsedHeader = HeaderParser(headerStream)

        # get the payload

        payloadStream = BytesIO(self.payload)

        self.manager(parsedHeader, payloadStream)

    def manager(self, parsedHeader, payloadStream):
        command = parsedHeader.command.decode("utf-8")
        message = {"timestamp": time.time(), "command": "Output - " + command, "header": parsedHeader.to_string(), "payload": ""}

        if command.startswith('ping'):
            ping = Ping.DecodePing(payloadStream)
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