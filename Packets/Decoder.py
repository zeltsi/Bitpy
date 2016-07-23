from Packets.HeaderParser import HeaderParser
from Packets.PacketCreator import *
from Packets.control_messages import *
from Packets.data_messages import *


def manager(parsedHeader, payloadStream):

    command = parsedHeader.command.decode("utf-8")
    message = {"timestamp": time.time(), "command": command, "header": parsedHeader.to_string(), "payload": ""}


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