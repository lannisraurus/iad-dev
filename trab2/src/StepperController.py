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
    def __init__(self,initialAlt=0.0,initialAz=0.0):                                         
        # Define motor driver pins
        self.coil_A_1_pin = OutputDevice(24) # pink
        self.coil_A_2_pin = OutputDevice(4)  # orange
        self.coil_B_1_pin = OutputDevice(23) # blue
        self.coil_B_2_pin = OutputDevice(25) # yellow
        self.coil2_A_1_pin = OutputDevice(18) # pink
        self.coil2_A_2_pin = OutputDevice(22) # orange
        self.coil2_B_1_pin = OutputDevice(17) # blue
        self.coil2_B_2_pin = OutputDevice(27) # yellow

        #define steps
        self.Seq = list(range(0, 8))
        self.Seq[0] = [0,1,0,0]
        self.Seq[1] = [0,1,0,1]
        self.Seq[2] = [0,0,0,1]
        self.Seq[3] = [1,0,0,1]
        self.Seq[4] = [1,0,0,0]
        self.Seq[5] = [1,0,1,0] 
        self.Seq[6] = [0,0,1,0]
        self.Seq[7] = [0,1,1,0]

        self.alt = round(512*8*32*initialAlt/360/2)
        self.az = round(512*8*32*initialAz/360/2)

    # lower pins
    def stepAz(self,indexSeq):
        self.coil_A_1_pin.value = self.Seq[indexSeq][0]
        self.coil_A_2_pin.value = self.Seq[indexSeq][1]
        self.coil_B_1_pin.value = self.Seq[indexSeq][2]
        self.coil_B_2_pin.value = self.Seq[indexSeq][3]

     # upper pins
    def stepAlt(self,indexSeq):
        self.coil2_A_1_pin.value = self.Seq[indexSeq][0]
        self.coil2_A_2_pin.value = self.Seq[indexSeq][1]
        self.coil2_B_1_pin.value = self.Seq[indexSeq][2]
        self.coil2_B_2_pin.value = self.Seq[indexSeq][3]
    
    def moveToAz(self, az, delay=0.001):
        az=round(512*8*32*az/360/2)
        for i in range(self.az,az, 1 if self.az < az else -1):
            self.stepAz((8-i)%8)
            time.sleep(delay)
        self.az=az
        
    def moveToAlt(self, alt, delay=0.001):
        az=round(512*8*32*alt/360/2)
        for i in range(self.alt,alt, 1 if self.alt < alt else -1):
            self.stepAlt(i%8)
            time.sleep(delay)   
        self.alt=alt  

    def moveTo(self, az, alt, delay=0.001):
        self.moveToAz(az,delay)
        self.moveToAlt(alt,delay)

    def centerCoords(self, currAz, currAlt):
        self.az = round(currAz)
        self.alt = round(currAlt)

A = StepperController()
#A.moveToAlt(512*8*32,1./1000.)
A.moveToAz(90)
A.moveToAz(-90)
A.moveToAz(90)
A.moveToAz(-90)
A.moveToAz(45)
A.moveToAz(-45)
