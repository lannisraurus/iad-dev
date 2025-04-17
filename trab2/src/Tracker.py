"""
Grupo I, IAD, 2025
João Camacho, Duarte Tavares, Margarida Saraiva, Jorge Costa

This file contains a class to coordinate StepperController and
Astrolocator; the class also does the correspondence between to coordinate
systems: the coordinates of the motor and the coordinates of the sky.

"""
### Imports
from src.Astrolocator import Astrolocator
from src.StepperController import StepperController
from src.Camera import RPiCamera2
from src.RTLSDR import RTLSDRInterface

import astroalign
import numpy as np
import time

### Class
class Tracker():
    # Constructor
    def __init__(self,  stepperController, lat=90, lon=0, alt=0):
        self.aloc = Astrolocator(lat, lon, alt)
        self.motors = stepperController

        self.lat=lat
        self.lon=lon
        self.alt=alt

        self.alignmentPoints = []
        self.currAlignmentType = "None"
        self.currAlignment = None

        self.interruptTracking = False

    #Alignment Point - coordinates of the motor and the correspondent coordinates in the sky
    def addAlignmentPoint(self, realPos, name=""):
        currTime = self.aloc.getTime()
        motorPos = self.motors.getCoords()
        info = (self.lat, self.lon, self.alt, currTime, name)
        alignmentPoint = (realPos, motorPos,info)
        self.alignmentPoints.append(alignmentPoint)

    #Alignment for 1 Point Alignmet
    def onePointAlign(self):
        self.currAlignmentType = "OnePoint"
        aligner = self.alignmentPoints[0]
        self.currAlignment = (aligner[1][0]-aligner[0][0], aligner[1][1]-aligner[0][1])
        
     #Alignment for N point alignment
    def pointAlignment(self):
        src = []
        sky = []
        for i in range(len(self.alignmentPoints)):
            src.append(self.alignmentPoints[i][1])
            sky.append(self.alignmentPoints[i][0])
        src = np.array(src)
        sky = np.array(sky)
        self.currAlignmentType = "NPoint"
        self.currAlignment = (astroalign.estimate_transform('affine', src, sky), astroalign.estimate_transform('affine', sky, src))
    
    #Change coordinates to preferred system
    def realToMotor(self, realPos):
        if self.currAlignmentType == "None":
            return realPos 
        if self.currAlignmentType == "OnePoint":
            return (realPos[0] + self.currAlignment[0], realPos[1] + self.currAlignment[1])
        if self.currAlignmentType == "NPoint":
            realPos = np.array(realPos)
            result =  astroalign.matrix_transform(realPos, self.currAlignment[1].params)
            result = result.tolist()
            return result[0]
    
    def motorToReal(self, motorPos):
        if self.currAlignmentType == "None":
            return motorPos 
        if self.currAlignmentType == "OnePoint":
            return (motorPos[0] - self.currAlignment[0], motorPos[1] - self.currAlignment[1])
        if self.currAlignmentType == "NPoint":
            motorPosNum = np.array(motorPos)
            result = astroalign.matrix_transform(motorPosNum, self.currAlignment[0].params)
            result = result.tolist()
            print(result,type(result))
            return result[0]

    #Tracking Routine
    def trackingRoutine(self, params ,signalPoint):
        objDatabase = params[0]
        objId = params[1]
        self.interruptTracking = False
        trackObj = None
        while self.interruptTracking == False:
            if objDatabase == "SIMBAD":
                trackObj = self.aloc.querySimbad(objId)
            elif objDatabase == "Horizons":
                trackObj = self.aloc.queryHorizons(objId)
            else:
                trackObj = self.aloc.queryN2YO(objId)
            currTime = self.aloc.getTime()
            realPos = self.aloc.getAzAlt(trackObj, currTime)
            self.motors.moveToAz(self.realToMotor(realPos)[0])
            self.motors.moveToAlt(self.realToMotor(realPos)[1])
            signalPoint.emit(self.motors.getCoords())
            time.sleep(5)
