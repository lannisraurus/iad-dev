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
        self.setFixedSize(500,500)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('Astrolocator - Stepper Configuration')

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
        self.stepperTitleLabel = QLabel('Stepper Configuration')
        self.stepperTypeLabel = QLabel('Stepper Type:')
        self.gearRatioLabel = QLabel('Mount Gear Ratio:')
        self.pinsLabel = QLabel('Pin Configuration:')

        # Dropdowns
        self.stepperTypeDropdown = QComboBox()
        self.stepperTypeDropdown.addItems(['None','RB-MOTO2 (Joy-IT)'])
        self.stepperTypeDropdown.currentIndexChanged.connect(self.changeStepperType)

        # User Input Spinboxes
        self.gearRatioInput = QDoubleSpinBox()

        # User Input Lines
        self.pinsConfig = QLineEdit()
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

        self.stepperTypeLayout = QHBoxLayout()
        self.stepperTypeLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.stepperTypeLayout)
        self.stepperTypeLayout.addWidget(self.stepperTypeLabel, alignment=Qt.AlignTop)
        self.stepperTypeLayout.addWidget(self.stepperTypeDropdown, alignment=Qt.AlignTop)

        self.pinsLayout = QHBoxLayout()
        self.pinsLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.pinsLayout)
        self.pinsLayout.addWidget(self.pinsLabel, alignment=Qt.AlignTop)
        self.pinsLayout.addWidget(self.pinsConfig)

        self.gearRatioLayout = QHBoxLayout()
        self.gearRatioLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.gearRatioLayout)
        self.gearRatioLayout.addWidget(self.gearRatioLabel, alignment=Qt.AlignTop)
        self.gearRatioLayout.addWidget(self.gearRatioInput)

        self.mainLayout.addWidget(self.stepperDescription)
        self.mainLayout.addWidget(self.applyButton)

        # Load default settings
        mainWindow.logText('> Configuring Stepper Settings...\n')
        self.loadSettings()
        self.changeStepperType()






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





    ############################### Settings

    def changeStepperType(self):
        match self.stepperTypeDropdown.currentIndex():
            case 0:
                self.stepperDescription.setText('Please select a stepper.')
            case 1:
                self.stepperDescription.setText('RB-Moto2 (Joy-It) steppers: In the pin configuration, simply write a sequence of the connected pins to GPIO in the following order: Coil1A1 Coil1A2 Coil1B1 Coil1B2 Coil2A1 Coil2A2 Coil2B1 Coil2B2')

    def loadSettings(self):
        try:
            file = open('assets/stepper_settings','r')
            self.mainWindow.logText('> Opened configuration file.\n')
        except:
            file = None
            self.mainWindow.logText('> Could not open configuration file!\n')

        try:
            self.stepperTypeDropdown.setCurrentIndex(int(file.readline()))
            self.pinsConfig.setText(file.readline())
            self.gearRatioInput.setValue(float(file.readline()))
            self.mainWindow.logText('> Successfully loaded previous stepper settings.\n')
        except:
            self.stepperTypeDropdown.setCurrentIndex(0)
            self.pinsConfig.setText('')
            self.gearRatioInput.setValue(1)
            self.mainWindow.logText('> Could not load previous stepper settings. Please configure and apply settings!\n')
        
        if file:
            file.close()
        
        self.mainWindow.logText('\n')

    def saveSettings(self):
        try:
            file = open('assets/stepper_settings','w')
            file.write(str(self.stepperTypeDropdown.currentIndex())+'\n')
            file.write(self.pinsConfig.text().strip('\n')+'\n')
            file.write(str(self.gearRatioInput.value()))
            file.close()
            self.mainWindow.updateStepperController()
            self.mainWindow.logText('> Successfully saved and applied new stepper settings.\n\n')
        except:
            self.mainWindow.logText('> Something went wrong! Could not save new stepper settings!\n\n')
    
    def getSettings(self):
        return [self.stepperTypeDropdown.currentText(), self.pinsConfig.text(), self.gearRatioInput.value()]
