"""
Duarte Tavares, João Camacho, Jorge Costa, Margarida Saraiva
IST, 2025 - IAD

INSERT DESCRIPTION HERE

"""
##################### Python Libraries
from PyQt5.QtWidgets import QApplication # Qt App

##################### User defined classes/functions
from src.ui.mainWindow import mainWindow

##################### Main Programme Function

if __name__ == '__main__':

    # Start QApplication
    mainApp = QApplication([])
    
    # Create main window
    mainWin = mainWindow()
    mainWin.installEventFilter(mainWin)
    
    # Start event loop
    mainApp.exec()
