import Utils.globals, Utils.keyUtils.keys
from PyQt5 import QtWidgets
from Utils.OpCodes.Codes import *



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

            self.close()
            self.scriptText.append(self.stack.printStack())
        except:
            pass

    def run(self):
        self.exec_()