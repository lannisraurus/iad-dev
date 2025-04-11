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
            self.stepAz((self.stepsInSequence-self.az)%self.stepsInSequence)
            self.az += 1
        else:
            self.stepAz((self.stepsInSequence-self.az)%self.stepsInSequence)
            self.az -= 1
        time.sleep(delay)
        

    # Azimuthal threaded rotation
    def moveAlt(self, reverse=False, delay=0.001):

        if not self.working:
            time.sleep(delay)
            return
        
        if reverse:
            self.stepAlt((self.stepsInSequence-self.alt)%self.stepsInSequence)
            self.alt -= 1
        else:
            self.stepAlt((self.stepsInSequence-self.alt)%self.stepsInSequence)
            self.alt += 1
        time.sleep(delay)

    ########################################################## Moving Operations - Specific Angle

    # Azimuthal full rotation
    def moveToAz(self, azDeg, delay=0.001):
        if not self.working:
            return
        az=self.degToSteps(azDeg)
        for i in range(self.az,az, 1 if self.az < az else -1):
            self.stepAz((self.stepsInSequence-i)%self.stepsInSequence)
            time.sleep(delay)
        self.az=az
    
    # Altitude full rotation
    def moveToAlt(self, altDeg, delay=0.001):
        if not self.working:
            return
        alt=self.degToSteps(altDeg)
        for i in range(self.alt,alt, 1 if self.alt < alt else -1):
            self.stepAlt(i%self.stepsInSequence)
            time.sleep(delay)   
        self.alt=alt  

    # Altitude+Azimuth full rotation
    def moveTo(self, coordDeg, delay=0.001):
        if not self.working:
            return
        az = self.degToSteps(coordDeg[0])
        alt = self.degToSteps(coordDeg[1])

        azStepCount = 0
        altStepCount = 0

        while azStepCount < self.az or altStepCount < self.alt:

            if azStepCount < abs(self.az - az):
                azStep = (self.stepsInSequence-azStepCount)%self.stepsInSequence
                if self.az >= az:
                    azStep = azStepCount%self.stepsInSequence
                self.stepAz(azStep)
            
            if altStepCount < abs(self.alt- alt):
                altStep = altStepCount%self.stepsInSequence
                if self.alt >= alt:
                    altStep = (self.stepsInSequence-altStepCount)%self.stepsInSequence
                self.stepAlt(altStep)
            
            azStepCount += 1
            altStepCount += 1
            time.sleep(delay)
        
        self.az = az
        self.alt = alt

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
