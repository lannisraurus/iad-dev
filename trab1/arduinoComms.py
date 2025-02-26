# For USB communication.
import serial
import serial.tools.list_ports

class arduinoComms:

    # Init
    def initialize(self):
        msg = "* Setting up arduino communication...\n"
        self.serialObject = serial.Serial()
        self.serialObject.baudrate = 9600
        self.serialObject.timeout = 1
        msg += self.listPorts()
        self.validPorts = [port for port in self.systemDevices if port in ['/dev/ttyACM0','/dev/ttyUSB0']]
        try:
            self.serialObject.port = self.validPorts[0]
        except:
            msg += "* WARNING: No valid ports found!\n"
        if len(self.validPorts) > 1:
            msg += "* WARNING: Multiple valid ports found! Defaulted to first port.\n"
        msg += "* Selected Device: "+self.selectedPortStr()+'.\n'       
        return msg+"* Finished arduino communication setup.\n"

    def listPorts(self):
       self.systemDevices = [port.device for port in serial.tools.list_ports.comports()]
       return "* Available Devices: "+self.systemPortsStr()+'.\n'

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
            return 1
        return 0
    
    def tryOpeningIntToStr(self,error):
        if error == 0:
            return "* Successfully opened port \'"+self.selectedPortStr()+".\'\n"
        elif error == 1:
            return "* ERROR: Could not open serial port! Port may be busy/invalid!\n"

    def changePort(self, port):
        if port in self.systemDevices:
            self.serialObject.port = port
            return "* Changed port to \'"+self.selectedPortStr()+"\'\n"
        else:
            return "* ERROR: Port is not in the list of permitted ports! Permitted ports are: "+self.systemPortsStr()+".\n"

    def writeMessage(self,msg):
        tryOpen = self.tryOpening()
        if tryOpen != 0:
            return self.tryOpeningIntToStr(tryOpen)
        self.serialObject.write(msg.encode('utf-8'))
        return "* Sent the message: \'"+msg+"\' to the Arduino Port.\n"

    def readMessage(self):
        tryOpen = self.tryOpening()
        if tryOpen != 0:
            return self.tryOpeningIntToStr(tryOpen)
        message = ""
        while self.serialObject.in_waiting < 0:
            message += self.serialObject.readline().decode('utf-8').rstrip()
        return message    

