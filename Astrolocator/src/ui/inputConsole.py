"""
Duarte Tavares, João Camacho, Jorge Costa, Margarida Saraiva
IST, 2025 - IAD

This file contains the inputConsole, used in the main window.
the input console can detect inputs and take in written text from the
keyboard. It also has the capacity to save previous commands in a file
and load them up.

"""
##################### Imports
from PyQt5.QtCore import *      # Basic Qt functionalities.
from PyQt5.QtWidgets import *   # GUI windows
from PyQt5.QtCore import *      # Qt threads, ...
from PyQt5.QtGui import *       # GUI Elements

##################### Input console class
class inputConsole(QLineEdit):

    # Constructor
    def __init__(self,logPath,mainWin,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # Working vars
        self.currentText = ""
        self.index = 0
        self.lines = [""]
        self.logPath = logPath
        # load log from previous sessions
        self.loadLog()
        self.mainWin = mainWin

    # Reset index of the list; called after employing command.
    def resetIndex(self):
        self.index = 0

    # Add an empty line; called after employing command.
    def addLine(self):
        self.lines.insert(0,"")

    # Clear all lines.
    def clearLines(self):
        self.lines = [""]

    # Set most recent line to a cmd; called after employing command.
    def setFinal(self, cmd):
        self.lines[0] = cmd

    # key press events; used for detecting going up and down the list.
    def keyPressEvent(self,event):
        key = event.key()
        self.lines[self.index] = self.text()
        if key == Qt.Key_Up:
            if self.index < len(self.lines)-1:
                self.index += 1
                self.setText(self.lines[self.index])
        elif key == Qt.Key_Down:
            if self.index > 0:
                self.index -= 1
                self.setText(self.lines[self.index])
        super().keyPressEvent(event)
    
    # Save a log to the defined path.
    def saveLog(self):
        with open(self.logPath,'w') as file:
            for elem in self.lines:
                if elem != "" and not elem.isspace():
                    file.write(elem+'\n')

    # Load log from the defined path.
    def loadLog(self):
        with open(self.logPath, 'r') as file:
            for line in file:
                self.lines.append(line.strip())