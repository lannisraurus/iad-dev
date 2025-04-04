"""
Grupo I, IAD, 2025
João Camacho, Duarte Tavares, Margarida Saraiva, Jorge Costa

This file contains various methods to interface with the RB Moto2
driver, and control the angles of the 28BYJ-48 step motors.

"""

### Imports
from gpiozero import OutputDevice
import time

### Class Definition
class StepperController():

    # Constructor
    def __init__(self, alt = 0, az = 0): 

        # Define motor driver pins
        self.coil_A_1_pin = OutputDevice(24) # pink
        self.coil_A_2_pin = OutputDevice(4)  # orange
        self.coil_B_1_pin = OutputDevice(23) # blue
        self.coil_B_2_pin = OutputDevice(25) # yellow
        self.coil2_A_1_pin = OutputDevice(18) # pink
        self.coil2_A_2_pin = OutputDevice(22) # orange
        self.coil2_B_1_pin = OutputDevice(17) # blue
        self.coil2_B_2_pin = OutputDevice(27) # yellow

        # Step sequence
        self.Seq = list(range(0, 8))
        self.Seq[0] = [0,1,0,0]
        self.Seq[1] = [0,1,0,1]
        self.Seq[2] = [0,0,0,1]
        self.Seq[3] = [1,0,0,1]
        self.Seq[4] = [1,0,0,0]
        self.Seq[5] = [1,0,1,0] 
        self.Seq[6] = [0,0,1,0]
        self.Seq[7] = [0,1,1,0]

        # Set current step count
        self.centerCoords(az,alt)

    # Convert degrees to stepper steps
    def degToSteps(self,angleDeg):
        return round(512*8*32*angleDeg/360)

    # Azimuthal Stepping
    def stepAz(self,indexSeq):
        self.coil_A_1_pin.value = self.Seq[indexSeq][0]
        self.coil_A_2_pin.value = self.Seq[indexSeq][1]
        self.coil_B_1_pin.value = self.Seq[indexSeq][2]
        self.coil_B_2_pin.value = self.Seq[indexSeq][3]

     # Altitude Stepping
    def stepAlt(self,indexSeq):
        self.coil2_A_1_pin.value = self.Seq[indexSeq][0]
        self.coil2_A_2_pin.value = self.Seq[indexSeq][1]
        self.coil2_B_1_pin.value = self.Seq[indexSeq][2]
        self.coil2_B_2_pin.value = self.Seq[indexSeq][3]
    
    # Azimuthal full rotation
    def moveToAz(self, azDeg, delay=0.001):
        az=self.degToSteps(azDeg)
        for i in range(self.az,az, 1 if self.az < az else -1):
            self.stepAz((8-i)%8)
            time.sleep(delay)
        self.az=az
    
    # Altitude full rotation
    def moveToAlt(self, altDeg, delay=0.001):
        alt=self.degToSteps(altDeg)
        for i in range(self.alt,alt, 1 if self.alt < alt else -1):
            self.stepAlt(i%8)
            time.sleep(delay)   
        self.alt=alt  

    # Altitude+Azimuth full rotation
    def moveTo(self, azDeg, altDeg, delay=0.001):

        az = self.degToSteps(azDeg)
        alt = self.degToSteps(altDeg)

        azStepCount = 0
        altStepCount = 0

        while azStepCount < self.az or altStepCount < self.alt:

            if azStepCount < abs(self.az - az):
                azStep = (8-azStepCount)%8
                if self.az >= az:
                    azStep = azStepCount%8
                self.stepAz(azStep)
            
            if altStepCount < abs(self.alt- alt):
                altStep = altStepCount%8
                if self.alt >= alt:
                    altStep = (8-altStepCount)%8
                self.stepAlt(altStep)
            
            azStepCount += 1
            altStepCount += 1
            time.sleep(delay)
        
        self.az = az
        self.alt = alt

    # Set azimuth and altitude current steps from degrees
    def centerCoords(self, azDeg, altDeg):
        self.az = self.degToSteps(azDeg)
        self.alt = self.degToSteps(altDeg)

