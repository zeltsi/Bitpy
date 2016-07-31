import Utils.globals, Utils.keyUtils.keys
from threading import Thread
from PyQt5 import QtCore, QtGui, QtWidgets
from UI.pyQt5_GUI.mainwindow import Ui_MainWindow
from Utils.OpCodes.Codes import *
import sys
from Manager import core_manager
import random
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

        except:
            pass


    def run(self):
        self.exec_()


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
        except:
            pass

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
        try:
            nonce = int(self.pongInput.text())
            if nonce == 0:
                self.pongInput.setText(str("Please insert a random number"))
            else:
                pong = core_manager.get_pong_pkt(nonce)
                self.sendingQueue.put(pong)
        except:
            pass

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
        try:
            data = self.dataInput.text()

            self.stack.push(data)
            if len(data)>5:
                self.scriptLine.insertPlainText("<OP_PUSH: " + data[:5] + "...> ")
            else:
                self.scriptLine.insertPlainText("<OP_PUSH: " + data + "> ")
            self.scriptText.append(self.stack.printStack())
        except:
            pass

    def run(self):
        self.exec_()

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
            version = core_manager.get_version_pkt(agent)
            self.sendingQueue.put(version)
        except:
            pass

    def run(self):
        self.exec_()


class op_returnDialog(QtWidgets.QDialog):
    def __init__(self, stack, scriptText, scriptLine):
        super(op_returnDialog, self).__init__()

        self.scriptText = scriptText
        self.scriptLine = scriptLine

        self.sendingQueue = Utils.globals.sendingQueue

        self.stack = stack

        self.setGeometry(50, 50, 500, 300)
        self.box()

    def box(self):
        self.sendBtn = QtWidgets.QPushButton(self)
        self.sendBtn.resize(200, 50)
        self.sendBtn.move(100, 100)
        self.sendBtn.setText("Insert message")
        self.sendBtn.clicked.connect(lambda: self.sendBtn_clicked())

        self.label = QtWidgets.QLabel(self)
        self.label.resize(300, 20)
        self.label.move(100, 200)
        self.label.setText("40 bytes message")

        self.theInput = QtWidgets.QLineEdit(self)
        self.theInput.resize(300, 20)
        self.theInput.move(100, 220)

        self.show()

    def sendBtn_clicked(self):
        try:
            input = str.encode(self.theInput.text())

            self.stack.OP_RETURN(input)
            input = bytes.decode(input)
            self.scriptLine.insertPlainText("<OP_RETURN: " + input + "...> ")
            self.scriptText.append(self.stack.printStack())
        except:
            pass

    def run(self):
        self.exec_()




# To generate the gui python code form the .ui file, use this command:
# pyuic5 UI/pyQt5_GUI/mainwindow.ui  -o UI/pyQt5_GUI/mainwindow.py


# Used to update the UI when receving incoming message
class UI_updater(Thread):
    def __init__(self, ui):
        Thread.__init__(self)
        self.ui = ui
        self.sendQueue = Utils.globals.sendingQueue
        self.messages = Utils.globals.messages

    def run(self):
        i = 0
        while True:
            message = self.messages.get()

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

        self.ui.connectBtn.toggle()
        self.ui.connectBtn.clicked.connect(lambda: self.onClick_Connect())

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

        self.ui.clearBtn.toggle()
        self.ui.clearBtn.clicked.connect((lambda: self.onClick_clearBtn()))

        self.ui.OP_RETURN.toggle()
        self.ui.OP_RETURN.clicked.connect((lambda: self.onClick_OP_RETURN()))



    def onClick_Connect(self):
        dialog = connectDialog()
        dialog.run()

    def onClick_listWidget(self, item):
        id = int(item.text().split('-')[0])
        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit.setPlainText(
            Utils.globals.node_messages[id]["header"] + "\n" + Utils.globals.node_messages[id]["payload"])

    def onClick_version(self):
        dialog = versionMsgDialog()
        dialog.run()


    def onClick_verack(self):
        verack = core_manager.get_verack_pkt()
        self.sendingQueue.put(verack)


    def onClick_createAddress(self):
        self.ui.KeysDisplay.clear()
        private_key = self.ui.privateKeyInsert.text()
        if (len(private_key) < 1):
            nk = Utils.keyUtils.keys.Key()
        else:
            try:
                nk = Utils.keyUtils.keys.Key(private_key)
            except:
                pass

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


    def onClick_clearBtn(self):
        self.stack.clear()
        scriptText = self.ui.scriptText
        scriptLine = self.ui.scriptLine

        scriptLine.clear()
        scriptText.clear()


    def onClick_OP_PUSH(self):
        scriptText = self.ui.scriptText
        scriptLine = self.ui.scriptLine

        pushDialogBox = pushDialog(self.stack, scriptText, scriptLine)
        pushDialogBox.run()


    def onClick_OP_DUP(self):
        scriptText = self.ui.scriptText
        scriptLine = self.ui.scriptLine

        try:
            self.stack.OP_DUP()
        except:
            pass

        scriptLine.insertPlainText("<OP_DUP> ")
        scriptText.append(self.stack.printStack())


    def onClick_OP_HASH160(self):
        scriptText = self.ui.scriptText
        scriptLine = self.ui.scriptLine
        try:
            self.stack.OP_HASH160()
        except:
            pass

        scriptLine.insertPlainText("<OP_HASH160> ")
        scriptText.append(self.stack.printStack())


    def onClick_OP_EQUAL(self):
        scriptText = self.ui.scriptText
        scriptLine = self.ui.scriptLine

        try:
            self.stack.OP_EQUAL()
        except:
            pass

        scriptLine.insertPlainText("<OP_EQUAL> ")
        scriptText.append(self.stack.printStack())


    def onClick_OP_VERIFY(self):
        scriptText = self.ui.scriptText
        scriptLine = self.ui.scriptLine

        self.stack.OP_VERIFY()

        scriptLine.insertPlainText("<OP_VERIFY> ")
        scriptText.append(self.stack.printStack())

    def onClick_OP_RETURN(self):
        scriptText = self.ui.scriptText
        scriptLine = self.ui.scriptLine

        dialog = op_returnDialog(self.stack, scriptText, scriptLine)
        dialog.run()