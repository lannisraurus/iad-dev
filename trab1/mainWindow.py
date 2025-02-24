##################### Python Library Imports

# UI
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
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

class mainWindow(QWidget):

    # Constructor
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Set title
        self.setWindowTitle('IAD - Project I (Group I)')

        # Set Size
        self.setGeometry(500, 500, 420, 220)

        # UI Elements - Buttons
        self.startButton = QPushButton('Run')
        self.startButton.clicked.connect(self.startCommand)
        self.stopButton = QPushButton('Interrupt')
        self.stopButton.clicked.connect(self.stopCommand)
        self.commandInfoButton = QPushButton('')
        self.commandInfoButton.clicked.connect(self.infoCommand)
        self.commandInfoButton.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))

        # UI Elements - Pixmaps
        self.groupLogoPixmap = QPixmap('assets/logo.png')
        self.groupLogoPixmap = self.groupLogoPixmap.scaled(250, 250, Qt.KeepAspectRatio)

        # UI Elements - Labels
        self.commandInputLabel = QLabel('Command:')
        self.groupLogoLabel = QLabel()
        self.groupLogoLabel.setPixmap(self.groupLogoPixmap)

        # UI Elements - Line/Text Edits
        self.commandInputLine = QLineEdit()
        self.commandOutputLine = QTextEdit()
        self.commandOutputLine.setReadOnly(True)
        self.commandOutputLine.setMinimumSize(400,250)
        self.logText("*****************************\n")
        self.logText("RPi - Arduino Interface (Log)\n")
        self.logText("*****************************\n\n")

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
        
        # Show window
        self.show()

        # Create Serial Communications
        self.arduinoCommsObject = arduinoComms()
        self.logText(self.arduinoCommsObject.initialize())

    
    # UI functions
    def logText(self,msg): 
        self.commandOutputLine.setPlainText(self.commandOutputLine.toPlainText() + msg)
        self.commandOutputLine.moveCursor(self.commandOutputLine.textCursor().End)

    def startCommand(self):
        self.logText("* Running...\n")

    def stopCommand(self):
        self.logText("* Interrupting...\n")

    def infoCommand(self):
        self.logText("* Opening Info Window.\n")

