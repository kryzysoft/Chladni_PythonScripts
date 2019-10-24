import matplotlib.pyplot as plt
import math
import numpy
import sys
import matplotlib.animation as animation

#change to False to see how it's not working
RESONANCE = True
SAVE_TO_FILE = False

class SineWave:
    def __init__(self, startingPoint, direction, startingPhase):
        self.NUM_OF_POINTS = 100
        self.barWidth = 0.2
        self.xStep = self.barWidth / self.NUM_OF_POINTS
        self.xValues = []
        
        self.yValues = [0]*self.NUM_OF_POINTS
        self.yValuesDraw = [0]*self.NUM_OF_POINTS
        if RESONANCE:
            self.waveFrequency = 1000
        else:
            self.waveFrequency = 1150
        self.waveSpeed = 100
        self.waveDirection = direction
        self.startingPoint = startingPoint
        self.startingPhase = startingPhase
        self.reflectionsCount = 0
        self.xIndexes = []


    def calculate(self, time):
        numberOfPoints = (self.waveSpeed * time) / self.xStep

        self.xValues = []
        self.yValues = []
        self.yValuesDraw = []
        self.xValuesDraw = []
        self.xIndexes = []
        x = 0
        deltaX = self.xStep
        yIndex = 0
        i = 0
        indexDelta = 1
        xIndex = 0
        totalWavePathLength = 0
        k = 2 * math.pi * self.waveFrequency / self.waveSpeed
        y = math.exp(-totalWavePathLength*0)*math.sin(2*math.pi*self.waveFrequency*time - k*totalWavePathLength)
        self.reflectionsCount = 0
        incReflections = False
        while(i<numberOfPoints):
            self.xValues.append(x)
            self.xIndexes.append(xIndex)
            self.xValuesDraw.append(x)
            self.yValues.append(y)
            self.yValuesDraw.append(y+yIndex)
            
            totalWavePathLength = totalWavePathLength + self.xStep
            y = math.exp(-totalWavePathLength*0)*math.sin(2*math.pi*self.waveFrequency*time - k*totalWavePathLength)
            
            xIndex = xIndex + indexDelta
            x = xIndex * self.xStep
            if incReflections:
                self.reflectionsCount = self.reflectionsCount+1
                incReflections = False
            
            if(xIndex >= self.NUM_OF_POINTS):
                self.xValuesDraw.append(x)
                self.yValuesDraw.append(y+yIndex)
                xIndex = xIndex - 1
                indexDelta = -1
                yIndex = yIndex - 8
                incReflections = True
                
            if(xIndex < 0):
                self.xValuesDraw.append(x)
                self.yValuesDraw.append(y+yIndex)
                xIndex = xIndex + 1
                indexDelta = 1
                yIndex = yIndex - 8
                incReflections = True
            i = i+1

    def getNumberOfReflections(self):
        return self.reflectionsCount

    def getXValues(self):
        return self.xValues

    def getXValuesDraw(self):
        return self.xValuesDraw

    def getYValues(self):
        return self.yValues

    def getYValuesDraw(self):
        return self.yValuesDraw

    def findZeros(self, xs, ys):
        retVal = []
        for i in range(len(xs)-1):
            if(ys[i]*ys[i+1] <= 0):
                retVal.append((xs[i] + xs[i+1])/2)
        return retVal
            
def calculateNextFrame(i, sineWaveCalculator):
    plt.clf()
    plt.ylim(-40,40)
    plt.xlim(0,0.2)
    plt.yticks([20,0,-8,-16,-24, -32, -40],['total','1st wave','1st reflection','2nd reflection','3rd reflection', '4th reflection', '5th reflection'], size = 'x-small')
    sineWaveCalculator = SineWave(0,1,0)
    sineWaveCalculator.calculate(i*0.0001)
    plt.plot([0,0.2],[20,20], '--', color = 'lightgray')
    plt.plot(sineWaveCalculator.getXValuesDraw(),sineWaveCalculator.getYValuesDraw())
    xValues = sineWaveCalculator.getXValues()
    yValues = sineWaveCalculator.getYValues()
    sumX = numpy.arange(0, sineWaveCalculator.barWidth, sineWaveCalculator.xStep)
    sumY = (sineWaveCalculator.NUM_OF_POINTS)*[20]
    for i in range(len(xValues)):
        index = sineWaveCalculator.xIndexes[i]
        value = sineWaveCalculator.getYValues()[i]
        sumY[index] = sumY[index] + value
    plt.plot(sumX,sumY)

    if RESONANCE:
        if(sineWaveCalculator.getNumberOfReflections()>=4):
            for i in range(8):
                if i%2 == 1:
                    x = i*0.025
                    plt.arrow(i*0.025,30,0,-10,head_width=0.005,head_length=3, head_starts_at_zero = False, length_includes_head = True)
                    plt.text(x,32,"node",ha='center')
                
    if((sineWaveCalculator.getNumberOfReflections()>=2) and (sineWaveCalculator.getNumberOfReflections()<6)):
        lastX = sineWaveCalculator.getXValuesDraw()[-1]
        lastY = sineWaveCalculator.getYValuesDraw()[-1]
        startPointX = 0.05
        startPointY = 5
        deltaX = lastX - startPointX
        deltaY = lastY - startPointY
        plt.arrow(startPointX,startPointY,deltaX,deltaY,head_width=0.005, head_length=3, head_starts_at_zero = False, length_includes_head = True)
        plt.arrow(startPointX,startPointY,deltaX,deltaY+16,head_width=0.005, head_length=3, head_starts_at_zero = False, length_includes_head = True)
        phaseDifferenceDescription = ""
        if RESONANCE:
            phaseDifferenceDescription = "the same phase"
        else:
            phaseDifferenceDescription = "different phase"
        plt.text(startPointX,startPointY+3,phaseDifferenceDescription,clip_on=True, ha='center',backgroundcolor = 'lightgray')
    
Writer = animation.writers['ffmpeg']
writer = Writer(fps=10, metadata=dict(artist='Me'), bitrate=1800)

sineWaveCalculator = SineWave(0,1,0)

fig1 = plt.figure(frameon=False)

#sineLine, = plt.plot([],[])
#sumLine, = plt.plot(sumX,sumX)
#actorsList = [sineLine, sumLine]#, phaseArrow1, phaseArrow2]

sineWaveAnimation = animation.FuncAnimation(fig1, calculateNextFrame, 300, fargs = [sineWaveCalculator], interval=15, blit=False, repeat = False)

fileName = ""
if RESONANCE:
    fileName = "StandingWave.mp4"
else:
    fileName = "Not_StandingWave.mp4"

if SAVE_TO_FILE:
    sineWaveAnimation.save(fileName, writer=writer)
else:
    plt.show()







