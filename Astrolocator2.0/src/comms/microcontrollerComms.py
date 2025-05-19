"""
Duarte Tavares, João Camacho, Jorge Costa, Margarida Saraiva
IST, 2025 - IAD

This file contains all communication capabilities. Updated by João Camacho.

"""

##################### Imports
import serial
import serial.tools.list_ports
import time

##################### Microcontroller Communication Class
class microcontrollerComms:

    # Initialize class - report to main window.
    def __init__(self, mainWindow):

        self.mainWindow = mainWindow
        
        self.mainWindow.logText('> Setting up micontrollerComms Object ...\n')
        
        # Signal that communications are occupied with a thread
        self.occupied = False

        # Communication specifications
        self.serialObject = serial.Serial()
        self.serialObject.baudrate = 115200
        self.serialObject.timeout = None
        
        # Timeout if reading goes on for too long
        self.timeoutSeconds = 1

        # List ports in the status msg
        self.mainWindow.logText("> Available Ports: "+self.listPorts())

        # Find valid ports
        self.validPorts = [port for port in self.systemDevices]
        try:
            self.serialObject.port = self.validPorts[0]
        except:
            self.mainWindow.logText('> WARNING: No ports found!\n')
        if len(self.validPorts) > 1:
            self.mainWindow.logText('> WARNING: Multiple valid ports found! Defaulted to first port!\n')
        self.mainWindow.logText("> Selected Device: "+self.selectedPortStr()+'.\n')
        self.mainWindow.logText(self.tryOpeningIntToStr(self.tryOpening()))
        self.mainWindow.logText('> Finished communication setup!\n')
    
    # Changes port for communication, reports to main window.
    def changePort(self, port):
        self.listPorts()
        if port in self.systemDevices:
            try:
                self.serialObject.port = port
                self.mainWindow.logText("> Changed port to \'"+self.selectedPortStr()+"\'\n")
            except:
                self.mainWindow.logText("> ERROR: Port is permitted but not available!?")
        else:
            self.mainWindow.logText("> ERROR: Port is not in the list of permitted ports! Permitted ports are: "+self.systemPortsStr()+".\n")

    # Returns available ports in message format.
    def listPorts(self):
       self.systemDevices = [port.device for port in serial.tools.list_ports.comports()]
       return self.systemPortsStr()+'\n'

    # Make a list of the system available ports, return string.
    def systemPortsStr(self):
        msg = ""
        for port in self.systemDevices:
            msg += "["+str(port)+'] '
        if msg == "":
            return "None"
        return msg

    # Returns the string of the selected port
    def selectedPortStr(self):
        return str(self.serialObject.port)

    # Checks if serial is open for communication
    def isOpen(self):
        return self.serialObject.isOpen()

    # Try opening, return status error int code depending.
    def tryOpening(self):
        try:
            if not self.isOpen():
                self.serialObject.open()
        except:
            return 1
        return 0
    
    # Turn tryOpening status into a string explaining the error.
    def tryOpeningIntToStr(self,error):
        if error == 0:
            return "> Successfully opened port \'"+self.selectedPortStr()+"\'.\n"
        elif error == 1:
            return "> ERROR: Could not open serial port! Port may be busy/invalid!\n"

    # Closes the communication port.
    def closePort(self):
        self.serialObject.close()

    # Write message onto the microcontroller. Return operation msg.
    def writeMessage(self,msg):
        # Check Connection
        tryOpen = self.tryOpening()
        if tryOpen != 0:
            return self.tryOpeningIntToStr(tryOpen)
        # Send
        try:
            self.serialObject.write((msg+'\n').encode('utf-8'))
        except:
            return "> FATAL ERROR: Device access is forbidden!\n"
        return "> Sent the message: \'"+msg+"\' to the microcontroller Port.\n"

    # Read a message from the microcontroller. Return the received message.
    def readMessage(self):
        # Check connection
        tryOpen = self.tryOpening()
        if tryOpen != 0:
            return self.tryOpeningIntToStr(tryOpen)
        # Keep reading until there is something; checking for timeouts
        message = ""
        start_time = time.time()
        while (len(message) == 0 or message[-1] != '\n') and time.time()-start_time <= self.timeoutSeconds:
            
            try:
                self.serialObject.inWaiting()
            except:
                return "> FATAL ERROR: Device access is forbidden!\n"

            while self.serialObject.inWaiting() > 0 :
                message += self.serialObject.read(1).decode('utf-8')

        
        if time.time()-start_time >= self.timeoutSeconds:
            return "> TIMEOUT! ("+str(time.time()-start_time)+" seconds).\n"
        
        return message 

    # Send a command; uses read and write. Waits until the comm channel is unoccupied.
    def writeAndRead(self, cmd):
        # Wait until the channel is unoccupied; Timeout
        start_time = time.time()
        while self.occupied and time.time()-start_time <= self.timeoutSeconds:
            pass
        if time.time()-start_time >= self.timeoutSeconds:
            return (writeMsg, "> TIMEOUT! ("+str(time.time()-start_time)+" seconds).\n")
        # Signal occupation, send message, receive message, free communication
        self.occupied = True 
        writeMsg = self.writeMessage(cmd)
        readMsg = self.readMessage()
        self.occupied = False
        # Finished
        return (writeMsg, readMsg)