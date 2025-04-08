"""
Duarte Tavares, João Camacho, Jorge Costa, Margarida Saraiva
IST, 2025 - IAD

This file contains a settings window for other periferals.

"""
##################### Imports
from PyQt5.QtCore import *      # Basic Qt functionalities.
from PyQt5.QtWidgets import *   # GUI windows
from PyQt5.QtCore import *      # Qt threads, ...
from PyQt5.QtGui import *       # GUI Elements
try:
    from gpiozero import OutputDevice
except:
    print('ERROR in othersConfigWindow: Could not import gpiozero! Please install!')

##################### Commands Window Class
class othersConfigWindow(QWidget):
    # Constructor
    def __init__(self, mainWindow):
        # Intializing general stuff
        self.mainWindow = mainWindow

        super().__init__()

        self.setFixedSize(500,500)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('Astrolocator - Other Configurations')

        # Buttons
        self.closeButton = QPushButton("X")
        self.closeButton.setFixedSize(30, 20)
        self.closeButton.setStyleSheet(
            "font-weight: bold; border: none;"
        )
        self.closeButton.clicked.connect(self.close)
        self.applyButton = QPushButton("Apply Changes")
        self.applyButton.clicked.connect(self.saveSettings)

        # Labels
        self.laserTitleLabel = QLabel('Other Configurations')
        self.laserPinsLabel = QLabel('Laser Pin Configuration:')
        self.laserTypeLabel = QLabel('Laser Type:')
                
        #Dropdown
        self.laserTypeDropdown = QComboBox()
        self.laserTypeDropdown.addItems(['None','Módulo laser 5mW - Ponto vermelho'])
        self.laserTypeDropdown.currentIndexChanged.connect(self.changeLaserType)

        # Text Edits
        self.laserPinsConfig = QLineEdit()
        self.laserPinsConfig.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.laserDescription = QTextEdit()
        self.laserDescription.setReadOnly(True)
        
        # Layouts
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.setLayout(self.mainLayout)

        self.titleLayout = QHBoxLayout()
        self.titleLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.titleLayout)
        self.titleLayout.addWidget(self.laserTitleLabel, alignment=Qt.AlignTop | Qt.AlignLeft)
        self.titleLayout.addWidget(self.closeButton, alignment=Qt.AlignTop | Qt.AlignRight)

        self.laserTypeLayout = QHBoxLayout()
        self.laserTypeLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.laserTypeLayout)
        self.laserTypeLayout.addWidget(self.laserTypeLabel, alignment=Qt.AlignTop)
        self.laserTypeLayout.addWidget(self.laserTypeDropdown, alignment=Qt.AlignTop)

        self.pinsLayout = QHBoxLayout()
        self.pinsLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.pinsLayout)
        self.pinsLayout.addWidget(self.laserPinsLabel, alignment=Qt.AlignTop)
        self.pinsLayout.addWidget(self.laserPinsConfig, alignment=Qt.AlignTop)

        self.mainLayout.addWidget(self.laserDescription)
        self.mainLayout.addWidget(self.applyButton)

        # Load default settings
        mainWindow.logText('> Configuring Other Settings...\n')
        self.loadSettings(mainWindow)
        mainWindow.logText('\n')
        self.changeLaserType()

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

    def loadSettings(self, mainWindow):
        pins = []
        try:
            file = open('assets/other_settings','r')
            mainWindow.logText('> Opened laser configuration file.\n')
        except:
            file = None
            mainWindow.logText('> Could not open laser configuration file!\n')
        try:    
            self.laserPinsConfig.setText(file.readline())
            mainWindow.logText('> Successfully loaded previous laser settings.\n')
            pins = self.laserPinsConfig.split(' ')
        except:
            self.laserPinsConfig.setText('')
            #É POSSÍVEL QUE EXISTAM 2 PINS EM VEZ DE 3
        if len(pins) == 3:
            try:
                    self.laserPin1 = OutputDevice(int(pins[0]))
                    self.laserPin2 = OutputDevice(int(pins[1]))
                    self.laserPin3 = OutputDevice(int(pins[2]))
            except:
                    mainWindow.logText('> ERROR! Could not set output pins! Either the pins are not ints, or your device cannot access the GPIO pins!\n')
        else:
                mainWindow.logText('> ERROR! Pin configuration is wrong! These should be 3!\n')
        file.close()

    def saveSettings(self):
        file = open('assets/other_settings','w')
        file.write(self.laserPinsConfig.text()+'\n')
        file.close()

    def changeLaserType(self):
        match self.laserTypeDropdown.currentIndex():
            case 0:
                self.laserDescription.setText('Please select a laser.')
            case 1:
                #MUDAR ISTO QUANDO TIVER O MANUAL DO LASER
                self.laserDescription.setText('Módulo laser 5mW - Ponto vermelho: In the pin configuration, simply write a sequence of the connected pins to GPIO in the following order: pin1 pin2 pin3')

    def laser(self):
        try:
            #MUDAR ISTO QUANDO TIVER O MANUAL DO LASER
            self.laserPin1.toggle()
            self.laserPin2.toggle()
            self.laserPin3.toggle()
        except:
            self.mainWindow.logText('> Laser is not connected! \n')     