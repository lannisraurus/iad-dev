"""
Duarte Tavares, João Camacho, Jorge Costa, Margarida Saraiva
IST, 2025 - IAD

INSERT DESCRIPTION HERE

"""
##################### Python Libraries
from PyQt5.QtWidgets import QApplication # Qt App
from PyQt5.QtCore import *
from PyQt5.QtGui import *

##################### Stop __pycache__ from generating
import sys
sys.dont_write_bytecode = True

##################### User defined classes/functions
from src.ui.mainWindow import mainWindow

##################### App aesthetics
def setAppDarkMode(app):
    app.setStyle("Fusion")
    
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)

    app.setPalette(dark_palette)
    
    app.setStyleSheet("""
        QWidget {
            background-color: #353535;
        }
        QLineEdit {
            background-color: #2d2d2d;
            color: white;
            border: 1px solid #444444;
            padding: 5px;
        }
        QComboBox {
            background-color: #2d2d2d;
            color: white;
            border: 1px solid #444444;
        }
        QComboBox::drop-down {
            background-color: #444444;
            border: none;
        }
        QPushButton {
            background-color: #5a5a5a;
            color: white;
            border: 1px solid #444444;
            padding: 5px 10px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #777777;
        }
        QPushButton:pressed {
            background-color: #333333;
        }
    """)

def setAppIcon(app):
    appIcon = QIcon('assets/logo.png')
    app.setWindowIcon(appIcon)


##################### Main Programme Function
if __name__ == '__main__':
    
    # Start QApplication
    mainApp = QApplication([])
    setAppDarkMode(mainApp)
    setAppIcon(mainApp)
    
    # Create main window
    mainWin = mainWindow()
    mainWin.installEventFilter(mainWin)
    
    # Start event loop
    mainApp.exec()
