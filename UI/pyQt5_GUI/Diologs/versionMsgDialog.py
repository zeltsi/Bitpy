import Utils.globals, Utils.keyUtils.keys
from PyQt5 import QtWidgets
from Utils.OpCodes.Codes import *
from Manager import core_manager

class versionMsgDialog(QtWidgets.QDialog):

    def __init__(self):
        super(versionMsgDialog, self).__init__()

        self.sendingQueue = Utils.globals.sendingQueue

        self.setGeometry(50, 50, 500, 300)
        self.box()

    def box(self):
        self.sendVersionMsg = QtWidgets.QPushButton(self)
        self.sendVersionMsg.resize(200, 50)
        self.sendVersionMsg.move(100, 100)
        self.sendVersionMsg.setText("send version message")
        self.sendVersionMsg.clicked.connect(lambda: self.sendVersionMsg_clicked())

        self.label = QtWidgets.QLabel(self)
        self.label.resize(300, 20)
        self.label.move(100, 200)
        self.label.setText("Insert agent name")

        self.agentInput = QtWidgets.QLineEdit(self)
        self.agentInput.resize(300, 20)
        self.agentInput.move(100, 220)

        self.show()


    def sendVersionMsg_clicked(self):
        try:
            agent = str(self.agentInput.text())
            print (agent)
            version = core_manager.get_version_pkt(agent)
            self.sendingQueue.put(version)
            self.close()

        except:
            pass

    def run(self):
        self.exec_()
