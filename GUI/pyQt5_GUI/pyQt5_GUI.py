from PyQt5 import QtCore, QtGui, QtWidgets
from GUI.pyQt5_GUI.mainwindow import Ui_MainWindow
import sys

# pyuic5 mainwindow.ui -o mainwindow.py
# ui.listWidget.addItem('Item %s' % (i + 1))

class Ui_manager:

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()

        # Start GUI
        self.ui.setupUi(self.MainWindow)

        # Init components
        self.init_components()

        # CLose GUI
        self.MainWindow.show()
        sys.exit(self.app.exec_())


    def init_components(self):

        self.ui.listWidget.itemClicked.connect(lambda: self.onClick_listWidget(self.ui.listWidget.currentItem()) )

        self.ui.pushButton.toggle()
        self.ui.pushButton.clicked.connect(lambda: self.onClick_button())


    def onClick_listWidget(self, item):
        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit.setPlainText(item.text() + " rgjhnsdkfjghslkfj")


    def onClick_button(self):
        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit.setPlainText(" rgjhnsdkfjghslkfj")


    def onClick_button2(self):
        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit.setPlainText(" rgjhnsdkfjghslkfj")

