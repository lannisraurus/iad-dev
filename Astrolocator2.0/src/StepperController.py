"""
Grupo I, IAD, 2025
João Camacho, Duarte Tavares, Margarida Saraiva, Jorge Costa

This file contains various methods to interface with a microcontroller
which commands stepper motors. Updated code by João Camacho.

"""

### Imports
from src.comms.microcontrollerComms import microcontrollerComms
import time

### Class Definition
class StepperController():

    ########################################################## Constructor
    def __init__(self, mainWindow):
        
        # Logging
        self.mainWindow = mainWindow

        # Log
        mainWindow.logText('> Configuring StepperController Object ...\n')

        # Microcontroller communication setup
        self.comms = microcontrollerComms(mainWindow)

        # Extract settings

        # Step tracking
        self.az = 0
        self.alt = 0

        # Log
        mainWindow.logText('> Finished configuring StepperController Object!\n\n')

    ########################################################## Stepping Operations

    # Stepping function - provide microcontroller command accordingly as defined in its programming. Returns success status
    def step(self, cmd, delay=0.001):
        # Time keeping
        start_time = time.time()
        # Send and receive data.
        result = self.comms.writeAndRead(cmd)[1]
        increments = result.split(' ')
        # Error checking and extraction.
        success = True
        if len(increments) == 2:
            try:
                self.az += int(increments[0])
                self.alt += int(increments[1])
            except:
                success = False
        else:
            success = False
        # Debugging message in case of error.
        if not success:
            return 1
        # Delay
        dt = time.time() - start_time
        if dt < delay:
            time.sleep(delay - dt)
        return 0

    ########################################################## Getters

    # Set azimuth and altitude current steps from degrees
    def getCoords(self):
        return ( float(self.az) , float(self.alt) )
    
    # Set azimuth and altitude current steps from degrees
    def getMicrocontrollerInfo(self):
        return self.comms.writeAndRead("request_commands\n")[1]
    
    def getAvailablePorts(self):
        return self.comms.listPorts()

    def getPort(self):
        return self.comms.selectedPortStr()
    
    ########################################################## Setters

    def setPort(self, port):
        self.comms.changePort(port)
