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
import numpy

##################### User defined functions (imports)
from src.ui.inputConsole import inputConsole                 # User input
from src.StepperController import StepperController          # Manipulating Stepper Motors
from src.Tracker import Tracker                              # Coordinating StepperController with Astrolocator
from src.ui.stepperConfigWindow import stepperConfigWindow   # Configuration window for steppers

from src.ui.locationConfigWindow import locationConfigWindow # Configuration window for location

from src.utils.commandThread import CommandThread            # For multithreading routines


##################### Main Programme Class
class mainWindow(QWidget):

    ############ Constructor
    def __init__(self, *args, **kwargs):

        ############################# GENERAL

        super().__init__(*args, **kwargs)   # Initialize parent class

        ############################# UI ELEMENTS

        # General
        self.setFixedSize(900,520)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('Astrolocator')
        self.setWindowIcon(QIcon('assets/logo.png'))

        # Close Button
        self.closeButton = QPushButton("X")
        self.closeButton.setFixedSize(30, 20)
        self.closeButton.setStyleSheet(
            "font-weight: bold; border: none;"
        )
        self.closeButton.clicked.connect(self.close)

        # Alignment Button
        self.alignmentBeginButton = QPushButton('Begin Alignment')
        self.alignmentBeginButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.alignmentBeginButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogYesButton))
        self.alignmentBeginButton.clicked.connect(self.alignmentRoutine1)

        # Alignment Delay Slider
        self.alignmentDelaySlider = QSlider(Qt.Horizontal, self)
        self.alignmentDelaySlider.setMaximum(100)
        self.alignmentDelaySlider.setMinimum(1)
        self.alignmentDelaySlider.valueChanged.connect(self.updateDelayValue)

        # Alignment options
        self.alignmentDropdown = QComboBox()
        self.alignmentDropdown.addItems(['1 Point','N Point'])
        self.alignmentDropdown.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.steppersDropdown = QComboBox()
        self.steppersDropdown.addItems(['RB-Moto2 (Joy-IT)'])

        # Manual Movement Mode
        self.movementModeDropdown = QComboBox()
        self.movementModeDropdown.addItems(['Half-Stepping','Full-Stepping'])
        self.movementModeDropdown.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Alignment Movement buttons
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

        # Tracking button
        self.trackBeginButton = QPushButton('Begin Tracking')
        self.trackBeginButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.trackBeginButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView))
        self.trackBeginButton.clicked.connect(self.beginStopTracking1)

        # Stepper settings
        self.settingsSteppersButton = QPushButton('Periferals\' Settings')
        self.settingsSteppersButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.settingsSteppersButton.clicked.connect(self.stepperConfigWindowShow)

        # Location settings
        self.settingsLocationButton = QPushButton('Location Settings')
        self.settingsLocationButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.settingsLocationButton.clicked.connect(self.locationConfigWindowShow)

        # Logo
        self.groupLogoPixmap = QPixmap('assets/logo.png')
        self.groupLogoPixmap = self.groupLogoPixmap.scaled(250, 250, Qt.KeepAspectRatio)

        # Labels
        self.titleLabel = QLabel('Astrolocator 2.0')
        self.groupLogoLabel = QLabel()
        self.groupLogoLabel.setPixmap(self.groupLogoPixmap)
        self.inputCommandLabel = QLabel('User Input (Enter to Confirm):')
        self.alignmentLabel = QLabel('Alignment / Movement:')
        self.alignmentLabel.setFixedWidth(200)
        self.alignmentDelayLabel = QLabel('Step Delay:')
        self.alignmentTypeLabel = QLabel('Alignment Type:')
        self.trackLabel = QLabel('Tracking / Data Acquisition:')
        self.trackLabel.setFixedWidth(200)
        self.settingsLabel = QLabel('Settings:')
        self.settingsLabel.setFixedWidth(200)
        self.alignmentDelayValueLabel = QLabel('hi!')
        self.updateDelayValue()
        self.alignmentDelayValueLabel.setFixedWidth(100)
        self.alignmentAngles = QLabel('(az=ERR , alt=ERR)')
        self.trackDevicesLabel = QLabel('Acquisition Devices:')
        self.movementModeLabel = QLabel('Mode:')

        # Input console and output log
        self.commandOutputLine = QTextEdit()
        self.commandOutputLine.setReadOnly(True)
        self.commandOutputLine.setFixedHeight(250)
        self.commandOutputLine.setMinimumWidth(400)
        self.logText("----- Astrolocator (Log) -----\n\n")
        self.logText("> Welcome to Astrolocator 2.0, the second prototype of the Astrolocator project! Make sure to align your system before tracking objects. Enjoy!\n")
        self.logText("> Duarte Tavares, João Camacho, Jorge Costa, Margarida Saraiva (IST, 2025 - IAD)\n\n")
        self.commandInputLine = inputConsole('assets/input_log', self)
        self.commandInputLine.returnPressed.connect(self.sendText)

        # Spacers
        self.spacer1 = QSpacerItem(40, 20, QSizePolicy.Minimum,QSizePolicy.Expanding)

        ############################# UI ORGANIZATION

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.setLayout(self.mainLayout)

        self.titleLayout = QHBoxLayout()
        self.titleLayout.addWidget(self.titleLabel, alignment=Qt.AlignTop | Qt.AlignLeft)
        self.titleLayout.addWidget(self.closeButton, alignment=Qt.AlignTop | Qt.AlignRight)
        self.mainLayout.addLayout(self.titleLayout)
        
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
        self.alignmentLayoutR5.addWidget(self.movementModeLabel)
        self.alignmentLayoutR5.addWidget(self.movementModeDropdown)
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
        
        self.trackLayout.setAlignment(Qt.AlignTop)
        self.trackLayoutR.setAlignment(Qt.AlignTop)

        self.settingsLayout.addWidget(self.settingsLabel, alignment= Qt.AlignTop | Qt.AlignLeft)
        self.settingsLayout.addLayout(self.settingsLayoutR)

        self.settingsLayoutR.addWidget(self.settingsSteppersButton)
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
        self.tracker = None
        self.updateStepperController()
        self.stepperConfigWindow.getMicrocontrollerInfo()
        self.stepperConfigWindow.setPortInfo()

        # Location Configuration
        self.locationConfigWindow = locationConfigWindow(self)

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
        self.waitingForText = False     # Detect if programme is asking for information
        self.inputtedText = ""          # Text user inputted
        self.receiverForText = None     # Function which runs

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

        # Angle labels
        self.updateAltAzLabel(self.stepperController.getCoords())

    ######################### EVENTS
    
    def closeEvent(self,event):
        # Save Input Log
        self.commandInputLine.saveLog()
        # Close additional windows
        #self.grapher.close()
        self.stepperConfigWindow.close()
        #self.deviceConfigWindow.close()
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

    ######################### CONFIGURATION BUTTON SETTINGS

    def stepperConfigWindowShow(self):
        self.stepperConfigWindow.show()
        self.stepperConfigWindow.activateWindow()

    def locationConfigWindowShow(self):
        self.locationConfigWindow.show()
        self.locationConfigWindow.activateWindow()

    ######################### GENERAL UTILITY

    # Logs text onto the programme log window.
    def logText(self,msg): 
        self.commandOutputLine.insertHtml(msg.replace("\n","<br>"))
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
        exist = False
        if not self.tracker is None:
            exist = True
            self.tracker.motors = None
        self.stepperController = None
        self.stepperController = StepperController(self)
        if exist:
            self.tracker.motors = self.stepperController

    # Update Az and Alt labels
    def updateAltAzLabel(self, sent_data):
        if not (type(sent_data[0]) == str and type(sent_data[1]) == str):
            angles = self.tracker.motorToReal(sent_data)
            self.alignmentAngles.setText(f"(az= {angles[0]:.3f}, alt= {angles[1]:.3f})")

    ######################### MANUAL STEPPER CONTROL BUTTONS

    def stepperUpPress(self):
        if not self.stepperUpThreadObj:
            if self.movementModeDropdown.currentIndex() == 0:
                params = [self.stepperConfigWindow.yPlusMode0Cmd.text()]
            else:
                params = [self.stepperConfigWindow.yPlusMode1Cmd.text()]
            self.stepperUpThreadObj = CommandThread(self.stepperUpThread, params)
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
            if self.movementModeDropdown.currentIndex() == 0:
                params = [self.stepperConfigWindow.yMinusMode0Cmd.text()]
            else:
                params = [self.stepperConfigWindow.yMinusMode1Cmd.text()]
            self.stepperDownThreadObj = CommandThread(self.stepperDownThread, params)
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
            if self.movementModeDropdown.currentIndex() == 0:
                params = [self.stepperConfigWindow.xMinusMode0Cmd.text()]
            else:
                params = [self.stepperConfigWindow.xMinusMode1Cmd.text()]
            self.stepperLeftThreadObj = CommandThread(self.stepperLeftThread, params)
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
            if self.movementModeDropdown.currentIndex() == 0:
                params = [self.stepperConfigWindow.xPlusMode0Cmd.text()]
            else:
                params = [self.stepperConfigWindow.xPlusMode1Cmd.text()]
            self.stepperRightThreadObj = CommandThread(self.stepperRightThread, params)
            self.stepperRightThreadObj.send_data.connect(self.updateAltAzLabel)
            self.stepperRightThreadRunning = True
            self.stepperRightThreadObj.start()
    
    def stepperRightRelease(self):
        if self.stepperRightThreadObj:
            self.stepperRightThreadRunning = False
            self.stepperRightThreadObj.wait()
            self.stepperRightThreadObj = None

    ######################### STEPPER MANUAL THREADS

    def stepperUpThread(self, params, send_data):
        while self.stepperUpThreadRunning:
            self.stepperController.step(params[0], float(self.alignmentDelaySlider.value() / 1000.))
            send_data.emit(self.stepperController.getCoords())

    def stepperDownThread(self, params, send_data):
        while self.stepperDownThreadRunning:
            self.stepperController.step(params[0], float(self.alignmentDelaySlider.value() / 1000.))
            send_data.emit(self.stepperController.getCoords())

    def stepperLeftThread(self, params, send_data):
        while self.stepperLeftThreadRunning:
            self.stepperController.step(params[0], float(self.alignmentDelaySlider.value() / 1000.))
            send_data.emit(self.stepperController.getCoords())

    def stepperRightThread(self, params, send_data):
        while self.stepperRightThreadRunning:
            self.stepperController.step(params[0], float(self.alignmentDelaySlider.value() / 1000.))
            send_data.emit(self.stepperController.getCoords())

    ######################### ALIGNMENT ROUTINES

    def alignmentRoutine1(self):

        self.logText(">>> Starting alignment routine...\n" + \
                    "> Please confirm current coordinates in the location settings window.\n" + \
                    "> Input <b>yes</b> for a 10 element list of objects, <b>no</b> otherwise, and <b>exit</b> to cancel.\n" + \
                    "> Note: If you choose to generate a list, it might take longer ...\n")
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
            self.logText("> Write object name(s) from SIMBAD (stars) or Horizons (planets) databases.\n")
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

            self.logText("> Please select ")
            self.logText("<b>one</b> " if self.alignmentDropdown.currentIndex() == 0 else "<b>at least three</b> (separated by commas (,) ) ")
            self.logText("of the provided objects for alignment, or provide the name of your preferred object(s) from SIMBAD (stars) or Horizons (planets) databases.\n" + \
                        "> Type <b>exit</b> to cancel alignment.\n" +\
                        "> Note: Use numeric IDs for Horizons objects.\n" +\
                        "> Below are the recommended objects:\n")

            html = "<table><tr> <td>| Name</td>  <td>| Azimuth</td>  <td>| Altitude</td>  <td>| Magnitude</td> </tr>"
        
            for row in objsCopy:
                html += '<tr>'
                for val in row:
                    numStr = str(val)
                    index = numStr.find('.')

                    if index != -1 and index + 4 <= len(numStr):
                        insert_position = index + 4
                        numStr = numStr[:insert_position]
                    
                    html += f"<td>| {numStr}</td>"

                html += '</tr>'
            
            html += '</table>'

            self.logText(html+'\n')

            self.receiverForText = self.alignmentRoutine3
            self.waitingForText = True
        else:
            self.logText("> Input not recognised, please type either <b>yes</b>, <b>no</b> or <b>exit</b>.\n")
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
                # No results found
                if (simbadQuery is None) and (horizonsQuery is None):
                    self.logText(f"> ERROR: {obj} not recognised / ambiguous, please type either exit or valid identifier, preferrably one of the recommended. Note: for planets and satellites, use the ID.\n")
                    self.waitingForText = True
                    return
            self.alignList = responses
            self.logText(f"> Starting alignment with {response}...\n" if self.alignmentDropdown.currentIndex() == 1 else "")
            self.logText(f"> Using {responses[0]} to align, please point to it and type <b>ok</b> when finished, or type <b>exit</b> to cancel.\n")
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
                self.logText("> Alignment complete. \n" + "\n")
                self.receiverForText = None
                self.updateAltAzLabel(self.stepperController.getCoords())
                return
            
            self.logText(f"> Using {self.alignList[-self.itemsInAlign+1]} to align, please point to it and type <b>ok</b> when finished, or type <b>exit</b> to cancel.\n")
            self.itemsInAlign -= 1
            self.receiverForText = self.alignmentRoutine4
            self.waitingForText = True
        
        else:
            self.logText("> Input not recognised, please type either <b>ok</b> or <b>exit</b>.\n")
            self.waitingForText = True
            self.inputtedText = ""

    ######################### TRACKING METHODS

    def setTracker(self):
        coords = self.locationConfigWindow.getSettings()
        self.tracker = Tracker(self.stepperController, coords[0], coords[1], coords[2])
        self.logText(f"> Initialized Tracker with latitude: {coords[0]}, longitude: {coords[1]}, altitude: {coords[2]}\n\n")

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

