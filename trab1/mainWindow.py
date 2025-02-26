##################### Python Library Imports

# UI
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QStyle,
)
from PyQt5.QtGui import QPixmap
import pyqtgraph    # For Data Visualization.

##################### User defined functions (imports)
from arduinoComms import arduinoComms

##################### Main Programme Class

# Class which inherits from QWidget class. Contains UI functionalities.

class commandWindow(QWidget):
    def __init__(self, int_commands, ext_commands):
        super().__init__()
        self.setWindowTitle("Commands")
        self.intCommands = int_commands
        self.extCommands = ext_commands

        self.commandOutputLine = QTextEdit()
        self.commandOutputLine.setReadOnly(True)
        
        self.setFixedSize(600,300)

        self.logTextSplashScreen = ""

        self.setCommandText()

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.commandOutputLine)

    def setCommandText(self):
        self.commandOutputLine.setPlainText(self.logTextSplashScreen + \
                "* Internal Commands - Processed by RaspberryPi:\n" + self.intCommands + "\n" + \
                "* External Commands - Processed by Arduino:\n" + self.extCommands)



class graphWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
         # Set title
        self.setWindowTitle('Graph')

        # Set Size
        self.setGeometry(500, 500, 720, 420)

        self.graph = pyqtgraph.PlotWidget()
        self.setCentralWidget(self.graph)
        self.xs = []
        self.ys = []
        self.graph.setTitle("Title")
        self.graph.setLabel("left", "Y")
        self.graph.setLabel("bottom", "X")
        self.graph.plot(self.xs, self.ys)

    def addDataPoint(x,y):
        self.xs.append(x)
        self.ys.append(y)
        self.graph.setData(self.xs, self.ys)


class mainWindow(QWidget):

    ############ Constructor
    def __init__(self, *args, **kwargs):

        ##### UI
        super().__init__(*args, **kwargs)

        # Set title
        self.setWindowTitle('Raspberry Pi - Arduino Interface')

        # Set Size
        self.setGeometry(500, 500, 420, 220)

        # UI Elements - Buttons
        self.startButton = QPushButton('Run')
        self.startButton.clicked.connect(self.startCommand)
        self.stopButton = QPushButton('Interrupt')
        self.stopButton.clicked.connect(self.stopCommand)
        self.commandInfoButton = QPushButton('Commands')
        self.commandInfoButton.clicked.connect(self.infoCommand)
        self.commandInfoButton.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))
        self.graphButton = QPushButton('Graph')
        self.graphButton.clicked.connect(self.graphShow)
        self.graphButton.setIcon(self.style().standardIcon(QStyle.SP_FileDialogContentsView))

        # UI Elements - Pixmaps
        self.groupLogoPixmap = QPixmap('assets/logo.png')
        self.groupLogoPixmap = self.groupLogoPixmap.scaled(250, 250, Qt.KeepAspectRatio)

        # UI Elements - Labels
        self.commandInputLabel = QLabel('Command:')
        self.groupLogoLabel = QLabel()
        self.groupLogoLabel.setPixmap(self.groupLogoPixmap)

        # UI Elements - Line/Text Edits
        self.commandInputLine = QLineEdit()
        self.commandInputLine.returnPressed.connect(self.startCommand)
        self.commandOutputLine = QTextEdit()
        self.commandOutputLine.setReadOnly(True)
        self.commandOutputLine.setMinimumSize(400,250)
        self.logTextSplashScreen = "******************************\n* RPi - Arduino Interface (Log) *\n******************************\n\n"
        self.logText(self.logTextSplashScreen)

        # Create a layouts
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)

        # UI Elements - Top Layout 
        self.topLayout.addWidget(self.groupLogoLabel)
        self.topLayout.addWidget(self.commandOutputLine)
        
        # UI Elements - Main Layout
        self.mainLayout.addWidget(self.startButton)
        self.mainLayout.addWidget(self.stopButton)
        
        # UI Elements - Bottom Layout
        self.bottomLayout.addWidget(self.commandInputLabel)
        self.bottomLayout.addWidget(self.commandInputLine)
        self.bottomLayout.addWidget(self.commandInfoButton)
        self.bottomLayout.addWidget(self.graphButton)

        # Show window
        self.show()

        ##### COMMS
        # Create Serial Communications
        self.arduinoCommsObject = arduinoComms()
        self.logText(self.arduinoCommsObject.initialize())

        ##### INTERNAL COMMANDS
        self.intCommands = {
            "test_port": self.testPort,
            "change_port": self.changePort,
            "clear": self.logClear,
            "list_ports": self.listPorts
        }
        self.intCommandsDescription = "test_port: Tests communications through the selected port.\n" + \
            "change_port PORT_NAME: Changes the port to whatever the user provides.\n" + \
            "clear: Clears the console log.\n" + \
            "list_ports: Re-checks available ports and prints them on screen.\n"
        
        ##### External Commands
        self.extCommandsDescription = ""

        ##### Additional Windows
        self.infoWindow = commandWindow(self.intCommandsDescription, self.extCommandsDescription)
        self.graphWindow = graphWindow()


    ############ Close Window Event
    def closeEvent(self,event):
        self.graphWindow.close()
        self.infoWindow.close()
        event.accept()

    ############ Button Functions
    
    # 'Run' Button; used to parse and send commands
    def startCommand(self):

        # Extract the command from the input line
        cmd = self.commandInputLine.text()
        
        # Split the command into substrings
        cmdPartitions = cmd.split()
        
        # Extract Command Tag (first word)
        if len(cmd) > 0:
            cmdTag = cmdPartitions[0]
        else:
            cmdTag = ""
        
        # Command Extraction Variables
        cmdArgs = []
        cmdKwargs = {}
        keyKwarg = ""
        
        # Extract arguments from the command - place in cmgArgs and cmdKwargs
        if len(cmdPartitions) > 0:
            for string in cmdPartitions[1:]:
                if string[0] == "-":
                    if keyKwarg:
                        cmdKwargs[keyKwarg] = True
                        keyKwarg = ""
                    keyKwarg = string[1:]
                else:
                    if keyKwarg:
                        cmdKwargs[keyKwarg] = string
                        keyKwarg = ""
                    else:
                        cmdArgs.append(string)
            if keyKwarg:
                cmdKwargs[keyKwarg] = True
        
        # Parsing complete; Send command to its' rightful place.
        if cmdTag in self.intCommands.keys():
            # Run internal commands - processed by RPi
            self.logText("* Running internal command \'"+cmd+"\'\n")
            self.intCommands[cmdTag](*cmdArgs,**cmdKwargs)
        elif len(cmd) > 0:
            # Run external commands - processed by arduino
            self.logText("* Running external command \'"+cmd+"\'\n")
            self.logText(self.arduinoCommsObject.writeMessage(cmd))
            self.logText(self.arduinoCommsObject.readMessage())
    
    # 'Interrupt' Button; used to interrupt on-going processes in the RPi/Arduino
    def stopCommand(self):
        self.logText("* Interrupting...\n")
        self.arduinoCommsObject.writeString("stop") # CHANGE
    
    # Info icon button. Displays information on implemented commands.
    def infoCommand(self):
        self.arduinoCommsObject.writeMessage("request_commands")
        self.extCommandsDescription = self.arduinoCommsObject.readMessage()
        self.infoWindow.show()
        self.infoWindow.activateWindow()

    def graphShow(self):
        self.graphWindow.show()
        self.graphWindow.activateWindow()

    ############ Utility

    def logText(self,msg): 
        self.commandOutputLine.setPlainText(self.commandOutputLine.toPlainText() + msg)
        self.commandOutputLine.moveCursor(self.commandOutputLine.textCursor().End)

    ############ Internal Commands

    def logClear(self,*args,**kwargs):
        if args:
            self.logText("* ERROR: Unknown args in the clear function.\n")
        if kwargs:
            self.logText("* ERROR: Unknown kwargs in the clear function.\n")
        if (not args) and (not kwargs):
            self.commandOutputLine.setPlainText(self.logTextSplashScreen)
            self.commandOutputLine.moveCursor(self.commandOutputLine.textCursor().End)
        
    def testPort(self,*args,**kwargs):
        if args:
            self.logText("* ERROR: Unknown args in the test_port function.\n")
        if kwargs:
            self.logText("* ERROR: Unknown kwargs in the test_port function.\n")
        if not args and not kwargs:
            self.logText(self.arduinoCommsObject.tryOpeningIntToStr(self.arduinoCommsObject.tryOpening()))

    def listPorts(self,*args,**kwargs):
        if args:
            self.logText("* ERROR: Unknown args in the list_ports function.\n")
        if kwargs:
            self.logText("* ERROR: Unknown kwargs in the list_ports function.\n")
        if not args and not kwargs:
            self.logText(self.arduinoCommsObject.listPorts())

    def changePort(self,*args,**kwargs):
        if kwargs:
            self.logText("* ERROR: Unknown kwargs in the change_port function.\n")
        elif len(args) != 1:
            self.logText("* ERROR: change_port functions expects 1 argument!\n")
        else:
            self.logText(self.arduinoCommsObject.changePort(args[0]))
