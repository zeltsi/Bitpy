import time
import random

from Utils.dataTypes import *


class Pong():
    def __init__(self,ping_received):
        self.nonce = ping_received

    def forge(self):
        return self.nonce