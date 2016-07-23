import Utils.globals, Utils.keyUtils.keys
from threading import Thread
from PyQt5 import QtCore, QtGui, QtWidgets
from UI.pyQt5_GUI.mainwindow import Ui_MainWindow
from Utils.OpCodes.Codes import *
import binascii
import sys
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
        nonce = int(self.pingInput.text())
        if nonce == 0:
            self.pingInput.setText(str("Please insert a random number"))
        else:
            ping = core_manager.get_ping_pkt(nonce)
            self.sendingQueue.put(ping)



    def run(self):
        self.exec_()



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
        nonce = int(self.pongInput.text())
        if nonce == 0:
            self.pongInput.setText(str("Please insert a random number"))
        else:
            pong = core_manager.get_pong_pkt(nonce)
            self.sendingQueue.put(pong)

    def run(self):
        self.exec_()

class pushDialog(QtWidgets.QDialog):

    def __init__(self, stack, scriptText, scriptLine):
        super(pushDialog, self).__init__()

        self.scriptText = scriptText
        self.scriptLine = scriptLine

        self.stack = stack
        self.sendingQueue = Utils.globals.sendingQueue

        self.setGeometry(50, 50, 500, 300)
        self.box()

    def box(self):

        self.pushData = QtWidgets.QPushButton(self)
        self.pushData.resize(200, 50)
        self.pushData.move(100, 100)
        self.pushData.setText("Push data")
        self.pushData.clicked.connect(lambda: self.pushData_clicked())

        self.label = QtWidgets.QLabel(self)
        self.label.resize(300, 20)
        self.label.move(100, 200)
        self.label.setText("Insert the data you wish to push on top of the stack")

        self.dataInput = QtWidgets.QLineEdit(self)
        self.dataInput.resize(300, 20)
        self.dataInput.move(100, 220)

        self.show()

    def pushData_clicked(self):
        data = self.dataInput.text()

        self.stack.push(data)
        if len(data)>5:
            self.scriptLine.insertPlainText("<OP_PUSH: " + data[:5] + "...> ")
        else:
            self.scriptLine.insertPlainText("<OP_PUSH: " + data + "> ")
        self.scriptText.append(self.stack.printStack())

    def run(self):
        self.exec_()



# To generate the gui python code form the .ui file, use this command:
# pyuic5 UI/pyQt5_GUI/mainwindow.ui  -o UI/pyQt5_GUI/mainwindow.py


# Used to update the UI when receving incoming message
class UI_updater(Thread):
    def __init__(self, ui):
        Thread.__init__(self)
        self.ui = ui
        # self.receivingQueue = Utils.globals.receivingQueue
        self.sendQueue = Utils.globals.sendingQueue
        self.messages = Utils.globals.messages

    def run(self):
        i = 0
        while True:
            message = self.messages.get()
            # sent = self.sendQueue.get()
            # print ("sent:", sent)
            # print ("recieves:", message)


            cmd = str(i) + "- Message: " + str(message["command"])
            self.ui.listWidget.addItem(cmd)
            i += 1

        print("Exit pyQt5_GUI Thread")


class Ui_manager():
    def __init__(self):
        self.receivingQueue = Utils.globals.receivingQueue
        self.sendingQueue = Utils.globals.sendingQueue

        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.stack = Stack()


        # Start UI
        self.ui.setupUi(self.MainWindow)

        # Init components
        self.init_components()

        UI_updater(self.ui).start()

        # CLose UI
        self.MainWindow.show()
        sys.exit(self.app.exec_())

    # define the actions when event triggered by the UI
    def init_components(self):

        # onClick on elt from listWidget, display content in the plainTextEdit
        self.ui.listWidget.itemClicked.connect(lambda: self.onClick_listWidget(self.ui.listWidget.currentItem()))

        # onClick on Version button, send Version to node
        self.ui.pushButton.toggle()
        self.ui.pushButton.clicked.connect(lambda: self.onClick_version())

        # onClick on Version button, send Verack to node
        self.ui.pushButton_2.toggle()
        self.ui.pushButton_2.clicked.connect(lambda: self.onClick_verack())

        # onClick on Version button, send Ping to node
        self.ui.pushButton_3.toggle()
        self.ui.pushButton_3.clicked.connect(lambda: self.onClick_pong())

        # onClick on newPing button, send Ping to node
        self.ui.pushButton_4.toggle()
        self.ui.pushButton_4.clicked.connect(lambda: self.onClick_Ping())

        # ...


        # ... keyUtils tab

        self.ui.createAddressButton.toggle()
        self.ui.createAddressButton.clicked.connect(lambda: self.onClick_createAddress())

        # ...


        # ... Scripts tab
        self.ui.OP_PUSH.toggle()
        self.ui.OP_PUSH.clicked.connect((lambda: self.onClick_OP_PUSH()))

        self.ui.OP_DUP.toggle()
        self.ui.OP_DUP.clicked.connect((lambda: self.onClick_OP_DUP()))

        self.ui.OP_HASH160.toggle()
        self.ui.OP_HASH160.clicked.connect((lambda: self.onClick_OP_HASH160()))

        self.ui.OP_EQUAL.toggle()
        self.ui.OP_EQUAL.clicked.connect((lambda: self.onClick_OP_EQUAL()))

        self.ui.OP_VERIFY.toggle()
        self.ui.OP_VERIFY.clicked.connect((lambda: self.onClick_OP_VERIFY()))




    def onClick_listWidget(self, item):
        id = int(item.text().split('-')[0])
        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit.setPlainText(
            Utils.globals.node_messages[id]["header"] + "\n" + Utils.globals.node_messages[id]["payload"])

    def onClick_version(self):
        version = core_manager.get_version_pkt()
        self.sendingQueue.put(version)

    def onClick_verack(self):
        verack = core_manager.get_verack_pkt()
        self.sendingQueue.put(verack)

    def onClick_createAddress(self):
        self.ui.KeysDisplay.clear()
        private_key = self.ui.privateKeyInsert.text()
        if (len(private_key) < 1):
            nk = Utils.keyUtils.keys.Key()
        else:
            nk = Utils.keyUtils.keys.Key(private_key)
        self.ui.KeysDisplay.setPlainText(str(
            "Private key: " + nk.printable_pk) + "\n"
                                         + "Public key: " + str(nk.public_key, "ascii") + "\n"
                                         + "Hashes public key: " + str(nk.hashed_public_key, "ascii") + "\n"
                                         + "Address: " + str(nk.addr))

    def onClick_Ping(self):
        dialog = newPingDialog()
        dialog.run()

    def onClick_pong(self):
        dialog = newPongDialog()
        dialog.run()


    def onClick_OP_PUSH(self):

        scriptText = self.ui.scriptText
        scriptLine = self.ui.scriptLine

        pushDialogBox = pushDialog(self.stack, scriptText, scriptLine)
        pushDialogBox.run()


    def onClick_OP_DUP(self):
        scriptText = self.ui.scriptText
        scriptLine = self.ui.scriptLine

        self.stack.OP_DUP()

        scriptLine.insertPlainText("<OP_DUP> ")
        scriptText.append(self.stack.printStack())


    def onClick_OP_HASH160(self):
        scriptText = self.ui.scriptText
        scriptLine = self.ui.scriptLine

        self.stack.OP_HASH160()

        scriptLine.insertPlainText("<OP_HASH160> ")
        scriptText.append(self.stack.printStack())


    def onClick_OP_EQUAL(self):
        scriptText = self.ui.scriptText
        scriptLine = self.ui.scriptLine

        self.stack.OP_EQUAL()

        scriptLine.insertPlainText("<OP_EQUAL> ")
        scriptText.append(self.stack.printStack())


    def onClick_OP_VERIFY(self):
        scriptText = self.ui.scriptText
        scriptLine = self.ui.scriptLine

        self.stack.OP_VERIFY()

        scriptLine.insertPlainText("<OP_VERIFY> ")
        scriptText.append(self.stack.printStack())