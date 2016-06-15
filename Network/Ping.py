import PacketCreator
import random
import Utils.dataTypes


class Ping():
    def __init__(self):
        self.nonce = Utils.dataTypes.to_uint64(random.getrandbits(64))

    def forgePayload(self):
        return self.nonce

Ping_msg = PacketCreator.packet(Ping().forgePayload(), "Ping")