##################### Python Library Imports

# UI Lib
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QLabel,
)

from PyQt5.QtGui import QPixmap

import os           # For USB access.
import serial       # For USB communication.
import pyqtgraph    # For Data Visualization.
import numpy        # For Numerical Calculations.

##################### User defined functions (imports)

##################### Main Programme Class

# Class which inherits from QWidget class. Contains UI functionalities.

class mainWindow(QWidget):

    # Constructor
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Set title
        self.setWindowTitle('IAD - Project I (Group I)')

        # Set Size
        self.setGeometry(100, 100, 320, 210)

        # UI Elements - Buttons
        startButton = QPushButton('Start Acquisition')
        startButton.clicked.connect(self.startCommand)
        stopButton = QPushButton('End Acquisition')
        stopButton.clicked.connect(self.stopCommand)

        # UI Elements - Pixmaps
        groupLogoPixmap = QPixmap('assets/logo.png')

        # UI Elements - Labels
        self.statusLabel = QLabel('STATUS: [Not Running]')
        commandInputLabel = QLabel('Insert Command Here:')
        groupLogoLabel = QLabel()
        groupLogoLabel.setPixmap(groupLogoPixmap)

        # UI Elements - Line Edits
        commandInputLine = QLineEdit()
        
        # Create a layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # UI Element Orders in layout
        layout.addWidget(groupLogoLabel)
        layout.addWidget(self.statusLabel)
        layout.addWidget(startButton)
        layout.addWidget(stopButton)
        layout.addWidget(commandInputLabel)
        layout.addWidget(commandInputLine)
        
        # Show window
        self.show()
    
    # UI functions
    def startCommand(self):
        self.statusLabel.setText('STATUS: [Running]')
        print('*** Starting Acquisition...')

    def stopCommand(self):
        self.statusLabel.setText('STATUS: [Not Running]')
        print('*** Stopping Acquisition...')

##################### Main Programme Function

if __name__ == '__main__':

    # Start QApplication
    mainApp = QApplication([])
    
    # Create main window
    mainWin = mainWindow()
    
    # Start event loop
    mainApp.exec()
