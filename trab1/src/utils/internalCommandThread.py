##################### Imports
from PyQt5.QtCore import *  # Qt threads, ...

##################### Internal Command Thread Class
class internalCommandThread(QThread):
    
    finished = pyqtSignal()

    send_data = pyqtSignal(list)
    send_occupied = pyqtSignal(bool)
    
    def __init__(self,obj,func,params):
        super().__init__()
        self.obj = obj
        self.func = func
        self.params = params

    def run(self):
        getattr(self.obj, self.func)(self.params,self.send_data,self.send_occupied)
        self.finished.emit()