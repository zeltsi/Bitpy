import hashlib
import time
import random
from dataTypes import *

class Header(): # Takes two arguments, the payload of the message and the message command
    def __init__(self, payload, command):
        self.payload = payload.forge()  # The message payload
        self.magic = to_hexa("F9BEB4D9")  # The Magic number of the Main network -> This message will be accepted by the main network
        self.command = self.command_padding(command)
        self.checksum = self.checksum()
        self.length = to_uint32(len(self.payload))

    def command_padding(self, command):  # The message command should be padded to be 12 bytes long.
        command = command + (12 - len(command)) * "\00"
        return command

    def checksum(self):
        check = hashlib.sha256(hashlib.sha256(self.payload).digest()).digest()[:4]
        return check

    def forge(self):
        return self.magic + self.command + self.length + self.checksum