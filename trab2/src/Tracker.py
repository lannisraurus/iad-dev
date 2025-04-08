"""
Grupo I, IAD, 2025
João Camacho, Duarte Tavares, Margarida Saraiva, Jorge Costa



"""
### Imports
from src.Astrolocator import Astrolocator
from src.StepperController import StepperController
import astroalign

### Class
class Tracker():
    # Constructor
    def __init__(self,  stepperController, lat=90, lon=0, alt=0):
        self.aloc = Astrolocator()
        self.motors = stepperController

        self.lat=lat
        self.lon=lon
        self.alt=alt

        self.alignmentPoints = []
        self.currAlignmentType = "None"
        self.currAlignment = None

        self.trackingInterrupt = False

    # After 
    def addAlignmentPoint(self, name):
        currTime = self.aloc.getTime()
        realPos = self.aloc.getAzAlt(name, self.lat, self.lon, self.alt, currTime) #returns (az, alt)
        motorPos = self.motors.getCoords()
        info = (name, self.lat, self.lon, self.alt, currTime)
        self.alignmentPoints.append((realPos, motorPos,info))

    def nearestOnePointAlign(self, motorAz=0, motorAlt=0):
        dist = -1 
        nearestObject = None
        for aligner in self.alignmentPoints:
            currDist = aligner[1][0]*aligner[1][0] + aligner[1][1]*aligner[1][1]
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
            return astroalign.matrixtransform(realPos, self.currAlignment[1].params)
    
    def motorToReal(self, motorPos):
        if self.currAlignmentType == "None":
            return motorPos 
        if self.currAlignmentType == "NearestOnePoint":
            return (motorPos[0] - self.currAlignment[0], motorPos[1] - self.currAlignment[1])
        if self.currAlignmentType == "NPoint":
            return astroalign.matrixtransform(motorPos, self.currAlignment[0].params)

    def pointAlignment(self, npoint):
        i = 0
        for i in npoint-1:
            src = self.alignmentPoints[i][1]
            sky = self.alignmentPoints[i][0]
        self.currAlignmentType = "NPoint"
        self.currAlignment = (astroalign.estimate_transform('affine', src, sky), astroalign.estimate_transform('affine', sky, src))

    def trackingRoutine(self, params ,signalPoint):
        print("AAAAAA")
        objName = params[0]
        self.stopTracking = False
        while self.stopTracking == False:
            currTime = self.aloc.getTime()
            realPos = self.aloc.getAzAlt(objName, self.lat, self.lon, self.alt, currTime)
            self.motors.moveTo(self.realToMotor(realPos))
            signalPoint.emit(realPos)