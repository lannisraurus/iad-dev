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

##################### User defined functions (imports)
from src.ui.inputConsole import inputConsole                # User input
from src.Astrolocator import Astrolocator                   # Locating astronomical objects
from src.StepperController import StepperController         # Manipulating Stepper Motors
from src.Tracker import Tracker                             # Coordinating StepperController with Astrolocator
from src.ui.stepperConfigWindow import stepperConfigWindow  # Configuration window for steppers
from src.ui.deviceConfigWindow import deviceConfigWindow    # Configuration window for acquisition devices
from src.ui.othersConfigWindow import othersConfigWindow    # Configuration window for other periferals
from src.ui.locationConfigWindow import locationConfigWindow    # Configuration window for location
from src.ui.graphWindow import graphWindow                  # For data visualization
from src.utils.commandThread import CommandThread           # For multithreading routines
from src.Camera import RPiCamera2

##################### Main Programme Class
class mainWindow(QWidget):

    ############ Constructor
    def __init__(self, *args, **kwargs):

        ############################# UI

        super().__init__(*args, **kwargs)   # Initialize parent class

        # UI - General
        self.setFixedSize(1280,680)
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
        self.alignmentBeginButton.clicked.connect(self.alignmentRoutine1)

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
        self.trackBeginButton.clicked.connect(self.beginStopTracking1)

        self.settingsSteppersButton = QPushButton('Steppers')
        self.settingsSteppersButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.settingsSteppersButton.clicked.connect(self.stepperConfigWindowShow)
        
        #self.settingsDeviceButton = QPushButton('Acquisition Device')
        #self.settingsDeviceButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        #self.settingsDeviceButton.clicked.connect(self.deviceConfigWindowShow)
        
        self.settingsOthersButton = QPushButton('Other Periferals')
        self.settingsOthersButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.settingsOthersButton.clicked.connect(self.othersConfigWindowShow)

        self.settingsLocationButton = QPushButton('Location Settings')
        self.settingsLocationButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.settingsLocationButton.clicked.connect(self.locationConfigWindowShow)

        self.cameraButton = QPushButton('Camera')
        self.cameraButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.cameraButton.clicked.connect(self.cameraStart)

        self.antennaButton = QPushButton('Antenna')
        self.antennaButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # UI Elements - Sliders
        self.alignmentDelaySlider = QSlider(Qt.Horizontal, self)
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
        self.trackLabel = QLabel('Tracking / Data Acquisition:')
        self.trackLabel.setFixedWidth(200)
        self.settingsLabel = QLabel('Settings:')
        self.settingsLabel.setFixedWidth(200)
        self.alignmentDelayValueLabel = QLabel('hi!')
        self.updateDelayValue()
        self.alignmentDelayValueLabel.setFixedWidth(120)
        self.alignmentAngles = QLabel('(az=ERR , alt=ERR )')
        self.trackDevicesLabel = QLabel('Acquisition Devices:')

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
        self.alignmentDropdown.addItems(['1 Point','N Point'])
        self.alignmentDropdown.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        #self.trackDeviceDropdown = QComboBox()
        #self.trackDeviceDropdown.addItems(['Telescope','Satellite Antena'])
        #self.trackDeviceDropdown.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.steppersDropdown = QComboBox()
        self.steppersDropdown.addItems(['RB-Moto2 (Joy-IT)'])
        self.cameraDropdown = QComboBox() # read devices in rpi
        self.antennaDropdown = QComboBox() # read devices in rpi

        # UI - Spacers
        self.spacer1 = QSpacerItem(40, 20, QSizePolicy.Minimum,QSizePolicy.Expanding)

        # UI - Angle lock
        #self.fixedAnglesLabel = QLabel('Lock Rotation:')
        self.fixedAnglesButton = QPushButton('Limit Stepper Angles')
        self.fixedAnglesButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.fixedAnglesButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical))
        self.fixedAnglesButton.clicked.connect(self.angleLock1)

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
        #self.alignmentLayoutR2.setSpacing(32)

        self.alignmentLayoutR4 = QHBoxLayout()
        self.alignmentLayoutR5 = QHBoxLayout()
        self.alignmentLayoutR6 = QHBoxLayout()
        #self.alignmentLayoutR7 = QHBoxLayout()
        
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
        #self.alignmentLayoutRL.addLayout(self.alignmentLayoutR7)
        #self.alignmentLayoutR6.addWidget(self.fixedAnglesLabel)
        self.alignmentLayoutR6.addWidget(self.fixedAnglesButton)
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
        #self.trackLayoutR.addWidget(self.trackDeviceDropdown)
        self.trackLayoutR.addWidget(self.cameraButton)
        self.trackLayoutR.addWidget(self.antennaButton)
        
        self.trackLayout.setAlignment(Qt.AlignTop)
        self.trackLayoutR.setAlignment(Qt.AlignTop)

        self.settingsLayout.addWidget(self.settingsLabel, alignment= Qt.AlignTop | Qt.AlignLeft)
        self.settingsLayout.addLayout(self.settingsLayoutR)

        self.settingsLayoutR.addWidget(self.settingsSteppersButton)
        #self.settingsLayoutR.addWidget(self.settingsDeviceButton)
        self.settingsLayoutR.addWidget(self.settingsOthersButton)
        self.settingsLayoutR.addWidget(self.settingsLocationButton)

        self.settingsLayout.setAlignment(Qt.AlignTop)
        self.settingsLayoutR.setAlignment(Qt.AlignTop)
        
        # Show window
        self.show()

        ############################ TECHNICAL FUNCTIONALITIES

        # Dragging window
        self.dragging = False

        # Load Stepper Configuration
        self.stepperConfigWindow = stepperConfigWindow(self)
        self.stepperController = None
        self.updateStepperController()  # Creates stepperController from settings window.

        # Device Configuration
        self.deviceConfigWindow = deviceConfigWindow()

        # Location Configuration
        self.locationConfigWindow = locationConfigWindow(self)

        # Other Configurations for periferals (example: laser)
        self.othersConfigWindow = othersConfigWindow(self)
        self.laserButton.clicked.connect(self.othersConfigWindow.laserToggle)

        # Movement Buttons Connect - Steppers
        self.alignmentUp.pressed.connect(self.stepperUpPress)
        self.alignmentDown.pressed.connect(self.stepperDownPress)
        self.alignmentLeft.pressed.connect(self.stepperLeftPress)
        self.alignmentRight.pressed.connect(self.stepperRightPress)
        self.alignmentUp.released.connect(self.stepperUpRelease)
        self.alignmentDown.released.connect(self.stepperDownRelease)
        self.alignmentLeft.released.connect(self.stepperLeftRelease)
        self.alignmentRight.released.connect(self.stepperRightRelease)

        # Stepper manual movement threads
        self.stepperUpThreadObj = None
        self.stepperDownThreadObj = None
        self.stepperLeftThreadObj = None
        self.stepperRightThreadObj = None

        # Thread worker for steppers
        self.stepperUpThreadRunning = False
        self.stepperDownThreadRunning = False
        self.stepperLeftThreadRunning = False
        self.stepperRightThreadRunning = False
        
        # User Input vars
        self.waitingForText = False     # detect if programme is asking for information
        self.inputtedText = ""          # text user inputted
        self.receiverForText = None     # function which runs

        # Alignment
        self.alignList = []
        self.itemsInAlign = 0

        # Angle Locking
        self.minAz = 0
        self.maxAz = 0
        self.minAlt = 0
        self.maxAlt = 0

        # Tracking
        self.tracking = False
        self.tracker = Tracker(self.stepperController)
        # self.requestPosition()  # ADDED CONFIGURATION WINDOW FOR THIS!

        # Graphing Window
        self.grapher = graphWindow()

        # Angle labels
        self.updateAltAzLabel(self.stepperController.getCoords())

        # Camera
        self.camera = None
        






    ############# Events
    
    def closeEvent(self,event):
        # Save Input Log
        self.commandInputLine.saveLog()
        # Close additional windows
        self.grapher.close()
        self.stepperConfigWindow.close()
        self.deviceConfigWindow.close()
        self.othersConfigWindow.close()
        self.locationConfigWindow.close()
        # Close running Threads
        self.stepperUpRelease()
        self.stepperDownRelease()
        self.stepperLeftRelease()
        self.stepperRightRelease()
        # Accept event
        event.accept()
    
    # Move window around
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.pos()

    # Move window around
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    # Move window around
    def mouseReleaseEvent(self, event):
        self.dragging = False

    # Add grey border to window
    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(170, 170, 170))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(Qt.transparent)
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)








    ############ Configuration Button Methods

    def stepperConfigWindowShow(self):
        self.stepperConfigWindow.show()
        self.stepperConfigWindow.activateWindow()
    
    #def deviceConfigWindowShow(self):
    #    self.deviceConfigWindow.show()
    #    self.deviceConfigWindow.activateWindow()

    def othersConfigWindowShow(self):
        self.othersConfigWindow.show()
        self.othersConfigWindow.activateWindow()

    def locationConfigWindowShow(self):
        self.locationConfigWindow.show()
        self.locationConfigWindow.activateWindow()






    ############ General Utility

    # Logs text onto the programme log window.
    def logText(self,msg): 
        self.commandOutputLine.setPlainText(self.commandOutputLine.toPlainText() + msg)
        self.commandOutputLine.moveCursor(self.commandOutputLine.textCursor().End)

    # Send requested user input to requesting function
    def sendText(self):
        if self.waitingForText:
            self.inputtedText = self.commandInputLine.text()
            self.waitingForText = False
            self.receiverForText()
            self.commandInputLine.setText('')

    # Update the delay value from the slider
    def updateDelayValue(self):
        self.alignmentDelayValueLabel.setText('Value: '+str(self.alignmentDelaySlider.value())+' ms')
    
    # Load Stepper Settings onto StepperController object
    def updateStepperController(self):
        self.stepperController = StepperController(self.stepperConfigWindow.getSettings(), self)
    
    # Update Az and Alt labels
    def updateAltAzLabel(self, sent_data):
        if not (type(sent_data[0]) == str and type(sent_data[1]) == str):
            angles = self.tracker.motorToReal(sent_data)
            self.alignmentAngles.setText(f"(az= {angles[0]:.3f}, alt= {angles[1]:.3f})")







    ######################### MANUAL STEPPER CONTROL

    def stepperUpPress(self):
        if not self.stepperUpThreadObj:
            self.stepperUpThreadObj = CommandThread(self.stepperUpThread, [])
            self.stepperUpThreadObj.send_data.connect(self.updateAltAzLabel)
            self.stepperUpThreadRunning = True
            self.stepperUpThreadObj.start()
    
    def stepperUpRelease(self):
        if self.stepperUpThreadObj:
            self.stepperUpThreadRunning = False
            self.stepperUpThreadObj.wait()
            self.stepperUpThreadObj = None

    def stepperDownPress(self):
        if not self.stepperDownThreadObj:
            self.stepperDownThreadObj = CommandThread(self.stepperDownThread, [])
            self.stepperDownThreadObj.send_data.connect(self.updateAltAzLabel)
            self.stepperDownThreadRunning = True
            self.stepperDownThreadObj.start()
    
    def stepperDownRelease(self):
        if self.stepperDownThreadObj:
            self.stepperDownThreadRunning = False
            self.stepperDownThreadObj.wait()
            self.stepperDownThreadObj = None
    
    def stepperLeftPress(self):
        if not self.stepperLeftThreadObj:
            self.stepperLeftThreadObj = CommandThread(self.stepperLeftThread, [])
            self.stepperLeftThreadObj.send_data.connect(self.updateAltAzLabel)
            self.stepperLeftThreadRunning = True
            self.stepperLeftThreadObj.start()
    
    def stepperLeftRelease(self):
        if self.stepperLeftThreadObj:
            self.stepperLeftThreadRunning = False
            self.stepperLeftThreadObj.wait()
            self.stepperLeftThreadObj = None
    
    def stepperRightPress(self):
        if not self.stepperRightThreadObj:
            self.stepperRightThreadObj = CommandThread(self.stepperRightThread, [])
            self.stepperRightThreadObj.send_data.connect(self.updateAltAzLabel)
            self.stepperRightThreadRunning = True
            self.stepperRightThreadObj.start()
    
    def stepperRightRelease(self):
        if self.stepperRightThreadObj:
            self.stepperRightThreadRunning = False
            self.stepperRightThreadObj.wait()
            self.stepperRightThreadObj = None




    def stepperUpThread(self, params, send_data):
        while self.stepperUpThreadRunning:
            self.stepperController.moveAlt(False, float(self.alignmentDelaySlider.value() / 1000.) )
            send_data.emit(self.stepperController.getCoords())

    def stepperDownThread(self, params, send_data):
        while self.stepperDownThreadRunning:
            self.stepperController.moveAlt(True, float(self.alignmentDelaySlider.value() / 1000.) )
            send_data.emit(self.stepperController.getCoords())

    def stepperLeftThread(self, params, send_data):
        while self.stepperLeftThreadRunning:
            self.stepperController.moveAz(True, float(self.alignmentDelaySlider.value() / 1000.) )
            send_data.emit(self.stepperController.getCoords())

    def stepperRightThread(self, params, send_data):
        while self.stepperRightThreadRunning:
            self.stepperController.moveAz(False, float(self.alignmentDelaySlider.value() / 1000.) )
            send_data.emit(self.stepperController.getCoords())




    ######################### ANGLE LOCKING METHODS
    def angleLock1(self):
        self.logText('>>> Beginning Angle Locking Routine...\n')
        self.logText('> Please position your device in its MINIMUM AZIMUTHAL angle. Type ok when finished or exit to cancel the procedure, pressing enter to confirm. To simply remove the limitations, type remove and press enter.\n')
        self.waitingForText = True
        self.receiverForText = self.angleLock2

    def angleLock2(self):
        response = self.inputtedText
        if response == 'ok':
            # Save MIN AZ
            self.minAz = self.stepperController.getCoords()[0]
            # Msg
            self.logText('> Confirmed. Now position your device in its MAXIMUM AZIMUTHAL ANGLE. Proceed as before.\n')
            self.waitingForText = True
            self.receiverForText = self.angleLock3
        elif response == 'exit':
            self.logText('> Exiting angle locking routine...\n\n')
        elif response == 'remove':
            # Disable angle locking in StepperController
            self.stepperController.setAngleLock(False)
            # Msg
            self.logText('> Removing previous limitations and exiting angle locking routine...\n\n')
        else:
            self.logText('> Invalid input. either type ok or exit.\n')
            self.waitingForText = True
            self.receiverForText = self.angleLock2

    def angleLock3(self):
        response = self.inputtedText
        if response == 'ok':
            # Save MAX AZ
            self.maxAz = self.stepperController.getCoords()[0]
            # Msg
            self.logText('> Confirmed. Now position your device in its MINIMUM POLAR ANGLE. Proceed as before.\n')
            self.waitingForText = True
            self.receiverForText = self.angleLock4
        elif response == 'exit':
            self.logText('> Exiting angle locking routine...\n\n')
        else:
            self.logText('> Invalid input. either type ok or exit.\n')
            self.waitingForText = True
            self.receiverForText = self.angleLock3

    def angleLock4(self):
        response = self.inputtedText
        if response == 'ok':
            # Save MIN ALT
            self.minAlt = self.stepperController.getCoords()[1]
            # Msg
            self.logText('> Confirmed. Now position your device in its MAXIMUM POLAR ANGLE. Proceed as before.\n')
            self.waitingForText = True
            self.receiverForText = self.angleLock5
        elif response == 'exit':
            self.logText('> Exiting angle locking routine...\n\n')
        else:
            self.logText('> Invalid input. either type ok or exit.\n')
            self.waitingForText = True
            self.receiverForText = self.angleLock4

    def angleLock5(self):
        response = self.inputtedText
        if response == 'ok':
            # Save MAX ALT
            self.maxAlt = self.stepperController.getCoords()[1]
            # Msg
            self.logText('> Confirmed. Saving all changes onto StepperController object...\n')
            # Apply changes on stepper controller
            self.stepperController.setAngleLock(True)
            self.stepperController.limitAngles(self.minAz, self.maxAz, self.minAlt, self.maxAlt)
            # Msg
            self.logText('> Finished Angle Locking Routine!\n\n')
        elif response == 'exit':
            self.logText('> Exiting angle locking routine...\n\n')
        else:
            self.logText('> Invalid input. either type ok or exit.\n')
            self.waitingForText = True
            self.receiverForText = self.angleLock5

    ######################### ALIGNMENT AND TRACKING METHODS

    #def requestPosition(self):
    #    self.logText("> Please insert your current coordinates in the following format (enter to ignore): latitude longitude altitude  \n")
    #    self.waitingForText = True
    #    self.receiverForText = self.setTracker

    def setTracker(self):
        coords = self.locationConfigWindow.getSettings()
        self.tracker = Tracker(self.stepperController, coords[0], coords[1], coords[2])
        self.logText(f"> Initialized Tracker with latitude: {coords[0]}, longitude: {coords[1]}, altitude: {coords[2]}\n\n")

    def alignmentRoutine1(self):

        self.logText("-----------------\n>>> Starting alignment routine...\n" + \
                    "> Please confirm your current coordinates are the ones in the location window (bottom right corner button).\n" + \
                    "> When finished, please type yes for a 10 element list of objects, no to just proceed, or type exit to cancel alignment\n" + \
                    "> Note: If you choose to generate a list, be weary that it will take a while...\n")
        self.waitingForText = True
        self.receiverForText = self.alignmentRoutine2

    def alignmentRoutine2(self):
        response = self.inputtedText
        if response == "exit":
            self.logText("> Cancelling alignment...\n")
            self.receiverForText = None
        elif response == "no":
            self.setTracker()
            self.receiverForText = self.alignmentRoutine3
            self.waitingForText = True
            self.logText("> Write object name(s) from SIMBAD (stars) or Horizons (planets) databases...\n")
        elif response == "yes":

            self.setTracker()
            astro=self.tracker.aloc
            mag = 0
            objs = astro.queryBrightObjects(mag)
            while len(objs) < 10 :
                mag += 0.5
                objs = astro.queryBrightObjects(mag)

            objsCopy = objs[:10].copy()
            for i,row in enumerate(objsCopy):
                azAlt = astro.getAzAlt(row,astro.getTime())
                objsCopy["RA"][i] = azAlt[0]
                objsCopy["DEC"][i] = azAlt[1]
            objsCopy.rename_column("RA","Az")
            objsCopy.rename_column("DEC","Alt")
            objsCopy["Az"].format = "8.3f"
            objsCopy["Alt"].format = "8.3f"
            objsCopy["V"].format = "8.3f"
            #objsCopyLines = objsCopy.pformat(max_lines=-1, max_width=-1)
            #objsCopyStr = '\n'.join(objsCopyLines)

            self.logText("> Please select ")
            self.logText("one " if self.alignmentDropdown.currentIndex() == 0 else "at least three (separated by commas (,) ) ")
            self.logText("of the provided objects for alignment, or provide the name of your preferred object(s) from SIMBAD (stars) or Horizons (planets) databases.\n" + \
                        "> Type exit to cancel alignment.\n" +\
                        "> Note: Use numeric IDs for Horizons objects.\n" +\
                        "> Below are the recommended objects:\n\n" + str(objsCopy) + "\n\n")

            self.receiverForText = self.alignmentRoutine3
            self.waitingForText = True
        else:
            self.logText("> Input not recognised, please type either ok or exit.\n")
            self.waitingForText = True

        self.inputtedText = ""


    def alignmentRoutine3(self):
        response = self.inputtedText
        if response == "exit":
            self.logText("> Cancelling alignment...\n")
            self.inputtedText = ""
            self.receiverForText = None
        else:
            astro = self.tracker.aloc
                
            #SÍTIO PARA FAZER O MOVIMENTO PRÉVIO PARA AJUDAR (deprecated feature due to lack of time)

            responses = response.split(",")
            # Alignment 1 point
            if len(responses) != 1 and self.alignmentDropdown.currentIndex() == 0:
                self.logText("> ERROR: Please provide only one object for alignment, or type exit to cancel.\n")
                self.waitingForText = True
                return
            # Alignment 3 point
            if len(responses) < 3 and self.alignmentDropdown.currentIndex() == 1:
                self.logText("> ERROR: Please provide at least three objects for alignment, or type exit to cancel.\n")
                self.waitingForText = True
                return
            for obj in responses:
                simbadQuery = astro.querySimbad(obj)
                horizonsQuery = astro.queryHorizons(obj)
                #print(obj,'\n',simbadQuery,'\n',horizonsQuery) # DEBUGGING
                #print(simbadQuery is None)
                # No results found
                if (simbadQuery is None) and (horizonsQuery is None):
                    self.logText(f"> ERROR: {obj} not recognised / ambiguous, please type either exit or valid identifier, preferrably one of the recommended. Note: for planets and satellites, use the ID.\n")
                    self.waitingForText = True
                    return
                #if len(astro.queryHorizons(obj)) > 1 or len(astro.querySimbad(obj)) > 1:
                #    self.logText(f"{obj} provided various possible objects. Please be more specific (use only ID for planet).\n")
                #    self.waitingForText = True
                #    return
            self.alignList = responses
            self.logText(f"> Starting alignment with {response}...\n" if self.alignmentDropdown.currentIndex() == 1 else "")
            self.logText(f"> Using {responses[0]} to align, please point to it and type ok when finished, or type exit to cancel.\n")
            self.inputtedText = ""
            self.itemsInAlign = len(responses)
            self.receiverForText = self.alignmentRoutine4
            self.waitingForText = True


    def alignmentRoutine4(self):
        response = self.inputtedText
        if response == "exit":
            self.logText("> Cancelling alignment...\n")
            self.inputtedText = ""
            self.receiverForText = None
        elif response == "ok":
            self.inputtedText = ""
            astro = self.tracker.aloc
            name = self.alignList[-self.itemsInAlign]
            queryStars = astro.querySimbad(name)
            queryPlanets = astro.queryHorizons(name)
            #print(name, queryStars, queryPlanets)
            if queryStars:
                self.tracker.addAlignmentPoint( astro.getAzAlt( queryStars,astro.getTime() ) , name)
            elif queryPlanets:
                self.tracker.addAlignmentPoint( astro.getAzAlt( queryPlanets,astro.getTime() ) , name)
            else: 
                self.logText(f"> Failed, try again\n")
                self.receiverForText = self.alignmentRoutine3
                self.waitingForText = True

            if self.itemsInAlign == 1:
                if self.alignmentDropdown.currentIndex() == 0:
                    self.tracker.onePointAlign()
                else:
                    self.tracker.pointAlignment()
                self.alignList = []
                self.logText("> Alignment complete. \n" + "-----------------\n\n")
                self.receiverForText = None
                self.updateAltAzLabel(self.stepperController.getCoords())
                return
            
            self.logText(f"> Using {self.alignList[-self.itemsInAlign+1]} to align, please point to it and type ok when finished, or type exit to cancel.\n")
            self.itemsInAlign -= 1
            self.receiverForText = self.alignmentRoutine4
            self.waitingForText = True
        
        else:
            self.logText("> Input not recognised, please type either ok or exit.\n")
            self.waitingForText = True
            self.inputtedText = ""
        
    def beginStopTracking1(self):
        if self.tracking:
            self.logText("> Ending Tracking Threads...\n")
            self.tracker.stopTracking = True

            self.tracking = False
            self.waitingForText = False
            return
            
        self.tracking = True
        self.logText("> Please input object query system: SIMBAD, Horizons or N2YO\n")
        self.waitingForText = True
        self.receiverForText = self.beginStopTracking2

    def beginStopTracking2(self):
        self.queryDatabase = self.inputtedText
        if self.queryDatabase not in ["SIMBAD", "Horizons", "N2YO"]:
            self.logText("> ERROR: Input not recognised, please try again\n")
            self.logText("> Please input object query system: SIMBAD, Horizons or N2YO\n")
            self.waitingForText = True
            self.receiverForText = self.beginStopTracking2

        self.logText("> Please input object id in the database\n")
        self.waitingForText = True
        self.receiverForText = self.beginStopTracking3

    def beginStopTracking3(self):
        
        queryId = self.inputtedText
        trackObj = None

        if self.queryDatabase == "SIMBAD":
            trackObj = self.tracker.aloc.querySimbad(queryId)
        elif self.queryDatabase == "Horizons":
            trackObj = self.tracker.aloc.queryHorizons(queryId)
        else:
            trackObj = self.tracker.aloc.queryN2YO(queryId)

        if trackObj is None:
            self.logText("> ERROR: Object not found! Please try again.\n")
            self.logText("> Please input object query system: SIMBAD, Horizons or N2YO\n")
            self.waitingForText = True
            self.receiverForText = self.beginStopTracking2

        # start thread for motor tracking
        self.logText(">>> Starting Motor Tracking Thread.\n")
        self.threadMotor = CommandThread(self.tracker.trackingRoutine,[self.queryDatabase,queryId])
        self.threadMotor.send_data.connect(self.updateAltAzLabel)
        self.threadMotor.start()

        # start thread for aquisition
        #if self.trackDeviceDropdown.currentIndex() == 0:     
        #    self.logText("* Telescope WORK IN PROGRESS.\n")
        #elif self.trackDeviceDropdown.currentIndex() == 1:  
        #    self.grapher.show()   
        #    self.logText("* Starting Antenna Thread.\n")
        #    # get params from config screen
        #    params = [self.grapher,0,0,0]
        #    self.threadAntenna = CommandThread(self.tracker.antennaRoutine, params)
        #    self.threadAntenna.start()





    ######################### ALIGNMENT AND TRACKING METHODS
    def cameraStart(self):
        if not self.camera:
            self.camera = True
            print('meow1')
        else:
            print('meow2')
            self.camera = None