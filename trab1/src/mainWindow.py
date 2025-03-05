##################### Python Library Imports
from PyQt5.QtCore import *      # Basic Qt functionalities.
from PyQt5.QtWidgets import *   # GUI windows
from PyQt5.QtCore import *      # Qt threads, ...
from PyQt5.QtGui import *       # GUI Elements
import pyqtgraph                # Data Visualization.
import re
import time                     # For routines

##################### User defined functions (imports)
from src.arduinoComms import arduinoComms
from src.commandWindow import commandWindow
from src.graphWindow import graphWindow
from src.inputConsole import inputConsole

##################### Main Programme Class

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
        self.commandInputLine = inputConsole('assets/input_log', self)
        self.commandInputLine.returnPressed.connect(self.startCommand)
        self.commandOutputLine = QTextEdit()
        self.commandOutputLine.setReadOnly(True)
        self.commandOutputLine.setMinimumSize(500,250)
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
            "list_ports": self.listPorts,
            "acquire_plot": self.acquirePlot,
            "set_titles": self.setTitles,
            "clear_graph": self.clearGraph
        }
        self.intCommandsDescription = "test_port: Tests communications through the selected port.\n" + \
            "change_port PORT_NAME: Changes the port to whatever the user provides.\n" + \
            "clear: Clears the console log.\n" + \
            "list_ports: Re-checks available ports and prints them on screen.\n" + \
            "acquire_plot: Acquire the number of points specified (after -n) with the time interval between each aquisition specified (after -t) and draw a graph.\n" + \
            "set_titles: Set the X axis title (specified after -x), Y axis title (specified after -y) and/or graph title (specified after -g).\n" + \
            "clear_graph: Clears all data in the graph.\n"
        
        ##### External Commands
        self.extCommandsDescription = ""

        ##### Additional Windows
        self.infoWindow = commandWindow(self.intCommandsDescription, self.extCommandsDescription)
        self.graphWindow = graphWindow()

        ##### INTERRUPTING
        self.interrupt = False


    ############# Events
    
    def closeEvent(self,event):
        self.interrupt = True
        time.sleep(0.1)
        self.arduinoCommsObject.closePort()
        self.graphWindow.close()
        self.infoWindow.close()
        self.commandInputLine.saveLog()
        event.accept()

    ############ Button Functions
    
    # 'Run' Button; used to parse and send commands
    def startCommand(self):
        # Uninterrupt for potential new thread routines.
        self.interrupt = False

        # Extract the command from the input line
        cmd = self.commandInputLine.text()

        # Clear command line input
        self.commandInputLine.clear()
        # Reset previous command log index
        self.commandInputLine.resetIndex()
        # Add new empty line to previous command log
        if cmd != "" and not cmd.isspace():
            self.commandInputLine.addLine()

        # Split the command into substrings
        expression = r'(?:[^\s"]|"(?:\\.|[^"\\])*")+'  # Match non-space characters or quoted parts
        cmdPartitions = re.findall(expression, cmd.strip())
        
        # Remove quotes from the quoted strings
        cmdPartitions = [part.strip('"') if part.startswith('"') and part.endswith('"') else part for part in cmdPartitions]

        # Extract Command Tag (first word)
        cmdTag = ""
        if cmdPartitions:
            cmdTag = cmdPartitions[0]
        # Command Extraction Variables
        cmdArgs = []
        cmdKwargs = {}
        keyKwarg = ""
        # Extract arguments from the command - place in cmgArgs and cmdKwargs
        if cmdPartitions:
            for string in cmdPartitions[1:]:
                if string.startswith('-'):
                    if keyKwarg:
                        cmdKwargs[keyKwarg] = True
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
        elif cmd:
            # Run external commands - processed by arduino
            self.logText("* Running external command \'"+cmd+"\'\n")
            self.logText(self.arduinoCommsObject.writeMessage(cmd))
            self.logText(">>> "+self.arduinoCommsObject.readMessage()+"\n")
    
    # 'Interrupt' Button; used to interrupt on-going processes in the RPi/Arduino
    def stopCommand(self):
        self.logText("* Interrupting...\n")
        self.interrupt = True
    
    # Info icon button. Displays information on implemented commands.
    def infoCommand(self):
        self.arduinoCommsObject.writeMessage("request_commands")
        self.extCommandsDescription = self.arduinoCommsObject.readMessage()
        self.infoWindow.updateExternalCommands(self.extCommandsDescription)
        self.infoWindow.show()
        self.infoWindow.activateWindow()

    def graphShow(self):
        self.graphWindow.show()
        self.graphWindow.activateWindow()

    ############ Utility

    def logText(self,msg): 
        self.commandOutputLine.setPlainText(self.commandOutputLine.toPlainText() + msg)
        self.commandOutputLine.moveCursor(self.commandOutputLine.textCursor().End)

    def addDataPoint(self,point):
        self.graphWindow.addDataPoint(point[0],point[1])

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

    def acquirePlot(self,*args,**kwargs):
        n_points = -1
        interval = 0
        clear = True
        if len(args) >0:
            self.logText("* ERROR: acquire_plot does not take regular arguments, only kwargs.\n")
        for tag in kwargs.keys():
            if tag not in ["t", "n", "c"]:
                return self.logText("* ERROR: unrecognised parameter in acquire_plot function\n")
            if tag == "t":
                interval = kwargs[tag]
            if tag == "n":
                n_points = kwargs[tag]
            if tag == "c":
                clear = False

        # clear previous graph
        if clear:
            self.logText("* Clearing Graph...\n")
            self.graphWindow.clearGraph()
        # set start time to 0
        self.logText("* Resetting Arduino Timer (set_pivot external command)...\n")
        self.arduinoCommsObject.writeMessage("set_pivot")
        self.logText(">>> "+self.arduinoCommsObject.readMessage())
        # start thread for aquisition
        self.logText("* Starting Acquisition Thread.\n")
        self.thread = internalCommandThread(self,'acquirePlotThread',[n_points,interval])
        self.thread.send_data.connect(self.addDataPoint)
        self.thread.start()
                   
    def setTitles(self, *args, **kwargs):
        if len(args) >0:
            self.logText("* ERROR: set_titles does not take regular arguments, only kwargs.\n")
        if len(kwargs) == 0:
            self.logText("* ERROR: Parameters missing in set_titles function\n")
        for tag in kwargs.keys():
            if tag not in ["x", "y", "g"]:
                return self.logText("* ERROR: Unrecognised parameter in set_titles function\n")
            if tag == "x":
                self.graphWindow.graphPlot.setLabel("bottom", kwargs["x"])
            if tag == "y":
                self.graphWindow.graphPlot.setLabel("left", kwargs["y"])
            if tag == "g":
                self.graphWindow.graphPlot.setTitle(kwargs["g"])

    def clearGraph(self, *args, **kwargs):
        if args:
            self.logText("* ERROR: Unknown args in the clear_graph function.\n")
        if kwargs:
            self.logText("* ERROR: Unknown kwargs in the clear_graph function.\n")
        if not args and not kwargs:
            self.graphWindow.clearGraph()

############ Internal Command Threading

    def acquirePlotThread(self,params,signal):
        counter = 0
        while counter != params[0] and self.interrupt == False:
            self.arduinoCommsObject.writeMessage("acquire")
            point = self.arduinoCommsObject.readMessage()
            list_point = point.split()
            # self.graphWindow.addDataPoint(float(list_point[0])*1e-3, float(list_point[1]))
            signal.emit( [float(list_point[0])*1e-3, float(list_point[1])] )
            time.sleep(float(params[1])*float(1e-3))
            counter += 1