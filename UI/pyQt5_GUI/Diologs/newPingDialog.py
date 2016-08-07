import Utils.globals, Utils.keyUtils.keys
from PyQt5 import QtWidgets
from Utils.OpCodes.Codes import *
from Manager import core_manager
import random

class newPingDialog(QtWidgets.QDialog):

    def __init__(self):
        super(newPingDialog, self).__init__()

        self.sendingQueue = Utils.globals.sendingQueue

        self.setGeometry(50, 50, 500, 300)
        self.box()

    def box(self):
        self.generateRandom = QtWidgets.QPushButton(self)
        self.generateRandom.resize(200, 50)
        self.generateRandom.move(100, 50)
        self.generateRandom.setText("Generate random number")
        self.generateRandom.clicked.connect(lambda: self.generateRandom_clicked())

        self.sendPing = QtWidgets.QPushButton(self)
        self.sendPing.resize(200, 50)
        self.sendPing.move(100, 100)
        self.sendPing.setText("Send ping")
        self.sendPing.clicked.connect(lambda: self.sendPing_clicked())

        self.label = QtWidgets.QLabel(self)
        self.label.resize(300, 20)
        self.label.move(100, 200)
        self.label.setText("Please Insert a random Uint64 number")

        self.pingInput = QtWidgets.QLineEdit(self)
        self.pingInput.resize(300, 20)
        self.pingInput.move(100, 220)


        self.show()

    def generateRandom_clicked(self):
        self.pingInput.setText(str(random.getrandbits(64)))

    def sendPing_clicked(self):
        try:
            nonce = int(self.pingInput.text())
            if nonce == 0:
                self.pingInput.setText(str("Please insert a random number"))
            else:
                ping = core_manager.get_ping_pkt(nonce)
                self.sendingQueue.put(ping)
                self.close()

        except:
            pass

    def run(self):
        self.exec_()