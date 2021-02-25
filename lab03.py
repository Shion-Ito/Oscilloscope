# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import matplotlib.pyplot as plt


# Software SPI configuration:
CLK  = 11
MISO = 9
MOSI = 10
CS   = 22

mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
voltage = [] 
pastTime = [] 
timeStamps = []

startTime = time.time()
passedTime = 0.0
currentTime =[]

# The Oscilloscope will run for 5 seconds
while passedTime <= 0.1:
    # read from channel 0
    VoltageChannel = mcp.read_adc(0)
    # find out the time stamp of the reading and the elapsed time
    passedTime = time.time() - startTime
    XYValue = (VoltageChannel, passedTime)
    voltage.append(VoltageChannel)
    pastTime.append(passedTime)
    currentTime.append(time.time())
    print("Time: \t%f, Voltage: \t%d" % (XYValue[1], XYValue[0]))


maxValue = max(voltage)
cnt = 0
timeRange = []
form = ""


def findPeaks(array):
    if form == "Sine" or form == "Triangle":
        i = 1
        while i < len(array)-1:
            if array[i+1] <= array[i] and array[i-1] <= array[i]:
                timeRange.append(currentTime[i])
                break
            i += 1
        while i < len(array) and array[i] == array[i+1]:
            i += 1
        i += 1
        while i < len(array):
            if array[i+1] <= array[i] and array[i-1] <= array[i]:
                timeRange.append(currentTime[i])
                break
            i += 1
        return timeRange
    else:
        i = 0
        while i < len(array)-1:
            if array[i] > 10 and array[i+1] < 10:
                timeRange.append(currentTime[i])
                break
            i += 1
        i += 1
        #print("AFTER FIRST",voltage[i])
        while i < len(array)-1:
            if array[i] > 10 and array[i+1] < 10:
                timeRange.append(currentTime[i])
                break
            i += 1
        return timeRange

def form(array, time):
    i = 0
    cnt = 0
    while i < len(array)-1 and cnt < 10:
        if array[i] >= array[i+1]-2 and array[i] <= array[i+1]+2:
            #print(array[i])
            cnt += 1
        else:
            cnt = 0
        i += 1
    if cnt == 10:
        return "Square"
    else:
        i = 0
        j = 1
        cnt = 0
        prevSlope = 0
        slope = 0
        while i < len(array)-1 and j < len(array)-2 and cnt < 6:
            prevSlope = (array[i+1]-array[i])/(time[i+1]-time[i])
            slope = (array[j+1]-array[j])/(time[j+1]-time[j])
            if (prevSlope != 0):
                difference = abs((slope - prevSlope)/ prevSlope)
            elif(slope != 0):
                difference = abs((prevSlope - slope)/ slope)
            elif(prevSlope != 0 and slope != 0):
                 difference = abs((slope - prevSlope)/ prevSlope)
            else:
                difference = 0                
            if 100*difference <= 8:
                cnt += 1
            else:
                cnt = 0
            i += 1
            j += 1
        if cnt >= 5:
            return "Triangle"
        else:
            return "Sine"


form = form(voltage, currentTime)

print("Waveform Shape:", form)
findPeaks(voltage)
period = timeRange[1] - timeRange[0]
print("Frequency:", 1 / period)

plt.plot(pastTime, voltage, 'o-')
plt.title("Wave")
plt.ylabel('Voltage Value')
plt.xlabel('time')

plt.show()