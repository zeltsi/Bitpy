
class EncodeVerack():
    def __init__(self):
        self.command_name = "verack"

    #Verack messages have an empty payload
    def forge(self):
        return ""


#No need this class because, like GetAddr, there is no payload
class DecodeVerack():
    def __init__(self,payload=""):
        pass



