# -*- coding: utf-8 -*-
from gpiozero import OutputDevice
import time

# Definieren der Pins als OutputDevice-Instanzen
coil_A_1_pin = OutputDevice(24) # pink
coil_A_2_pin = OutputDevice(4)  # orange
coil_B_1_pin = OutputDevice(23) # blue
coil_B_2_pin = OutputDevice(25) # yellow
coil2_A_1_pin = OutputDevice(18) # pink
coil2_A_2_pin = OutputDevice(22) # orange
coil2_B_1_pin = OutputDevice(17) # blue
coil2_B_2_pin = OutputDevice(27) # yellow

StepCount = 8
Seq = list(range(0, StepCount))
Seq[0] = [0,1,0,0]
Seq[1] = [0,1,0,1]
Seq[2] = [0,0,0,1]
Seq[3] = [1,0,0,1]
Seq[4] = [1,0,0,0]
Seq[5] = [1,0,1,0] 
Seq[6] = [0,0,1,0]
Seq[7] = [0,1,1,0]

#upper motor
def setStep2(w1, w2, w3, w4):
    coil_A_1_pin.value = w1
    coil_A_2_pin.value = w2
    coil_B_1_pin.value = w3
    coil_B_2_pin.value = w4

#lower motor
def setStep1(w1, w2, w3, w4):
    coil2_A_1_pin.value = w1
    coil2_A_2_pin.value = w2
    coil2_B_1_pin.value = w3
    coil2_B_2_pin.value = w4

def forward1(delay, steps):
    for i in range(steps):
        for j in range(StepCount):
            setStep1(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)

def backwards1(delay, steps):
    for i in range(steps):
        for j in reversed(range(StepCount)):
            setStep1(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)

def backwards2(delay, steps):
    for i in range(steps):
        for j in reversed(range(StepCount)):
            setStep2(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)
def backwards12(delay, steps):
    for i in range(steps):
        for j in reversed(range(StepCount)):
            setStep1(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            setStep2(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)


#28BYJ-48 stepper has 512 cycles per rev (4096steps per rev)
      
# motor1 512 slow steps forward
delay = 20
steps = 512
# forward1(delay / 1000.0, steps)
# motor1 512 quick steps backwards
delay = 1
steps = round(512*4*100)
backwards12(delay / 1000.0, steps)
