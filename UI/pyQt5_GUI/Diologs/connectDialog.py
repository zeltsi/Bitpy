import Utils.globals, Utils.keyUtils.keys
from PyQt5 import QtWidgets
from Utils.OpCodes.Codes import *
import Network.Connection

class connectDialog(QtWidgets.QDialog):

    def __init__(self):
        super(connectDialog, self).__init__()

        self.setGeometry(50, 50, 500, 300)
        self.box()

    def box(self):

        self.connect = QtWidgets.QPushButton(self)
        self.connect.resize(200, 50)
        self.connect.move(100, 100)
        self.connect.setText("Conncect")
        self.connect.clicked.connect(lambda: self.connect_clicked())

        self.labelIp = QtWidgets.QLabel(self)
        self.labelIp.resize(300, 20)
        self.labelIp.move(100, 200)
        self.labelIp.setText("IP address of remote node")

        self.ipInput = QtWidgets.QLineEdit(self)
        self.ipInput.resize(300, 20)
        self.ipInput.move(100, 220)

        self.labelPort = QtWidgets.QLabel(self)
        self.labelPort.resize(300, 20)
        self.labelPort.move(100, 250)
        self.labelPort.setText("Port number of the remote node")

        self.portInput = QtWidgets.QLineEdit(self)
        self.portInput.resize(300, 20)
        self.portInput.move(100, 270)


        self.show()

    def connect_clicked(self):
        try:
            Utils.globals.HOST = str(self.ipInput.text())
            Utils.globals.PORT = int(self.portInput.text())

            Network.Connection.connect()
            self.close()
        except:
            pass


    def run(self):
        self.exec_()
