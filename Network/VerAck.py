import time
import random

from Utils.dataTypes import *


class VerAck():
    def __init__(self):
        #Verack messages have an empty payload
        pass

    def forge(self):
        return ""