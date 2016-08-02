from Packets.HeaderParser import HeaderParser
from Packets.PacketCreator import *
import Packets.control_messages
import Packets.data_messages


def manager(parsedHeader, payloadStream):

    command = parsedHeader.command.decode("utf-8")
    message = {"timestamp": time.time(), "command": command, "header": parsedHeader.to_string(), "payload": ""}


    if command.startswith('ping'):
        ping = Packets.control_messages.Ping.DecodePing(payloadStream)
        message["payload"] = str(ping.nonce)
        self.display(message)

    elif command.startswith('inv'):
        inv = Packets.control_messages.Inv.DecodeInv(payloadStream)
        message["payload"] = inv.get_decoded_info()
        self.display(message)

    elif command.startswith('addr'):
        addr = Packets.control_messages.Addr.DecodeAddr(payloadStream)
        message["payload"] = addr.get_decoded_info()
        self.display(message)

    elif command.startswith('pong'):
        pong = Packets.control_messages.Pong.DecodePong(payloadStream)
        message["payload"] = pong.get_decoded_info()
        self.display(message)

    elif command.startswith('version'):
        version = Packets.control_messages.Version.DecodeVersion(payloadStream)
        message["payload"] = version.get_decoded_info()
        self.display(message)