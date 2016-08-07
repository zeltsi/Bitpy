import sys
from threading import Thread

from PyQt5 import QtWidgets

import Utils.globals
import Utils.keyUtils.keys
from Manager import core_manager
from UI.pyQt5_GUI.Diologs import connectDialog, newPongDialog, pushDialog, versionMsgDialog, op_returnDialog, newPingDialog
from UI.pyQt5_GUI.mainwindow import Ui_MainWindow
from Utils.OpCodes.Codes import *


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
        dialog = connectDialog.connectDialog()
        dialog.run()

    def onClick_listWidget(self, item):
        id = int(item.text().split('-')[0])
        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit.setPlainText(
            Utils.globals.node_messages[id]["header"] + "\n" + Utils.globals.node_messages[id]["payload"])

    def onClick_version(self):
        dialog = versionMsgDialog.versionMsgDialog()
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
        dialog = newPingDialog.newPingDialog()
        dialog.run()


    def onClick_pong(self):
        dialog = newPongDialog.newPongDialog()
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

        pushDialogBox = pushDialog.pushDialog(self.stack, scriptText, scriptLine)
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

        dialog = op_returnDialog.op_returnDialog(self.stack, scriptText, scriptLine)
        dialog.run()

