#!/home/pi/envs/plants/bin/python
# -*- coding: utf-8 -*-

#import RPi.GPIO as GPIO
import sys, time, os
from datetime import datetime
import serial
import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plot

Serial = serial.Serial('/dev/ttyUSB0', 115200, timeout= 0.5 )
print (Serial)
if Serial.isOpen():
       print("open success")
else:
       print("open failed")




plotLength = 30
thLight = 950
thWater = 20
lightTime = (6,18)  #hour
waterTime = (5,18) # hour
waterInterval =  2 * 60 * 60 #seconds
wateringTimeLength = 15  #seconds

automatic = True
tList = []
hList = []
lList = []
wList = []
timeList_t = []
timeList_h = []
timeList_l = []
timeList_w = []

btnLight = 21
btnWater = 3
btnAuto = 4


def inputData(arrayName, data, length):
    if(len(arrayName)>length):
        arrayName.pop(0)

    arrayName.append(data)

    return arrayName

def readSerial():
    recv = ""
    dataString = ""
    count = Serial.inWaiting()
    if count != 0:
        try:
            recv = Serial.read(count).decode('utf-8')
            print ("recv1:",recv)
        except:
            pass

        if(recv == "["):
            while recv != "]":
                if Serial.inWaiting():
                    recv = Serial.read(count).decode('utf-8')
                    print('recv2:',recv)
                    if(recv!="]"):
                        dataString += recv

                    time.sleep(0.1)
    #print('dataString:',dataString)
    return dataString

def readSerial2():
    global light1, nowTemperature, nowHumandity
    recv = ""
    dataString = ""
    count = int(Serial.inWaiting())

    if count > 0:
        recv = Serial.read(count).decode('utf-8')
        #print("recv:", recv)
        print('recv1:',recv)
        aLoc = recv.find("[")
        bLoc = recv.find("]")

        if(aLoc>=0 and bLoc>0 and aLoc<bLoc):
            dataString = recv[aLoc+1:bLoc]
    
    return dataString






powerT="OFF"
powerH="OFF"
powerL="OFF"
powerW="OFF"
nowLight = 0
nowWater = 0
waterLastTime = 0


i = 0

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





app_start_time = time.time()

while True:
    data = readSerial2()
    #bg = cv2.imread("bgplant.jpg")

    if(data != ""):
        
        dataList = data.split(",")
        print ("dataList",dataList)
        for dataValue in dataList:
            if(dataValue!=""):
                #print(dataValue)
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
                    print("tList",tList)
                    powerT="ON" if sPower==1 else "OFF"
                elif(sType=="H"):
                    hList = inputData(hList, sValue, plotLength)
                    timeList_h = inputData(timeList_h, dataTime, plotLength)
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


    i += 1
    if(time.time()-app_start_time > 12 * 60 * 60):
        os.execv('/home/pi/works/plant/main.py', [''])
