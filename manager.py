__author__ = 'alexisgallepe'


class Manager:

    def __init__(self,message):
        self.message = message
        self.header = self.parseHeader(message)



    def parseHeader(self):