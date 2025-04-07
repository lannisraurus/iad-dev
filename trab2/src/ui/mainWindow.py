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
from src.Tracker import Tracker
from src.ui.stepperConfigWindow import stepperConfigWindow
from src.ui.deviceConfigWindow import deviceConfigWindow
from src.ui.othersConfigWindow import othersConfigWindow
from src.utils.commandThread import CommandThread

##################### Main Programme Class
class mainWindow(QWidget):

    ############ Constructor
    def __init__(self, *args, **kwargs):

        ############################# UI

        super().__init__(*args, **kwargs)   # Initialize parent class

        # UI - General
        self.setFixedSize(1280,660)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('Astrolocator')
        self.setWindowIcon(QIcon('assets/logo.png'))

        # UI Elements - Buttons

        self.closeButton = QPushButton("X")
        self.closeButton.setFixedSize(30, 20)
        self.closeButton.setStyleSheet(
            "font-weight: bold; border: none;"
        )
        self.closeButton.clicked.connect(self.close)

        self.alignmentBeginButton = QPushButton('Begin Alignment')
        self.alignmentBeginButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.alignmentBeginButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogYesButton))

        self.alignmentUp = QPushButton('')
        self.alignmentUp.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowUp))
        self.alignmentUp.setFixedSize(36, 28)
        self.alignmentDown = QPushButton('')
        self.alignmentDown.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown))
        self.alignmentDown.setFixedSize(36, 28)
        self.laserButton = QPushButton('')
        self.laserButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogNoButton))
        self.laserButton.setFixedSize(36, 28)
        
        self.alignmentLeft = QPushButton('')
        self.alignmentLeft.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack))
        self.alignmentLeft.setFixedSize(36, 28)
        self.alignmentRight = QPushButton('')
        self.alignmentRight.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward))
        self.alignmentRight.setFixedSize(36, 28)

        self.trackBeginButton = QPushButton('Begin Tracking')
        self.trackBeginButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.trackBeginButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView))
        self.trackBeginButton.clicked.connect(self.beginStopTracking)

        self.settingsSteppersButton = QPushButton('Configure Steppers')
        self.settingsSteppersButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.settingsSteppersButton.clicked.connect(self.stepperConfigWindowShow)
        
        self.settingsDeviceButton = QPushButton('Configure Acquisition Device')
        self.settingsDeviceButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.settingsDeviceButton.clicked.connect(self.deviceConfigWindowShow)
        
        self.settingsOthersButton = QPushButton('Configure Other Periferals')
        self.settingsOthersButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.settingsOthersButton.clicked.connect(self.othersConfigWindowShow)

        # UI Elements - Sliders
        self.alignmentDelaySlider = QSlider(Qt.Horizontal, self)
        self.alignmentDelaySlider.setMaximum(1000)
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
        self.trackLabel = QLabel('Tracking / Data Acquisition:')
        self.trackLabel.setFixedWidth(200)
        self.settingsLabel = QLabel('Settings:')
        self.settingsLabel.setFixedWidth(200)
        self.alignmentDelayValueLabel = QLabel('hi!')
        self.updateDelayValue()
        self.alignmentDelayValueLabel.setFixedWidth(90)
        self.alignmentAngles = QLabel('(az= , alt= )')
        self.trackDevicesLabel = QLabel('Acquisition Device:')

        # UI Elements - Line Edits
        self.commandOutputLine = QTextEdit()
        self.commandOutputLine.setReadOnly(True)
        self.commandOutputLine.setFixedHeight(400)
        self.commandOutputLine.setMinimumWidth(500)
        self.logText("----- Astrolocator (Log) -----\n\n")
        self.logText("> Welcome to Astrolocator, a RPi application made for interfacing with astrolocation devices! Make sure to align your system before tracking objects. Enjoy!\n")
        self.logText("> Duarte Tavares, João Camacho, Jorge Costa, Margarida Saraiva (IST, 2025 - IAD)\n\n")

        self.commandInputLine = inputConsole('assets/input_log', self)
        self.commandInputLine.returnPressed.connect(self.sendText)

        # UI Elements - Dropdowns
        self.alignmentDropdown = QComboBox()
        self.alignmentDropdown.addItems(['1 Point','3 Point'])
        self.alignmentDropdown.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.trackDeviceDropdown = QComboBox()
        self.trackDeviceDropdown.addItems(['Telescope','Satellite Antena'])
        self.trackDeviceDropdown.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.steppersDropdown = QComboBox()
        self.steppersDropdown.addItems(['RB-Moto2 (Joy-IT)'])
        self.cameraDropdown = QComboBox() # read devices in rpi
        self.antennaDropdown = QComboBox() # read devices in rpi

        # UI - Spacers
        self.spacer1 = QSpacerItem(40, 20, QSizePolicy.Minimum,QSizePolicy.Expanding)

        # Create a layouts
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.closeButton, alignment=Qt.AlignTop | Qt.AlignRight)
        
        self.topLayout = QHBoxLayout()
        self.midLayout = QHBoxLayout()
        self.bottomLayout = QVBoxLayout()

        self.alignmentLayout = QHBoxLayout()
        self.trackLayout = QHBoxLayout()
        self.settingsLayout = QHBoxLayout()
        
        self.alignmentLayoutR = QHBoxLayout()
        self.trackLayoutR = QHBoxLayout()
        self.settingsLayoutR = QHBoxLayout()

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
        self.topLayout.setAlignment(Qt.AlignTop)
        
        # UI Elements - Mid Layout
        self.midLayout.addWidget(self.inputCommandLabel)
        self.midLayout.addWidget(self.commandInputLine)
        self.midLayout.setAlignment(Qt.AlignTop)

        # UI Elements - Bottom Layout
        self.bottomLayout.addLayout(self.alignmentLayout)
        self.bottomLayout.addLayout(self.trackLayout)
        self.bottomLayout.addLayout(self.settingsLayout)
        self.bottomLayout.setAlignment(Qt.AlignTop)

        # UI Elements - Other Layouts
        self.alignmentLayout.addWidget(self.alignmentLabel, alignment=Qt.AlignTop | Qt.AlignLeft)

        self.alignmentLayout.addLayout(self.alignmentLayoutR)

        self.alignmentLayoutR.addLayout(self.alignmentLayoutRL)
        self.alignmentLayoutR.addItem(self.spacer1)
        self.alignmentLayoutR.addLayout(self.alignmentLayoutRR)
        self.alignmentLayoutR.addItem(self.spacer1)

        self.alignmentLayoutRR.addLayout(self.alignmentLayoutR1)
        self.alignmentLayoutRR.addLayout(self.alignmentLayoutR2)
        self.alignmentLayoutRR.addLayout(self.alignmentLayoutR3)

        self.alignmentLayoutRL.addLayout(self.alignmentLayoutR4)
        self.alignmentLayoutR4.addWidget(self.alignmentTypeLabel)
        self.alignmentLayoutR4.addWidget(self.alignmentDropdown)
        self.alignmentLayoutRL.addLayout(self.alignmentLayoutR5)
        self.alignmentLayoutR5.addWidget(self.alignmentDelayLabel)
        self.alignmentLayoutR5.addWidget(self.alignmentDelaySlider)
        self.alignmentLayoutR5.addWidget(self.alignmentDelayValueLabel)
        self.alignmentLayoutRL.addLayout(self.alignmentLayoutR6)
        self.alignmentLayoutR6.addWidget(self.alignmentBeginButton)
        self.alignmentLayoutR6.addWidget(self.alignmentAngles)

        self.alignmentLayoutR1.addWidget(self.alignmentUp, alignment= Qt.AlignTop)
        self.alignmentLayoutR2.addWidget(self.alignmentLeft, alignment= Qt.AlignTop)
        self.alignmentLayoutR2.addWidget(self.laserButton, alignment= Qt.AlignTop)
        self.alignmentLayoutR2.addWidget(self.alignmentRight, alignment= Qt.AlignTop)
        self.alignmentLayoutR3.addWidget(self.alignmentDown, alignment= Qt.AlignTop)

        self.alignmentLayout.setAlignment(Qt.AlignTop)
        self.alignmentLayoutR.setAlignment(Qt.AlignTop)
        self.alignmentLayoutRL.setAlignment(Qt.AlignTop)
        self.alignmentLayoutRR.setAlignment(Qt.AlignTop)

        self.trackLayout.addWidget(self.trackLabel, alignment= Qt.AlignTop | Qt.AlignLeft)
        self.trackLayout.addLayout(self.trackLayoutR)
        
        self.trackLayoutR.addWidget(self.trackBeginButton)
        self.trackLayoutR.addWidget(self.trackDevicesLabel)
        self.trackLayoutR.addWidget(self.trackDeviceDropdown)
        
        self.trackLayout.setAlignment(Qt.AlignTop)
        self.trackLayoutR.setAlignment(Qt.AlignTop)

        self.settingsLayout.addWidget(self.settingsLabel, alignment= Qt.AlignTop | Qt.AlignLeft)
        self.settingsLayout.addLayout(self.settingsLayoutR)

        self.settingsLayoutR.addWidget(self.settingsSteppersButton)
        self.settingsLayoutR.addWidget(self.settingsDeviceButton)
        self.settingsLayoutR.addWidget(self.settingsOthersButton)

        self.settingsLayout.setAlignment(Qt.AlignTop)
        self.settingsLayoutR.setAlignment(Qt.AlignTop)
        
        # Show window
        self.show()

        ############################ TECHNICAL

        # Load Stepper Configuration
        self.stepperConfigWindow = stepperConfigWindow(self)
        self.stepperController = None
        self.updateStepperController()

        # Device Configuration
        self.deviceConfigWindow = deviceConfigWindow()

        # Other Configurations
        self.othersConfigWindow = othersConfigWindow(self)
        self.laserButton.clicked.connect(self.othersConfigWindow.laser)

        # Movement Buttons Connect
        self.alignmentUp.pressed.connect(self.stepperUpPress)
        self.alignmentDown.pressed.connect(self.stepperDownPress)
        self.alignmentLeft.pressed.connect(self.stepperLeftPress)
        self.alignmentRight.pressed.connect(self.stepperRightPress)
        self.alignmentUp.released.connect(self.stepperUpRelease)
        self.alignmentDown.released.connect(self.stepperDownRelease)
        self.alignmentLeft.released.connect(self.stepperLeftRelease)
        self.alignmentRight.released.connect(self.stepperRightRelease)
        
        # getInput
        self.waitingForText = False
        self.inputtedText = ""
        self.receiverForText = None

        # Tracking
        self.tracking = False
        self.tracker = Tracker(self.stepperController)#None
        self.requestPosition()


    ############# Events
    
    def closeEvent(self,event):
        self.commandInputLine.saveLog()
        self.stepperConfigWindow.close()
        self.deviceConfigWindow.close()
        self.othersConfigWindow.close()
        event.accept()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def paintEvent(self, event):
        # Draw the custom border around the window
        painter = QPainter(self)
        pen = QPen(QColor(170, 170, 170))  # Light gray color for the border
        pen.setWidth(2)  # Set border thickness
        painter.setPen(pen)
        painter.setBrush(Qt.transparent)
        
        # Draw the border around the window (excluding the title bar area)
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

    ############ Button Methods

    def stepperConfigWindowShow(self):
        self.stepperConfigWindow.show()
        self.stepperConfigWindow.activateWindow()
    
    def deviceConfigWindowShow(self):
        self.deviceConfigWindow.show()
        self.deviceConfigWindow.activateWindow()

    def othersConfigWindowShow(self):
        self.othersConfigWindow.show()
        self.othersConfigWindow.activateWindow()

    ############ Utility

    # Logs text onto the programme log window.
    def logText(self,msg): 
        self.commandOutputLine.setPlainText(self.commandOutputLine.toPlainText() + msg)
        self.commandOutputLine.moveCursor(self.commandOutputLine.textCursor().End)

    def sendText(self):
        if self.waitingForText:
            self.inputtedText = self.commandInputLine.text()
            self.waitingForText = False
            self.receiverForText()

    # Update the delay value from the slider
    def updateDelayValue(self):
        self.alignmentDelayValueLabel.setText('Value: '+str(self.alignmentDelaySlider.value())+' ms')
    
    # Load Stepper Settings onto StepperController object
    def updateStepperController(self):
        self.stepperController = StepperController(self.stepperConfigWindow.getSettings(), self)
    
    ######################### MANUAL STEPPER CONTROL

    def stepperUpPress(self):
        print('a')
    
    def stepperUpRelease(self):
        print('a')

    def stepperDownPress(self):
        print('a')
    
    def stepperDownRelease(self):
        print('a')
    
    def stepperLeftPress(self):
        print('a')
    
    def stepperLeftRelease(self):
        print('a')
    
    def stepperRightPress(self):
        print('a')
    
    def stepperRightRelease(self):
        print('a')




    #def stepperUpThread(self):
        print('a')
        #while True:
        #    self.stepperController.moveToAz

    def stepperDownThread(self):
        print('a')

    def stepperLeftThread(self):
        print('a')

    def stepperRightThread(self):
        print('a')

    ######################### INTERACTION WITH OTHER CLASSES FOR ALIGNMENT ROUTINE
    
    def readCoords(self):
        input = self.inputCommandLabel.text()


    def requestPosition(self):
        self.logText("> Please insert your current coordinates in the following format (enter to ignore): latitude longitude altitude  \n")
        self.waitingForText = True
        self.receiverForText = self.setTracker

    def setTracker(self):
        text = self.inputtedText
        if text == "":
            self.tracker = Tracker(self.stepperController)
            return
        coords = text.split(" ")
        if len(coords) != 3:
            self.logText("> ERROR: Invalid coordinates, please follow the requested format.\n")
            self.requestPosition()
            return        
        self.tracker = Tracker(self.stepperController, coords[0], coords[1], coords[2])
        self.logText(f"> Initialized with latitude: {coords[0]}, longitude: {coords[1]}, altitude: {coords[2]}\n\n")


    def alignmentRoutine(self):
        if self.alignmentDropdown.currentIndex() == 0:
            self.tracker.nearestOnePointAlign()
            
        
    def beginStopTracking(self):
        if self.tracking:
            self.logText("* Ending Tracking Threads.\n")
            self.tracker.stopTracking = True

            self.tracking = False
            self.waitingForText = False
            return
            
        self.tracking = True
        self.logText("> Please input object name\n")
        self.waitingForText = True
        self.receiverForText = self.beginTrackingThreads


    def beginTrackingThreads(self):
        objName = self.inputtedText
        
        # start thread for motor tracking
        self.logText("* Starting Motor Tracking Thread.\n")
        self.threadMotor = CommandThread(self.tracker.trackingRoutine,[objName])
        self.threadMotor.start()
        time.sleep(100)
        # start thread for aquisition
        self.logText("* Starting Acquisition Thread.\n")
        self.thread = CommandThread(self,'acquirePlotThread',[n_points,interval,x_multiplier,y_multipler])
        self.thread.send_data.connect(self.addDataPoint)
        self.thread.start()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    ############ COMANDOS MAGABIBA 1 SESSÃO
    #
    #def location(self, *args, **kwargs):
    #    # O user mete a sua localização
    #    if args:
    #        return self.logText("* ERROR: location function does not take regular arguments, only kwargs.\n")
    #    if len(kwargs)==0:
    #        return self.logText("* ERROR: location function must take kwargs.\n")
    #    for tag in kwargs.keys():
    #        if tag not in ["lat", "long", "alt"]:
    #            return self.logText("* ERROR: unrecognised parameter in location function\n")
    #        if (tag == "lat" and kwargs[tag] != "" and kwargs[tag] != True):
    #            self.latitude = kwargs[tag]
    #        if (tag == "long" and kwargs[tag] != "" and kwargs[tag] != True):
    #            self.longitude = kwargs[tag]
    #        if (tag == "alt" and kwargs[tag] != "" and kwargs[tag] != True):
    #            self.altitude = kwargs[tag]
    #    if self.latitude == "":
    #        self.logText("* WARNING: Latitude missing.\n")
    #    if self.longitude == "":
    #        self.logText("* WARNING: Longitude missing.\n")
    #    if self.altitude == "":
    #        self.logText("* WARNING: Altitude missing.\n")
    #    #FALTA METER UMA FUNÇÃO QUE DEPOIS ENVIE A INFORMAÇÃO DA LOCALIZAÇÃO PARA A CLASSE RESPETIVA

    #def request_location(self, *args, **kwargs):
    #    # O user pede a localização que a antena conhece
    #    if args:
    #        return self.logText("* ERROR: Unknown args in the request_location function.\n")
    #    if kwargs:
    #        return self.logText("* ERROR: Unknown kwargs in the request_location function.\n")            
    #    if (self.latitude == "" and self.longitude == "" and self.altitude == ""):
    #        return self.logText("* No location has been provided.\n")
    #    return self.logText("*LOCATION: \n*Latitude: " + self.latitude + "\n*Longitude: " + self.longitude + "\n*Altitude:" + self.altitude + "\n")
