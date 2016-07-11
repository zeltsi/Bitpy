import Utils.globals, Utils.keyUtils.keys
from threading import Thread
from PyQt5 import QtCore, QtGui, QtWidgets
from UI.pyQt5_GUI.mainwindow import Ui_MainWindow
import sys
from Manager import core_manager



# To generate the gui python code form the .ui file, use this command:
# pyuic5 UI/pyQt5_GUI/mainwindow.ui  -o UI/pyQt5_GUI/mainwindow.py


# Used to update the UI when receving incoming message
class UI_updater(Thread):

    def __init__(self,ui):
        Thread.__init__(self)
        self.ui = ui
        self.receivingQueue = Utils.globals.receivingQueue

    def run(self):
        i = 0
        while True:
            message = self.receivingQueue.get()
            cmd = str(i) + "- Message: " + str(message["command"])
            self.ui.listWidget.addItem(cmd)
            i += 1

        print("Exit pyQt5_GUI Thread")



class Ui_manager:

    def __init__(self):
        self.receivingQueue = Utils.globals.receivingQueue
        self.sendingQueue = Utils.globals.sendingQueue

        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()

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
        self.ui.listWidget.itemClicked.connect(lambda: self.onClick_listWidget(self.ui.listWidget.currentItem()) )

        # onClick on Version button, send Version to node
        self.ui.pushButton.toggle()
        self.ui.pushButton.clicked.connect(lambda: self.onClick_version())

        # onClick on Version button, send Verack to node
        self.ui.pushButton_2.toggle()
        self.ui.pushButton_2.clicked.connect(lambda: self.onClick_verack())

        # onClick on Version button, send Ping to node
        self.ui.pushButton_3.toggle()
        self.ui.pushButton_3.clicked.connect(lambda: self.onClick_ping())

        # ...


        #... keyUtils tab

        self.ui.createAddressButton.toggle()
        self.ui.createAddressButton.clicked.connect(lambda: self.onClick_createAddress())

        # ...


    def onClick_listWidget(self, item):
        id = int(item.text().split('-')[0])
        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit.setPlainText(Utils.globals.node_messages[id]["header"] + "\n" + Utils.globals.node_messages[id]["payload"])

    def onClick_version(self):
        version = core_manager.get_version_pkt()
        self.sendingQueue.put(version)

    def onClick_verack(self):
        verack = core_manager.get_verack_pkt()
        self.sendingQueue.put(verack)

    def onClick_ping(self):
        ping = core_manager.get_ping_pkt()
        self.sendingQueue.put(ping)


    def onClick_createAddress(self):
        self.ui.KeysDisplay.clear()
        private_key = self.ui.privateKeyInsert.text()
        if (len(private_key)<1):
            print ("here")
            nk = Utils.keyUtils.keys.Key()
        else:
            print ("there")
            nk = Utils.keyUtils.keys.Key(private_key)
        self.ui.KeysDisplay.setPlainText(str(
              "Private key: " + nk.printable_pk) + "\n"
             + "Public key: " + str(nk.public_key, "ascii") + "\n"
             + "Hashes public key: " + str(nk.hashed_public_key, "ascii") + "\n"
             + "Address: " + str(nk.addr))

