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
        self.alignmentPoints.append((realPos, motorPos,info))

    def nearestOnePointAlign(self, motorAz=0, motorAlt=0):
        dist = -1 
        nearestObject = None
        for aligner in self.alignmentPoints:
            currDist = (aligner[1][0]-motorAz)*(aligner[1][0]-motorAz) + (aligner[1][1]-motorAlt)*(aligner[1][1]-motorAlt)
            if dist < currDist:
                dist = currDist
                nearestObject = aligner
        if nearestObject:
            self.currAlignmentType = "NearestOnePoint"
            self.currAlignment = (aligner[1][0]-aligner[0][0], aligner[1][1]-aligner[0][1])
        
    def realToMotor(self, realPos):
        if self.currAlignmentType == "None":
            return realPos 
        if self.currAlignmentType == "NearestOnePoint":
            return (realPos[0] + self.currAlignment[0], realPos[1] + self.currAlignment[1])
        if self.currAlignmentType == "NPoint":
            realPos = np.array(realPos)
            return astroalign.matrix_transform(realPos, self.currAlignment[1].params)
    
    def motorToReal(self, motorPos):
        if self.currAlignmentType == "None":
            return motorPos 
        if self.currAlignmentType == "NearestOnePoint":
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
        src = np.array(src)
        sky = np.array(sky)
        self.currAlignmentType = "NPoint"
        self.currAlignment = (astroalign.estimate_transform('affine', src, sky), astroalign.estimate_transform('affine', sky, src))

    def trackingRoutine(self, params ,signalPoint):
        objName = params[0]
        self.interruptTracking = False
        trackObj = self.aloc.querySimbad(objName)
        while self.interruptTracking == False:
            currTime = self.aloc.getTime()
            realPos = self.aloc.getAzAlt(trackObj, currTime)
            self.motors.moveTo(self.realToMotor(realPos))
            signalPoint.emit(realPos)

    def telecopeRoutine(self, params ,signalPoint):
        sensor = RPiCamera2()
        fileName = params[0]
        exposure = params[1]
        gain = params[2]
        frameTime = params[3]
        fps = 1/max(exposure, frameTime)
        sensor.changeSettings(framerate=fps, exposureTime=exposure, analogueGain=gain)
        self.interruptTracking = False
        sensor.start_video(fileName)
        while self.interruptTracking == False:
            time.sleep(0.01)
        sensor.end_video()

    def antennaRoutine(self, params ,signalPoint):
        graphWindow = params[0]
        sampleRate = params[1]
        centerFreq = params[2]
        gain = params[3]
        sdr = RTLSDRInterface(sampleRate,centerFreq,gain)
        while self.interruptTracking == False:
            sdr.calculate_plot_psd(graphWindow)