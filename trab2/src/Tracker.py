"""
Grupo I, IAD, 2025
João Camacho, Duarte Tavares, Margarida Saraiva, Jorge Costa

This file contains a class to coordinate StepperController and
Astrolocator.

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

    def addAlignmentPoint(self, realPos, name=""):
        currTime = self.aloc.getTime()
        motorPos = self.motors.getCoords()
        info = (self.lat, self.lon, self.alt, currTime, name)
        alignmentPoint = (realPos, motorPos,info)
        #print(alignmentPoint)
        self.alignmentPoints.append(alignmentPoint)

    def onePointAlign(self):
        """dist = -1 
        nearestObject = None
        for aligner in self.alignmentPoints:
            currDist = (aligner[1][0]-motorAz)*(aligner[1][0]-motorAz) + (aligner[1][1]-motorAlt)*(aligner[1][1]-motorAlt)
            if dist < currDist:
                dist = currDist
                nearestObject = aligner
        if nearestObject:
            
            SE ESTIVER TD BEM TIRAR COMENTÁRIO
            """
        self.currAlignmentType = "OnePoint"
        aligner = self.alignmentPoints[0]
        self.currAlignment = (aligner[1][0]-aligner[0][0], aligner[1][1]-aligner[0][1])
        
    def realToMotor(self, realPos):
        if self.currAlignmentType == "None":
            return realPos 
        if self.currAlignmentType == "OnePoint":
            return (realPos[0] + self.currAlignment[0], realPos[1] + self.currAlignment[1])
        if self.currAlignmentType == "NPoint":
            realPos = np.array(realPos)
            return astroalign.matrix_transform(realPos, self.currAlignment[1].params)
    
    def motorToReal(self, motorPos):
        if self.currAlignmentType == "None":
            return motorPos 
        if self.currAlignmentType == "OnePoint":
            return (motorPos[0] - self.currAlignment[0], motorPos[1] - self.currAlignment[1])
        if self.currAlignmentType == "NPoint":
            motorPos = np.array(motorPos)
            return astroalign.matrix_transform(motorPos, self.currAlignment[0].params)

    def pointAlignment(self, npoint):
        src = []
        sky = []
        i = 0
        for i in npoint-1:
            src.append(self.alignmentPoints[i][1])
            sky.append(self.alignmentPoints[i][0])
            i = i+1
        src = np.array(src)
        sky = np.array(sky)
        self.currAlignmentType = "NPoint"
        self.currAlignment = (astroalign.estimate_transform('affine', src, sky), astroalign.estimate_transform('affine', sky, src))

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
