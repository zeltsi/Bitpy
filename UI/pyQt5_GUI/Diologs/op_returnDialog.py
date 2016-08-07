import Utils.globals, Utils.keyUtils.keys
from PyQt5 import QtWidgets
from Utils.OpCodes.Codes import *


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
            self.close()

        except:
            pass

    def run(self):
        self.exec_()
