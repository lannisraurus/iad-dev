# Communications
from PyQt5.QtWidgets import QApplication # Qt App

import os           # For USB access.

# Numerical
import numpy        # For Numerical Calculations.

##################### User defined functions (imports)
from mainWindow import mainWindow

##################### Main Programme Function

if __name__ == '__main__':

    # Start QApplication
    mainApp = QApplication([])
    
    # Create main window
    mainWin = mainWindow()
    mainWin.installEventFilter(mainWin)
    # Start event loop
    mainApp.exec()
