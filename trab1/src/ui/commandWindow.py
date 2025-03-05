##################### Imports
from PyQt5.QtCore import *      # Basic Qt functionalities.
from PyQt5.QtWidgets import *   # GUI windows
from PyQt5.QtCore import *      # Qt threads, ...
from PyQt5.QtGui import *       # GUI Elements

##################### Commands Window Class
class commandWindow(QWidget):
    def __init__(self, int_commands, ext_commands):
        super().__init__()
        self.setWindowTitle("Commands")
        self.intCommands = int_commands
        self.extCommands = ext_commands

        self.commandOutputLine = QTextEdit()
        self.commandOutputLine.setReadOnly(True)
        
        self.setFixedSize(600,500)

        self.logTextSplashScreen = ""

        self.setCommandText()

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.commandOutputLine)

    def setCommandText(self):
        self.commandOutputLine.setPlainText(self.logTextSplashScreen + \
                "* Internal Commands - Processed by RaspberryPi:\n" + self.intCommands + "\n" + \
                "* External Commands - Processed by Arduino:\n" + self.extCommands)

    def updateExternalCommands(self,desc):
        self.extCommands = desc
        self.setCommandText()