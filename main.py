#!/home/pi/envs/plants/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import sys, time, os
from datetime import datetime
import serial
import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plot

Serial = serial.Serial("/dev/ttyUSB0",115200 , timeout= 0.5 )

plotLength = 30
thLight = 950
thWater = 20
lightTime = (6,18)  #hour
waterTime = (5,18) # hour
waterInterval =  2 * 60 * 60 #seconds
wateringTimeLength = 15  #seconds

automatic = False
tList = []
hList = []
lList = []
wList = []
timeList_t = []
timeList_h = []
timeList_l = []
timeList_w = []

#btnLight = 21
#btnWater = 3
#btnAuto = 4
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(btnLight, GPIO.IN)
#GPIO.setup(btnWater, GPIO.IN)
#GPIO.setup(btnAuto, GPIO.IN)

def inputData(arrayName, data, length):
    if(len(arrayName)>length):
        arrayName.pop(0)

    arrayName.append(data)
    print(data)
    return arrayName

def readSerial():
    recv = ""
    dataString = ""
    count = Serial.inWaiting()
    if count != 0:
        try:
            recv = Serial.read(count).decode('utf-8')
        except:
            pass

        if(recv == "["):
            while recv != "]":
                if Serial.inWaiting():
                    recv = Serial.read(count).decode('utf-8')
                    if(recv!="]"):
                        dataString += recv

                    time.sleep(0.1)

    return dataString

def readSerial2():
    global light1, nowTemperature, nowHumandity
    recv = ""
    dataString = ""
    count = int(Serial.inWaiting())

    if count > 0:
        #recv = Serial.read(count).decode('utf-8')
        #print("recv:", recv)
        data_raw = Serial.readline()
        recv = data_raw.decode('utf-8')
        aLoc = recv.find("[")
        bLoc = recv.find("]")

        if(aLoc>=0 and bLoc>0 and aLoc<bLoc):
            dataString = recv[aLoc+1:bLoc]

    return dataString


cv2.namedWindow("Plant Image", cv2.WND_PROP_FULLSCREEN)        # Create a named window
cv2.setWindowProperty("Plant Image", cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

figure = plot.figure(num=None, figsize=(18, 7), dpi=70, facecolor='w', edgecolor='k')
ax_t = figure.add_subplot(2,2,1)
ax_h = figure.add_subplot(2,2,2)
ax_l = figure.add_subplot(2,2,3)
ax_w = figure.add_subplot(2,2,4)

powerT="OFF"
powerH="OFF"
powerL="OFF"
powerW="OFF"
nowLight = 0
nowWater = 0
waterLastTime = 0

i = 0


orgBG = cv2.imread("bgplant.jpg")
bg = orgBG.copy()





def lightPressed(channel):
    global nowLight, powerL, automatic

    automatic = False
    print("Light pressed", channel)
    if nowLight==1:
        Serial.write("b".encode())
        nowLight = 0
        print("Power off the Light.")
    else:
        Serial.write("a".encode())
        nowLight = 1
        print("Power on the Light.")

    powerL="ON" if nowLight==1 else "OFF"



#GPIO.add_event_detect(btnLight, GPIO.FALLING, lightPressed, bouncetime=1000)

app_start_time = time.time()

while True:
    data = readSerial2()
    #bg = cv2.imread("bgplant.jpg")

    if(data != ""):
        dataList = data.split(",")
        for dataValue in dataList:
            '''
            #Button commands
            clickLight = GPIO.input(btnLight)
            clickWater = GPIO.input(btnWater)
            clickAuto = GPIO.input(btnAuto)
            print("Button:", clickLight, clickWater, clickAuto)

            
                if(clickWater==0):
                    if nowWater==1:
                        Serial.write("d".encode())
                        nowWater = 0
                        print("Power off the Water.")
                    else:
                        Serial.write("c".encode())
                        nowWater = 1
                        print("Power on the Water.")

                    powerL="ON" if nowWater==1 else "OFF"
                    break
            '''

            if(dataValue!=""):
                print(dataValue)
                now = datetime.now()
                dataTime = now.strftime("%H:%M:%S")
                hourNow = int(now.strftime("%H"))
                try:
                    sType, sValue, sPower = dataValue.split(":")
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    break

                try:
                    sPower = int(sPower)
                    sValue = float(sValue)
                except:
                    break

                if(sType=="T"):
                    tList = inputData(tList, sValue, plotLength)
                    timeList_t = inputData(timeList_t, dataTime, plotLength)
                    print(tList)
                    powerT="ON" if sPower==1 else "OFF"
                elif(sType=="H"):
                    hList = inputData(hList, sValue, plotLength)
                    timeList_h = inputData(timeList_h, dataTime, plotLength)
                    print(hList)
                    powerH="ON" if sPower==1 else "OFF"

                elif(sType=="L"):
                    lList = inputData(lList, int(sValue), plotLength)
                    timeList_l = inputData(timeList_l, dataTime, plotLength)
                    powerL="ON" if sPower==1 else "OFF"

                    if(automatic is True):
                        if(hourNow<lightTime[1] and hourNow>=lightTime[0]):
                            if(int(sValue)<thLight and sPower==0):
                                #--> a: power on ligher, b: power off light, c: power on water, d: power off water
                                Serial.write("a".encode())
                                sPower = 1
                                nowLight = 1
                                print("Power on the Light.")
                            if(int(sValue)>=thLight and sPower==1):
                                #--> a: power on ligher, b: power off light, c: power on water, d: power off water
                                Serial.write("b".encode())
                                sPower = 0
                                nowLight = 0
                                print("Power off the Light.")
                        else:
                            if(sPower==1):
                                Serial.write("b".encode())
                                sPower = 0
                                nowLight = 0
                                print("Power off the Light.")

                elif(sType=="W"):
                    sValue = 1024 - int(sValue)
                    wList = inputData(wList, int(sValue), plotLength)
                    timeList_w = inputData(timeList_w, dataTime, plotLength)
                    powerW="ON" if sPower==1 else "OFF"

                    if(automatic is True):
                        if(hourNow<waterTime[1] and hourNow>=waterTime[0]):
                            if(sPower==1):
                                if(time.time()-waterLastTime>wateringTimeLength or int(sValue)>thWater):
                                    Serial.write("d".encode())
                                    sPower = 0
                                    nowWater = 0
                                    print("Power off the water.")

                            if(sPower==0):
                                if(time.time()-waterLastTime > waterInterval ):
                                    if(int(sValue)<=thWater):
                                        Serial.write("c".encode())
                                        print("Power on the water.")
                                        sPower = 1
                                        nowWater = 1
                                        waterLastTime = time.time()

                # draw a cardinal sine plot
                x = np.array (timeList_t )
                y = np.array (tList)
                ax_t.cla()
                ax_t.set_ylim(0, 80)
                ax_t.set_title("Temperature (C)")
                ax_t.axes.get_xaxis().set_visible(False)
                ax_t.plot ( x, y, 'ro-' )

                x = np.array (timeList_h )
                y = np.array (hList)
                ax_h.cla()
                ax_h.set_title("Humandity (%)")
                ax_h.set_ylim(0, 100)
                ax_h.axes.get_xaxis().set_visible(False)
                ax_h.plot ( x, y ,'co-')

                x = np.array (timeList_l )
                y = np.array (lList)
                ax_l.cla()
                ax_l.set_title("Lightness (degree)")
                ax_l.set_ylim(0, 1024)
                ax_l.axes.get_xaxis().set_visible(False)
                ax_l.plot ( x, y ,'yo-')

                x = np.array (timeList_w )
                y = np.array (wList)
                ax_w.cla()
                ax_w.set_title("Water (degree)")
                ax_w.set_ylim(0, 1024)
                ax_w.axes.get_xaxis().set_visible(False)
                ax_w.plot ( x, y , 'bo-')


                figure.canvas.draw()
                # convert canvas to image
                img = np.fromstring(figure.canvas.tostring_rgb(), dtype=np.uint8, sep='')
                img  = img.reshape(figure.canvas.get_width_height()[::-1] + (3,))
                # img is rgb, convert to opencv's default bgr
                img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

                #matplotlib.pyplot.show()
                bg = orgBG.copy()
                bg[290:290+490, 85:85+1260] = img
                cv2.putText(bg, str(lightTime[0])+":00~"+str(lightTime[1])+":00", (760, 140), cv2.FONT_HERSHEY_COMPLEX, 1.3, (255,0,0), 3)
                cv2.putText(bg, str(thLight), (1290, 140), cv2.FONT_HERSHEY_COMPLEX, 1.3, (0,0,255), 3)
                cv2.putText(bg, str(waterTime[0])+":00~"+str(waterTime[1])+":00", (760, 206), cv2.FONT_HERSHEY_COMPLEX, 1.3, (255,0,0), 3)
                cv2.putText(bg, str(thWater), (1290, 206), cv2.FONT_HERSHEY_COMPLEX, 1.3, (0,0,255), 3)

                if(len(tList)>0):
                    cv2.putText(bg, str(tList[len(tList)-1])+"C", (146, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0,255,0), 2)
                if(len(hList)>0):
                    cv2.putText(bg, str(hList[len(hList)-1])+"%", (310, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0,255,0), 2)
                if(len(lList)>0):
                    cv2.putText(bg, str(lList[len(lList)-1]), (476, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0,255,0), 2)
                if(len(wList)>0):
                    cv2.putText(bg, str(wList[len(wList)-1]), (656, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0,255,0), 2)

                #print("#2", "clickLight:", clickLight, "clickWater:", clickWater, "powerL:", powerL, "powerW:", powerW)
                color = (powerL=="ON") and (0,0,255) or (255,0,0)
                cv2.putText(bg, powerL, (620, 277), cv2.FONT_HERSHEY_COMPLEX, 0.8,  color, 2)
                #color=(0,0,0) if powerW=="ON" else (0,0,255)
                color = (powerW=="ON") and (0,0,255) or (255,0,0)
                cv2.putText(bg, powerW, (760, 277), cv2.FONT_HERSHEY_COMPLEX, 0.8, color, 2)
                cv2.putText(bg, str(int(waterInterval/60)), (960, 277), cv2.FONT_HERSHEY_COMPLEX, 1.1, (255,0,0), 2)
                cv2.putText(bg, str(wateringTimeLength), (1215, 277), cv2.FONT_HERSHEY_COMPLEX, 1.1, (255,0,0), 2)

                cv2.imshow("Plant Image", bg)
                #cv2.imwrite("plantimg.jpg", bg)

                cv2.waitKey(1)

        i+= 1
   # if(time.time()-app_start_time > 12 * 60 * 60):
    #    os.execv('/home/pi/works/plant/main.py', [''])
