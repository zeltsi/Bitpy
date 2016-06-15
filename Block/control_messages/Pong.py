
class EncodePong():
    def __init__(self,ping_received):
        self.command_name = "pong"

        self.nonce = ping_received

    def forge(self):
        return self.nonce


class DecodePong():
    def __init__(self,ping_received):
        self.command_name = "pong"

        self.nonce = ping_received
