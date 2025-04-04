"""
Grupo I, IAD, 2025
João Camacho, Duarte Tavares, Margarida Saraiva, Jorge Costa



"""
### Imports
from src.Astrolocator import Astrolocator
from src.StepperController import StepperController

### Class
class Tracker():
    # Constructor
    def __init__(self, lat, lon, alt=0):
        self.aloc = Astrolocator()
        self.motors = StepperController()


        self.lat=lat
        self.lon=lon
        self.alt=alt

        self.alignmentPoints = []
        self.currAlignmentType = "None"
        self.currAlignment = None

    
    def addAlignmentPoint(self, name):
        currTime = self.aloc.getTime()
        realPos = self.aloc.getAzAlt(name, self.lat, self.lon, self.alt, currTime)
        motorPos = self.motors.getCoords()
        info = (name, self.lat, self.lon, self.alt, currTime)
        self.aligmentPoints.append((realPos, motorPos,info))
        

    def nearestAlign(self, motorAz=0, motorAlt=0):
        dist = -1 
        nearestObject = None
        for aligner in self.alignmentPoints:
            currDist = aligner[1][0]*aligner[1][0] + aligner[1][1]*aligner[1][1]
            if dist < currDist:
                dist = currDist
                nearestObject = aligner
        if nearestObject:
            self.currAlignmentType = "Nearest"
            self.currAlignment = (aligner[1][0]-aligner[0][0], aligner[1][1]-aligner[0][1])

        
    def realToMotor(self, realPos):
        if self.currAlignmentType == "None":
            return realPos 
        if self.currAlignmentType == "Nearest":
            return (realPos[0] + self.currAlignment[0], realPos[1] + self.currAlignment[1])

    def motorToReal(self, motorPos):
        if self.currAlignmentType == "None":
            return motorPos 
        if self.currAlignmentType == "Neasrest":
            return (motorPos[0] - self.currAlignment[0], motorPos[1] - self.currAlignment[1])
