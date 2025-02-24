# For USB communication.
import serial
import serial.tools.list_ports

class serialComms:

    # Constructor
    def __init__(self):
        self.serialObject = serial.Serial()
        self.systemPorts = list(serial.tools.list_ports.comports())
        print(self.systemPorts)
        self.usbPorts = [port for port in self.systemPorts if 'USB' in port.description]
        print(len(self.systemPorts))
        self.serialObject.port = self.usbPorts[0]

    def selectedPortStr(self):
        return self.serialObject.portstr

    def usbPortsList(self):
        return self.usbPorts

    def isOpen(self):
        return self.serialObject.isOpen()
    
    def throwExceptions(self):
        msg = ''
        if not self.isOpen():
            msg += "ERROR: Could not open Serial Port "+self.serialObject.portstr+". Try re-defining the port using [COMMAND HERE]\n"
        return msg
