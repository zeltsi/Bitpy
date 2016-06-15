import PacketCreator
import Utils.dataTypes


class Pong():
    def __init__(self,ping_received):
        self.nonce = ping_received

    def forgePayload(self):
        return self.nonce