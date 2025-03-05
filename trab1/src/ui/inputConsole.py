"""
Duarte Tavares, João Camacho, Jorge Costa, Margarida Saraiva
IST, 2025 - IAD

This file contains the inputConsole

"""
##################### Imports
from PyQt5.QtCore import *      # Basic Qt functionalities.
from PyQt5.QtWidgets import *   # GUI windows
from PyQt5.QtCore import *      # Qt threads, ...
from PyQt5.QtGui import *       # GUI Elements

##################### Input console class
class inputConsole(QLineEdit):
    def __init__(self,logPath,mainWin,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.currentText = ""
        self.index = 0
        self.lines = [""]
        self.logPath = logPath
        # load log from previous sessions
        self.loadLog()
        self.mainWin = mainWin

    def resetIndex(self):
        self.index = 0

    def addLine(self):
        self.lines.insert(0,"")

    def clearLines(self):
        self.lines = [""]

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
    
    # needed to detect tab click
    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            #autocomplete, currently only for intcmds
            autocomplete = [cmd for cmd in self.mainWin.intCommands.keys() if cmd.startswith(self.text())]
            if len(autocomplete) == 1:
                self.setText(autocomplete[0])
            return True
        return QWidget.event(self, event)

    def saveLog(self):
        with open(self.logPath,'w') as file:
            for elem in self.lines:
                if elem != "" and not elem.isspace():
                    file.write(elem+'\n')

    def loadLog(self):
        with open(self.logPath, 'r') as file:
            for line in file:
                self.lines.append(line.strip())