"""
Duarte Tavares, João Camacho, Jorge Costa, Margarida Saraiva
IST, 2025 - IAD

This file contains a settings window for other periferals 
(namely, the laser).

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

    ################################################# Constructor
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
        self.laserTypeDropdown.addItems(['None','Laser 5mW - Ponto vermelho'])
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
        self.loadSettings()
        mainWindow.logText('\n')
        self.changeLaserType()

        # Dragging window
        self.dragging = False

    ################################################# Events

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

    ################################################# Settings (saved in file "other_settings.txt")

    def loadSettings(self):
        pins = []
        try:
            file = open('assets/other_settings','r')
            self.mainWindow.logText('> Opened other configurations file.\n')
        except:
            file = None
            self.mainWindow.logText('> Could not open other configurations file!\n')
        try:
            self.laserTypeDropdown.setCurrentIndex(int(file.readline()))
            self.laserPinsConfig.setText(file.readline())
            self.mainWindow.logText('> Successfully loaded previous other settings.\n')
            pins = self.laserPinsConfig.text().strip().split(' ')
        except:
            self.laserPinsConfig.setText('')
            self.mainWindow.logText('> Could not load previous other settings. Please configure and apply settings!\n')

        if len(pins) == 1:
            try:
                self.laserPin = OutputDevice(int(pins[0]))
            except:
                self.mainWindow.logText('> ERROR! Could not set output pins! Either the pins are not ints, or your device cannot access the GPIO pins!\n')
        else:
            self.mainWindow.logText('> ERROR! Pin configuration is wrong! These should be 1!\n')

        if file:
            file.close()

    def saveSettings(self):
        try:
            file = open('assets/other_settings','w')
            file.write(str(self.laserTypeDropdown.currentIndex())+'\n')
            file.write(self.laserPinsConfig.text()+'\n')
            file.close()
            self.mainWindow.logText('> Successfully saved other settings.\n')
            try:
                pins = self.laserPinsConfig.text().strip().split(' ')
                self.laserPin3 = OutputDevice(int(pins[0]))
                self.mainWindow.logText('> Successfully applied other settings.\n\n')
            except:
                self.mainWindow.logText('> ERROR: Could not apply other settings!\n\n')
        except:
            file = None
            self.mainWindow.logText('> ERROR! Could not save other configurations!\n\n')
        
        if file:
            file.close()

    def changeLaserType(self):
        match self.laserTypeDropdown.currentIndex():
            case 0:
                self.laserDescription.setText('Please select a laser.')
            case 1:
                self.laserDescription.setText('Laser 5mW - Ponto vermelho: In the pin configuration, simply write a sequence of the connected pin to GPIO')

    ################################################# Turn on/off the laser 
    def laserToggle(self):
        try:
            self.laserPin.toggle()
        except:
            self.mainWindow.logText('> ERROR: Laser is not connected / set up properly! \n\n')
