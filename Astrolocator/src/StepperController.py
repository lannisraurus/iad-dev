"""
Grupo I, IAD, 2025
João Camacho, Duarte Tavares, Margarida Saraiva, Jorge Costa

This file contains various methods to interface with the RB Moto2
driver, and control the angles of the 28BYJ-48 step motors.

"""

### Imports
try:
    from gpiozero import OutputDevice
except:
    print('ERROR in StepperController: Could not import gpiozero! Please install!')
import time

### Class Definition
class StepperController():

    ########################################################## Constructor
    def __init__(self, settings, mainWindow, alt = 0, az = 0):
        
        # Default
        self.working = False
        self.angleLock = False
        self.minAz = 0
        self.minAlt = 0
        self.maxAz = 0
        self.maxAlt = 0

        # Log
        mainWindow.logText('> Configuring StepperController Object...\n')

        # Set motor type
        self.motorType = settings[0]
        mainWindow.logText('> Initializing motor type '+self.motorType+'\n')

        # RB-MOTO2 (Joy-IT)
        if self.motorType == 'RB-MOTO2 (Joy-IT)':

            # Vars
            self.working = True

            # Steps in 360 deg
            self.stepsInRevolution = 512

            # Sequence Size
            self.stepsInSequence = 8

            # Step sequence
            mainWindow.logText('> Setting sequences...\n')
            self.Seq = list(range(0, self.stepsInSequence))
            self.Seq[0] = [0,1,0,0]
            self.Seq[1] = [0,1,0,1]
            self.Seq[2] = [0,0,0,1]
            self.Seq[3] = [1,0,0,1]
            self.Seq[4] = [1,0,0,0]
            self.Seq[5] = [1,0,1,0] 
            self.Seq[6] = [0,0,1,0]
            self.Seq[7] = [0,1,1,0]
            
            # Pins
            mainWindow.logText('> Extracting pin information...\n')
            pins = settings[1]
            pins = pins.split(' ')
            if len(pins) == self.stepsInSequence:
                try:
                    self.coil_A_1_pin = OutputDevice(int(pins[0])) # pink
                    self.coil_A_2_pin = OutputDevice(int(pins[1]))  # orange
                    self.coil_B_1_pin = OutputDevice(int(pins[2])) # blue
                    self.coil_B_2_pin = OutputDevice(int(pins[3])) # yellow
                    self.coil2_A_1_pin = OutputDevice(int(pins[4])) # pink
                    self.coil2_A_2_pin = OutputDevice(int(pins[5])) # orange
                    self.coil2_B_1_pin = OutputDevice(int(pins[6])) # blue
                    self.coil2_B_2_pin = OutputDevice(int(pins[7])) # yellow
                except:
                    self.working = False
                    mainWindow.logText('> ERROR! Could not set output pins! Either the pins are not ints, or your device cannot access the GPIO pins!\n')
            else:
                self.working = False
                mainWindow.logText('> ERROR! Pin configuration is wrong! These should be 8!\n')

        # Gear Ratio
        mainWindow.logText('> Configuring mount gear ratio...\n')
        self.gearRatio = settings[2]
        mainWindow.logText('> Finished StepperController Object configuration.\n\n')

        # Set current step count
        self.centerCoords(az,alt)

    def __del__(self):
        if hasattr(self, 'coil_A_1_pin'): self.coil_A_1_pin = None
        if hasattr(self, 'coil_A_2_pin'): self.coil_A_2_pin = None
        if hasattr(self, 'coil_B_1_pin'): self.coil_B_1_pin = None
        if hasattr(self, 'coil_B_2_pin'): self.coil_B_2_pin = None
        if hasattr(self, 'coil2_A_1_pin'): self.coil2_A_1_pin = None
        if hasattr(self, 'coil2_A_2_pin'): self.coil2_A_2_pin = None
        if hasattr(self, 'coil2_B_1_pin'): self.coil2_B_1_pin = None
        if hasattr(self, 'coil2_B_2_pin'): self.coil2_B_2_pin = None

    ########################################################## Angle Locking

    def setAngleLock(self, boolean):
        self.angleLock = boolean
    
    def limitAngles(self, minAz, maxAz, minAlt, maxAlt):
        self.minAz = self.degToSteps(minAz)
        self.maxAz = self.degToSteps(maxAz)
        self.minAlt = self.degToSteps(minAlt)
        self.maxAlt = self.degToSteps(maxAlt)
    
    def checkIfWithinLimits(self, azIncrement, altIncrement):
        result = True
        if self.az+azIncrement > self.maxAz:
            result = False
        if self.az+azIncrement < self.minAz:
            result = False
        if self.alt+altIncrement > self.maxAlt:
            result = False
        if self.alt+altIncrement < self.minAlt:
            result = False
        return result

    ########################################################## Conversions

    # Convert degrees to stepper steps
    def degToSteps(self,angleDeg):
        if not self.working:
            return 'ERR'
        return round(self.stepsInRevolution*self.stepsInSequence*self.gearRatio*angleDeg/360)

    def stepsToDeg(self,angleSteps):
        if not self.working:
            return 'ERR'
        return 360*angleSteps/self.stepsInRevolution/self.stepsInSequence/self.gearRatio

    ########################################################## Stepping Operations

    # Azimuthal Stepping
    def stepAz(self,indexSeq):
        if not self.working:
            return
        self.coil_A_1_pin.value = self.Seq[indexSeq][0]
        self.coil_A_2_pin.value = self.Seq[indexSeq][1]
        self.coil_B_1_pin.value = self.Seq[indexSeq][2]
        self.coil_B_2_pin.value = self.Seq[indexSeq][3]

     # Altitude Stepping
    def stepAlt(self,indexSeq):
        if not self.working:
            return
        self.coil2_A_1_pin.value = self.Seq[indexSeq][0]
        self.coil2_A_2_pin.value = self.Seq[indexSeq][1]
        self.coil2_B_1_pin.value = self.Seq[indexSeq][2]
        self.coil2_B_2_pin.value = self.Seq[indexSeq][3]
    
    ########################################################## Moving Operations - Threadable

    # Azimuthal threaded rotation
    def moveAz(self, reverse=False, delay=0.001):

        if not self.working:
            time.sleep(delay)
            return
        
        if not reverse:
            azIncrement = 1
        else:
            azIncrement = -1
        
        if not self.checkIfWithinLimits(azIncrement, 0) and self.angleLock:
            return

        self.stepAz((self.stepsInSequence-self.az)%self.stepsInSequence)
        self.az += azIncrement
            
        time.sleep(delay)
        

    # Azimuthal threaded rotation
    def moveAlt(self, reverse=False, delay=0.001):

        if not self.working:
            time.sleep(delay)
            return

        if not reverse:
            altIncrement = 1
        else:
            altIncrement = -1
        
        if not self.checkIfWithinLimits(0, altIncrement) and self.angleLock:
            return

        self.stepAlt((self.stepsInSequence-self.alt)%self.stepsInSequence)
        self.alt += altIncrement
        
        time.sleep(delay)

    ########################################################## REVIEW ALL THIS CODE TO BE CONCORDANT WITH THE PREV!!!

    ########################################################## Moving Operations - Specific Angle

    # Azimuthal full rotation
    def moveToAz(self, azDeg, delay=0.001):
        if not self.working:
            time.sleep(delay)
            return
        
        az=self.degToSteps(azDeg)
        direction = (1 if self.az < az else -1)
        for i in range(self.az,az, direction):
            if (not (self.az + direction > self.maxAz or self.az + direction < self.minAz)) or (not self.angleLock):
                self.stepAz((self.stepsInSequence-i)%self.stepsInSequence)
            time.sleep(delay)
        self.az=az
    
    # Altitude full rotation
    def moveToAlt(self, altDeg, delay=0.001):
        if not self.working:
            time.sleep(delay)
            return
        
        alt=self.degToSteps(altDeg)
        direction = (1 if self.alt < alt else -1)
        for i in range(self.alt,alt, direction):
            if (not (self.alt + direction > self.maxAlt or self.alt + direction < self.minAlt)) or (not self.angleLock):
                self.stepAlt((self.stepsInSequence-i)%self.stepsInSequence)
            time.sleep(delay)
        self.alt=alt

    ########################################################## Setters

    # Set azimuth and altitude current steps from degrees
    def centerCoords(self, azDeg, altDeg):
        if not self.working:
            return
        self.az = self.degToSteps(azDeg)
        self.alt = self.degToSteps(altDeg)

    ########################################################## Getters

    # Set azimuth and altitude current steps from degrees
    def getCoords(self):
        if not self.working:
            return ('ERR', 'ERR')
        return (float(self.stepsToDeg(self.az)),float(self.stepsToDeg(self.alt)))
