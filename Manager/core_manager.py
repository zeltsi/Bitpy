__author__ = 'alexisgallepe and Shlomi Zeltsinger'

import Utils.globals
from Packets.PacketCreator import *
from Packets.control_messages import Verack, Version, GetAddr, Ping, Pong, Addr
from  Packets.data_messages import GetBlocks, Inv


def get_version_pkt(agent):
    version = Version.EncodeVersion(agent)
    return PacketCreator(version).forge_packet()

def get_verack_pkt():
    verack = Verack.EncodeVerack()
    return PacketCreator(verack).forge_packet()

def get_getAddr_pkt():
    getAddr = GetAddr.EncodeGetaddr()
    return PacketCreator(getAddr).forge_packet()

def get_ping_pkt(nonce=0):
    ping = Ping.EncodePing(nonce)
    return PacketCreator(ping).forge_packet()

def get_pong_pkt(nonce=0):
    pong = Pong.EncodePong(nonce)
    return PacketCreator(pong).forge_packet()

def get_getBlocks_pkt(hashes=["5c3e6403d40837110a2e8afb602b1c01714bda7ce23bea0a0000000000000000"]):
    getBlocks = GetBlocks.EncodeGetblocks(hashes)
    return PacketCreator(getBlocks).forge_packet()


class Manager(object):
    def __init__(self):
        self.sendingQueue = Utils.globals.sendingQueue

        from UI.pyQt5_GUI.pyQt5_GUI import Ui_manager
        Utils.globals.UI = "pyQt5_gui"
        ui = Ui_manager()

#
# class Manager(object):
#     def __init__(self):
#         self.sendingQueue = Utils.globals.sendingQueue
#
#         print("-- BitPy --")
#         print("Choose your UI:")
#         print("0: CLI")
#         print("1: Tkinter")
#         print("2: pyQt 5 (pyQt5 library required)")
#
#         ui = int(input(">"))
#
#         if ui == 0:
#             from UI.CLI.CLI import CLI
#             Utils.globals.UI = "CLI"
#             CLI()
#
#         elif ui == 1:
#             from UI.tkinter_GUI.tkinter_GUI import start_GUI
#             Utils.globals.UI = "tkinter_gui"
#             start_GUI()
#
#         elif ui == 2:
#             from UI.pyQt5_GUI.pyQt5_GUI import Ui_manager
#             Utils.globals.UI = "pyQt5_gui"
#             ui = Ui_manager()


