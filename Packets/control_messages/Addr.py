import random
import time
from Utils.config import version_number, latest_known_block
from Utils.dataTypes import *
from io import BytesIO

class EncodeAddr():
    def __init__(self):
        self.command_name = "addr"



    def forge(self):
        return self.version + self.services



class DecodeAddr():
    def __init__(self,payload):
        pass


