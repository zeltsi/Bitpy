import PacketCreator


class VerAck():
    def __init__(self):
        #Verack messages have an empty payload
        pass

    def forgePayload(self):
        return ""

VerAck_msg = PacketCreator.packet(VerAck().forgePayload(), "VerAck")