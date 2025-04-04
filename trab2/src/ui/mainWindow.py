"""
Duarte Tavares, João Camacho, Jorge Costa, Margarida Saraiva
IST, 2025 - IAD

This file contains the main window class, containing all the UI
and programme methods.

"""
##################### Python Library Imports
from PyQt5.QtCore import *      # Basic Qt functionalities.
from PyQt5.QtWidgets import *   # GUI windows
from PyQt5.QtCore import *      # Qt threads, ...
from PyQt5.QtGui import *       # GUI Elements
import time                     # For routines

##################### User defined functions (imports)
from src.ui.inputConsole import inputConsole
from src.Astrolocator import Astrolocator
from src.StepperController import StepperController

##################### Main Programme Class
class mainWindow(QWidget):

    ############ Constructor
    def __init__(self, *args, **kwargs):

        ##### UI

        super().__init__(*args, **kwargs)   # Initialize parent class

        # UI - General
        self.setWindowTitle('Astrolocator')

        # UI Elements - Buttons
        self.alignmentBeginButton = QPushButton('Begin Alignment')
        self.alignmentBeginButton.setFixedWidth(364)
        self.alignmentUp = QPushButton('')
        self.alignmentUp.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowUp))
        self.alignmentUp.setFixedSize(36, 28)
        self.alignmentDown = QPushButton('')
        self.alignmentDown.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown))
        self.alignmentDown.setFixedSize(36, 28)
        self.alignmentLeft = QPushButton('')
        self.alignmentLeft.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack))
        self.alignmentLeft.setFixedSize(36, 28)
        self.alignmentRight = QPushButton('')
        self.alignmentRight.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward))
        self.alignmentRight.setFixedSize(36, 28)

        # UI Elements - Sliders
        self.alignmentDelaySlider = QSlider(Qt.Horizontal, self)
        self.alignmentDelaySlider.setFixedWidth(290)
        self.alignmentDelaySlider.setMaximum(100)
        self.alignmentDelaySlider.setMinimum(1)
        self.alignmentDelaySlider.valueChanged.connect(self.updateDelayValue)

        # UI Elements - Pixmaps
        self.groupLogoPixmap = QPixmap('assets/logo.png')
        self.groupLogoPixmap = self.groupLogoPixmap.scaled(400, 400, Qt.KeepAspectRatio)

        # UI Elements - Labels
        self.groupLogoLabel = QLabel()
        self.groupLogoLabel.setPixmap(self.groupLogoPixmap)
        self.inputCommandLabel = QLabel('User Input:')
        self.alignmentLabel = QLabel('Alignment / Movement:')
        self.alignmentLabel.setFixedWidth(200)
        self.alignmentDelayLabel = QLabel('Movement Delay:')
        self.alignmentTypeLabel = QLabel('Alignment Type:')
        self.alignmentTypeLabel.setFixedWidth(100)
        self.trackLabel = QLabel('Tracking / Data Acquisition:')
        self.trackLabel.setFixedWidth(200)
        self.settingsLabel = QLabel('Settings:')
        self.settingsLabel.setFixedWidth(200)
        self.alignmentDelayValueLabel = QLabel('hi!')
        self.updateDelayValue()
        self.alignmentAngles = QLabel('Angles = (az= , alt= )')

        # UI Elements - Line Edits
        self.commandOutputLine = QTextEdit()
        self.commandOutputLine.setReadOnly(True)
        self.commandOutputLine.setMinimumSize(500,400)
        self.logText("******************************\n*               Astrolocator (Log)               *\n******************************\n\n")
        self.logText("> Welcome to Astrolocator, a RPi application made for interfacing with astrolocation devices! Make sure to align your system before tracking objects. Enjoy!\n")
        self.logText("> Duarte Tavares, João Camacho, Jorge Costa, Margarida Saraiva (IST, 2025 - IAD)\n\n")

        self.commandInputLine = inputConsole('assets/input_log', self)
        #self.commandInputLine.returnPressed.connect(self.startCommand)

        # UI Elements - Dropdowns
        self.alignmentDropdown = QComboBox()
        self.alignmentDropdown.addItems(['1 Point','3 Point'])
        self.alignmentDropdown.setFixedWidth(350)
        self.trackDeviceDropdown = QComboBox()
        self.trackDeviceDropdown.addItems(['Telescope','Satellite Antena'])
        self.steppersDropdown = QComboBox()
        self.steppersDropdown.addItems(['RB-Moto2 (Joy-IT)'])
        self.cameraDropdown = QComboBox() # read devices in rpi
        self.antennaDropdown = QComboBox() # read devices in rpi

        # Create a layouts
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        
        self.topLayout = QHBoxLayout()
        self.midLayout = QHBoxLayout()
        self.bottomLayout = QVBoxLayout()

        self.alignmentLayout = QHBoxLayout()
        self.trackLayout = QHBoxLayout()
        self.settingsLayout = QHBoxLayout()
        
        self.alignmentLayoutR = QHBoxLayout()
        self.trackLayoutR = QVBoxLayout()
        self.settingsLayoutR = QVBoxLayout()

        self.alignmentLayoutRL = QVBoxLayout()
        self.alignmentLayoutRR = QVBoxLayout()

        self.alignmentLayoutR1 = QHBoxLayout()
        self.alignmentLayoutR2 = QHBoxLayout()
        self.alignmentLayoutR3 = QHBoxLayout()
        self.alignmentLayoutR2.setSpacing(32)

        self.alignmentLayoutR4 = QHBoxLayout()
        self.alignmentLayoutR5 = QHBoxLayout()
        self.alignmentLayoutR6 = QHBoxLayout()
        
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.midLayout)
        self.mainLayout.addLayout(self.bottomLayout)

        # UI Elements - Top Layout 
        self.topLayout.addWidget(self.groupLogoLabel)
        self.topLayout.addWidget(self.commandOutputLine)
        
        # UI Elements - Mid Layout
        self.midLayout.addWidget(self.inputCommandLabel)
        self.midLayout.addWidget(self.commandInputLine)

        # UI Elements - Bottom Layout
        self.bottomLayout.addLayout(self.alignmentLayout)
        self.bottomLayout.addLayout(self.trackLayout)
        self.bottomLayout.addLayout(self.settingsLayout)

        # UI Elements - Other Layouts
        self.alignmentLayout.addWidget(self.alignmentLabel, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.trackLayout.addWidget(self.trackLabel, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.settingsLayout.addWidget(self.settingsLabel, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.alignmentLayout.addLayout(self.alignmentLayoutR)
        self.trackLayout.addLayout(self.trackLayoutR)
        self.settingsLayout.addLayout(self.settingsLayoutR)

        self.alignmentLayoutR.addLayout(self.alignmentLayoutRL)
        self.alignmentLayoutR.addLayout(self.alignmentLayoutRR)

        self.alignmentLayoutRR.addLayout(self.alignmentLayoutR1)
        self.alignmentLayoutRR.addLayout(self.alignmentLayoutR2)
        self.alignmentLayoutRR.addLayout(self.alignmentLayoutR3)

        self.alignmentLayoutRL.addLayout(self.alignmentLayoutR4)
        self.alignmentLayoutR4.addWidget(self.alignmentTypeLabel, alignment=Qt.AlignmentFlag.AlignLeft)
        self.alignmentLayoutR4.addWidget(self.alignmentDropdown, alignment=Qt.AlignmentFlag.AlignLeft)
        self.alignmentLayoutRL.addLayout(self.alignmentLayoutR5)
        self.alignmentLayoutR5.addWidget(self.alignmentDelayLabel, alignment=Qt.AlignmentFlag.AlignLeft)
        self.alignmentLayoutR5.addWidget(self.alignmentDelaySlider, alignment=Qt.AlignmentFlag.AlignLeft)
        self.alignmentLayoutR5.addWidget(self.alignmentDelayValueLabel, alignment=Qt.AlignmentFlag.AlignLeft)
        self.alignmentLayoutRL.addLayout(self.alignmentLayoutR6)
        self.alignmentLayoutR6.addWidget(self.alignmentBeginButton, alignment=Qt.AlignmentFlag.AlignLeft)
        self.alignmentLayoutR6.addWidget(self.alignmentAngles, alignment=Qt.AlignmentFlag.AlignLeft)

        

        self.alignmentLayoutR1.addWidget(self.alignmentUp)
        self.alignmentLayoutR2.addWidget(self.alignmentLeft, alignment=Qt.AlignmentFlag.AlignRight)
        self.alignmentLayoutR2.addWidget(self.alignmentRight, alignment=Qt.AlignmentFlag.AlignLeft)
        self.alignmentLayoutR3.addWidget(self.alignmentDown)
        

        # Show window
        self.show()

    ############# Events
    def closeEvent(self,event):
        self.interrupt = True
        time.sleep(0.1)
        #self.arduinoCommsObject.closePort()
        event.accept()

    ############ Button Methods
    
    ############ Utility

    # Logs text onto the programme log window.
    def logText(self,msg): 
        self.commandOutputLine.setPlainText(self.commandOutputLine.toPlainText() + msg)
        self.commandOutputLine.moveCursor(self.commandOutputLine.textCursor().End)

    # Update the delay value from the slider
    def updateDelayValue(self):
        self.alignmentDelayValueLabel.setText('Value: '+str(self.alignmentDelaySlider.value())+' ms')

    ############ Internal Commands - Routines processed by this programme.
    
    def location(self, *args, **kwargs):
        # O user mete a sua localização
        if args:
            return self.logText("* ERROR: location function does not take regular arguments, only kwargs.\n")
        if len(kwargs)==0:
            return self.logText("* ERROR: location function must take kwargs.\n")
        for tag in kwargs.keys():
            if tag not in ["lat", "long", "alt"]:
                return self.logText("* ERROR: unrecognised parameter in location function\n")
            if (tag == "lat" and kwargs[tag] != "" and kwargs[tag] != True):
                self.latitude = kwargs[tag]
            if (tag == "long" and kwargs[tag] != "" and kwargs[tag] != True):
                self.longitude = kwargs[tag]
            if (tag == "alt" and kwargs[tag] != "" and kwargs[tag] != True):
                self.altitude = kwargs[tag]
        if self.latitude == "":
            self.logText("* WARNING: Latitude missing.\n")
        if self.longitude == "":
            self.logText("* WARNING: Longitude missing.\n")
        if self.altitude == "":
            self.logText("* WARNING: Altitude missing.\n")
        #FALTA METER UMA FUNÇÃO QUE DEPOIS ENVIE A INFORMAÇÃO DA LOCALIZAÇÃO PARA A CLASSE RESPETIVA

    def request_location(self, *args, **kwargs):
        # O user pede a localização que a antena conhece
        if args:
            return self.logText("* ERROR: Unknown args in the request_location function.\n")
        if kwargs:
            return self.logText("* ERROR: Unknown kwargs in the request_location function.\n")            
        if (self.latitude == "" and self.longitude == "" and self.altitude == ""):
            return self.logText("* No location has been provided.\n")
        return self.logText("*LOCATION: \n*Latitude: " + self.latitude + "\n*Longitude: " + self.longitude + "\n*Altitude:" + self.altitude + "\n")
