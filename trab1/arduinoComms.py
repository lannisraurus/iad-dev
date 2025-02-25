# For USB communication.
import serial
import serial.tools.list_ports

class arduinoComms:

    # Init
    def initialize(self):
        msg = "* Setting up arduino communication...\n"
        self.serialObject = serial.Serial()
        self.systemDevices = [port.device for port in serial.tools.list_ports.comports()]
        self.validPorts = [port for port in self.systemDevices if port in ['/dev/ttyACM0','/dev/ttyUSB0']]
        try:
            self.serialObject.port = self.validPorts[0]
        except:
            msg += "* WARNING: No valid ports found!\n"
        if len(self.validPorts) != 1:
            msg += "* WARNING: Multiple valid ports found! Defaulted to first port.\n"
        msg += "* Available Devices: "+self.systemPortsStr()+'.\n'
        msg += "* Selected Device: "+self.selectedPortStr()+'.\n'       
        return msg+"* Finished arduino communication setup.\n"


    def selectedPortStr(self):
        return str(self.serialObject.port)

    def systemPortsStr(self):
        msg = ""
        for port in self.systemDevices:
            msg += "["+str(port)+'] '
        if msg == "":
            return "None"
        return msg

    def isOpen(self):
        return self.serialObject.isOpen()
    
    def tryOpening(self):
        try:
            if not self.isOpen():
                self.serialObject.open()
        except:
            return "* ERROR: Could not open serial port! Port may be busy...\n"
