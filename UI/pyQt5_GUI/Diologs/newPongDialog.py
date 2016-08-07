import Utils.globals, Utils.keyUtils.keys
from PyQt5 import QtWidgets
from Utils.OpCodes.Codes import *
from Manager import core_manager

class newPongDialog(QtWidgets.QDialog):

    def __init__(self):
        super(newPongDialog, self).__init__()

        self.sendingQueue = Utils.globals.sendingQueue

        self.setGeometry(50, 50, 500, 300)
        self.box()

    def box(self):

        self.sendPong = QtWidgets.QPushButton(self)
        self.sendPong.resize(200, 50)
        self.sendPong.move(100, 100)
        self.sendPong.setText("Send pong")
        self.sendPong.clicked.connect(lambda: self.sendPong_clicked())

        self.label = QtWidgets.QLabel(self)
        self.label.resize(300, 20)
        self.label.move(100, 200)
        self.label.setText("Insert the ping number that was received from the remote node")

        self.pongInput = QtWidgets.QLineEdit(self)
        self.pongInput.resize(300, 20)
        self.pongInput.move(100, 220)

        self.show()

    def sendPong_clicked(self):
        try:
            nonce = int(self.pongInput.text())
            if nonce == 0:
                self.pongInput.setText(str("Please insert a random number"))
            else:
                pong = core_manager.get_pong_pkt(nonce)
                self.sendingQueue.put(pong)
                self.close()

        except:
            pass

    def run(self):
        self.exec_()
