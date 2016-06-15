
class EncodeVerack():
    def __init__(self):
        self.command_name = "verack"

    #Verack messages have an empty payload
    def forge(self):
        return ""


class DecodeVerack():
    def __init__(self):
        self.command_name = "verack"



