class EncodeGetaddr:
    def __init__(self):
        self.command_name = "getaddr"

    # getaddr messages have an empty payload
    def forge(self):
        return ""


# No need this class because, like Verack, there is no payload
class DecodeGetaddr:
    def __init__(self, payload=""):
        pass
