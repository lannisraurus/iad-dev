"""
Duarte Tavares, João Camacho, Jorge Costa, Margarida Saraiva
IST, 2025 - IAD

This file contains a settings window for steppers.

"""
##################### Imports
from PyQt5.QtCore import *      # Basic Qt functionalities.
from PyQt5.QtWidgets import *   # GUI windows
from PyQt5.QtCore import *      # Qt threads, ...
from PyQt5.QtGui import *       # GUI Elements

##################### Commands Window Class
class stepperConfigWindow(QWidget):
    
    ############################### Constructor
    def __init__(self, mainWindow):
        
        self.mainWindow = mainWindow

        # Intializing general stuff
        super().__init__()
        self.setFixedSize(700,500)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('Astrolocator - Periferals Configuration')

        # Buttons
        self.closeButton = QPushButton("X")
        self.closeButton.setFixedSize(30, 20)
        self.closeButton.setStyleSheet(
            "font-weight: bold; border: none;"
        )
        self.closeButton.clicked.connect(self.close)

        self.applyButton = QPushButton("Apply and Save Changes")
        self.applyButton.clicked.connect(self.saveSettings)

        self.refreshButton = QPushButton("Refresh Microcontroller Description and Connection")
        self.refreshButton.clicked.connect(self.getMicrocontrollerInfo)

        # Labels
        self.stepperTitleLabel = QLabel('Periferals\' Configuration')

        self.commandsLabel = QLabel('Microcontroller Stepper Commands:')

        self.xMinusMode0Label = QLabel('X- half-step:')
        self.yMinusMode0Label = QLabel('Y- half-step:')
        self.xPlusMode0Label = QLabel('X+ half-step:')
        self.yPlusMode0Label = QLabel('Y+ half-step:')

        self.xMinusMode1Label = QLabel('X- full-step:')
        self.yMinusMode1Label = QLabel('Y- full-step:')
        self.xPlusMode1Label = QLabel('X+ full-step:')
        self.yPlusMode1Label = QLabel('Y+ full-step:')

        self.usbPortLabel = QLabel('USB Port:')
        self.usbPortsLabel = QLabel('Avaliable Ports:')

        self.descriptionLabel = QLabel('Microcontroller Connection:')
        self.descriptionLabel2 = QLabel('Microcontroller Description (define \'request_commands\' in microcontroller!):')

        # User Input Lines
        self.xMinusMode0Cmd = QLineEdit()
        self.yMinusMode0Cmd = QLineEdit()
        self.xPlusMode0Cmd = QLineEdit()
        self.yPlusMode0Cmd = QLineEdit()
        self.xMinusMode0Cmd.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.yMinusMode0Cmd.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.xPlusMode0Cmd.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.yPlusMode0Cmd.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self.xMinusMode1Cmd = QLineEdit()
        self.yMinusMode1Cmd = QLineEdit()
        self.xPlusMode1Cmd = QLineEdit()
        self.yPlusMode1Cmd = QLineEdit()
        self.xMinusMode1Cmd.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.yMinusMode1Cmd.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.xPlusMode1Cmd.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.yPlusMode1Cmd.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self.usbPortName = QLineEdit()
        self.usbPortName.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.usbPorts = QLineEdit()
        self.usbPorts.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.usbPorts.setReadOnly(True)

        self.stepperDescription = QTextEdit()
        self.stepperDescription.setReadOnly(True)

        # Layouts
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.setLayout(self.mainLayout)

        self.titleLayout = QHBoxLayout()
        self.titleLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.titleLayout)
        self.titleLayout.addWidget(self.stepperTitleLabel, alignment=Qt.AlignTop | Qt.AlignLeft)
        self.titleLayout.addWidget(self.closeButton, alignment=Qt.AlignTop | Qt.AlignRight)

        self.mainLayout.addWidget(self.commandsLabel)

        self.lay1 = QHBoxLayout()
        self.lay1.setAlignment(Qt.AlignTop)
        self.lay1.addWidget(self.xMinusMode0Label, alignment=Qt.AlignTop)
        self.lay1.addWidget(self.xMinusMode0Cmd, alignment=Qt.AlignTop)
        #self.lay1 = QHBoxLayout()
        self.lay1.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.lay1)
        self.lay1.addWidget(self.yMinusMode0Label, alignment=Qt.AlignTop)
        self.lay1.addWidget(self.yMinusMode0Cmd, alignment=Qt.AlignTop)
        self.lay3 = QHBoxLayout()
        self.lay3.setAlignment(Qt.AlignTop)
        self.lay3.addWidget(self.xPlusMode0Label, alignment=Qt.AlignTop)
        self.lay3.addWidget(self.xPlusMode0Cmd, alignment=Qt.AlignTop)
        #self.lay3 = QHBoxLayout()
        self.lay3.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.lay3)
        self.lay3.addWidget(self.yPlusMode0Label, alignment=Qt.AlignTop)
        self.lay3.addWidget(self.yPlusMode0Cmd, alignment=Qt.AlignTop)

        self.lay5 = QHBoxLayout()
        self.lay5.setAlignment(Qt.AlignTop)
        self.lay5.addWidget(self.xMinusMode1Label, alignment=Qt.AlignTop)
        self.lay5.addWidget(self.xMinusMode1Cmd, alignment=Qt.AlignTop)
        #self.lay5 = QHBoxLayout()
        self.lay5.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.lay5)
        self.lay5.addWidget(self.yMinusMode1Label, alignment=Qt.AlignTop)
        self.lay5.addWidget(self.yMinusMode1Cmd, alignment=Qt.AlignTop)
        self.lay7 = QHBoxLayout()
        self.lay7.setAlignment(Qt.AlignTop)
        self.lay7.addWidget(self.xPlusMode1Label, alignment=Qt.AlignTop)
        self.lay7.addWidget(self.xPlusMode1Cmd, alignment=Qt.AlignTop)
        #self.lay7 = QHBoxLayout()
        self.lay7.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.lay7)
        self.lay7.addWidget(self.yPlusMode1Label, alignment=Qt.AlignTop)
        self.lay7.addWidget(self.yPlusMode1Cmd, alignment=Qt.AlignTop)

        self.mainLayout.addWidget(self.applyButton)

        self.mainLayout.addWidget(self.descriptionLabel)
        
        self.lay8 = QHBoxLayout()
        self.lay8.addWidget(self.usbPortsLabel, alignment=Qt.AlignTop)
        self.lay8.addWidget(self.usbPorts, alignment=Qt.AlignTop)
        self.mainLayout.addLayout(self.lay8)

        self.lay9 = QHBoxLayout()
        self.lay9.addWidget(self.usbPortLabel, alignment=Qt.AlignTop)
        self.lay9.addWidget(self.usbPortName, alignment=Qt.AlignTop)
        self.mainLayout.addLayout(self.lay9)

        self.mainLayout.addWidget(self.descriptionLabel2)
        self.mainLayout.addWidget(self.stepperDescription)

        self.mainLayout.addWidget(self.refreshButton)
        

        # Load default settings
        mainWindow.logText('> Configuring Stepper Settings...\n')
        self.loadSettings()

        # Dragging window
        self.dragging = False

    ############################### Events

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

    ############################### Settings (saved in file "stepper_settings.txt")

    def loadSettings(self):
        try:
            file = open('assets/stepper_settings','r')
            self.mainWindow.logText('> Opened configuration file.\n')
        except:
            file = None
            self.mainWindow.logText('> Could not open configuration file!\n')

        try:
            self.xMinusMode0Cmd.setText(file.readline())
            self.yMinusMode0Cmd.setText(file.readline())
            self.xPlusMode0Cmd.setText(file.readline())
            self.yPlusMode0Cmd.setText(file.readline())
            self.xMinusMode1Cmd.setText(file.readline())
            self.yMinusMode1Cmd.setText(file.readline())
            self.xPlusMode1Cmd.setText(file.readline())
            self.yPlusMode1Cmd.setText(file.readline())
            self.mainWindow.logText('> Successfully loaded previous stepper settings.\n')
        except:
            self.xMinusMode0Cmd.setText(' ')
            self.yMinusMode0Cmd.setText(' ')
            self.xPlusMode0Cmd.setText(' ')
            self.yPlusMode0Cmd.setText(' ')
            self.xMinusMode1Cmd.setText(' ')
            self.yMinusMode1Cmd.setText(' ')
            self.xPlusMode1Cmd.setText(' ')
            self.yPlusMode1Cmd.setText(' ')
            self.mainWindow.logText('> Could not load previous stepper settings. Please configure and apply settings!\n')
        
        if file:
            file.close()

    def saveSettings(self):
        try:
            file = open('assets/stepper_settings','w')

            file.write(self.xMinusMode0Cmd.text().strip('\n')+'\n')
            file.write(self.yMinusMode0Cmd.text().strip('\n')+'\n')
            file.write(self.xPlusMode0Cmd.text().strip('\n')+'\n')
            file.write(self.yPlusMode0Cmd.text().strip('\n')+'\n')

            file.write(self.xMinusMode1Cmd.text().strip('\n')+'\n')
            file.write(self.yMinusMode1Cmd.text().strip('\n')+'\n')
            file.write(self.xPlusMode1Cmd.text().strip('\n')+'\n')
            file.write(self.yPlusMode1Cmd.text().strip('\n')+'\n')

            file.close()
            self.mainWindow.updateStepperController()
            self.mainWindow.logText('> Successfully saved and applied new stepper settings.\n\n')
        except:
            self.mainWindow.logText('> Something went wrong! Could not save new stepper settings!\n\n')
    
    def getMicrocontrollerInfo(self):
        if self.usbPortName.text() != '':
            self.mainWindow.stepperController.setPort(self.usbPortName.text())
        microcontrollerInfo = self.mainWindow.stepperController.getMicrocontrollerInfo()
        microcontrollerInfo = microcontrollerInfo.replace('|','\n')
        self.stepperDescription.setText(microcontrollerInfo)
        self.setPortInfo()
    
    def setPortInfo(self):
        self.usbPortName.setText(self.mainWindow.stepperController.getPort())
        self.usbPorts.setText(self.mainWindow.stepperController.getAvailablePorts())