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
import random



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

powerT="OFF"
powerH="OFF"
powerL="OFF"
powerW="OFF"




cv2.namedWindow("Plant Image", cv2.WND_PROP_FULLSCREEN)        # Create a named window
cv2.setWindowProperty("Plant Image", cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
figure = plot.figure(num=None, figsize=(18, 7), dpi=70, facecolor='w', edgecolor='k')

ax_t = figure.add_subplot(2,2,1)
ax_h = figure.add_subplot(2,2,2)
ax_l = figure.add_subplot(2,2,3)
ax_w = figure.add_subplot(2,2,4)

orgBG = cv2.imread("bgplant.jpg")
bg = orgBG.copy()
i = 0


def inputData(arrayName, data, length):
    if(len(arrayName)>length):
        arrayName.pop(0)
    arrayName.append(data)
    return arrayName


cv2.imshow("Plant Image", bg)
#cv2.waitKey(0)
app_start_time = time.time()

while True:
    now = datetime.now()
    dataTime = now.strftime("%H:%M:%S")
    hourNow = int(now.strftime("%H"))

    sValue = random.randint(20, 25)
    tList = inputData(tList, sValue, plotLength)
    timeList_t = inputData(timeList_t, dataTime, plotLength)

    sValue = random.randint(50,90)
    hList = inputData(hList, sValue, plotLength)
    timeList_h = inputData(timeList_h, dataTime, plotLength)

    sValue = random.randint(0, 1024)
    lList = inputData(lList, sValue, plotLength)
    timeList_l = inputData(timeList_l, dataTime, plotLength)

    sValue = random.randint(0, 1024)
    wList = inputData(wList, sValue, plotLength)
    timeList_w = inputData(timeList_w, dataTime, plotLength)


    # draw a cardinal sine plot

    x = np.array(timeList_t)
    y = np.array(tList)
    ax_t.cla()
    ax_t.set_ylim(0, 80)
    ax_t.set_title("Temperature (C)")
    ax_t.axes.get_xaxis().set_visible(False)
    ax_t.plot(x, y, 'ro-')

    x = np.array(timeList_h)
    y = np.array(hList)
    ax_h.cla()
    ax_h.set_title("Humandity (%)")
    ax_h.set_ylim(0, 100)
    ax_h.axes.get_xaxis().set_visible(False)
    ax_h.plot(x, y, 'co-')

    x = np.array(timeList_l)
    y = np.array(lList)
    ax_l.cla()
    ax_l.set_title("Lightness (degree)")
    ax_l.set_ylim(0, 1024)
    ax_l.axes.get_xaxis().set_visible(False)
    ax_l.plot(x, y, 'yo-')

    x = np.array(timeList_w)
    y = np.array(wList)
    ax_w.cla()
    ax_w.set_title("Water (degree)")
    ax_w.set_ylim(0, 1024)
    ax_w.axes.get_xaxis().set_visible(False)
    ax_w.plot(x, y, 'bo-')



    figure.canvas.draw()

    # convert canvas to image
    img = np.fromstring(figure.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    img = img.reshape(figure.canvas.get_width_height()[::-1] + (3,))


    # img is rgb, convert to opencv's default bgr
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)



    bg = orgBG.copy()
    bg[290:290 + 490, 85:85 + 1260] = img
    cv2.putText(bg, str(lightTime[0]) + ":00~" + str(lightTime[1]) + ":00", (760, 140), cv2.FONT_HERSHEY_COMPLEX, 1.3,
                (255, 0, 0), 3)
    cv2.putText(bg, str(thLight), (1290, 140), cv2.FONT_HERSHEY_COMPLEX, 1.3, (0, 0, 255), 3)
    cv2.putText(bg, str(waterTime[0]) + ":00~" + str(waterTime[1]) + ":00", (760, 206), cv2.FONT_HERSHEY_COMPLEX, 1.3,
                (255, 0, 0), 3)
    cv2.putText(bg, str(thWater), (1290, 206), cv2.FONT_HERSHEY_COMPLEX, 1.3, (0, 0, 255), 3)

    if (len(tList) > 0):
        cv2.putText(bg, str(tList[len(tList) - 1]) + "C", (146, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)
    if (len(hList) > 0):
        cv2.putText(bg, str(hList[len(hList) - 1]) + "%", (310, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)
    if (len(lList) > 0):
        cv2.putText(bg, str(lList[len(lList) - 1]), (476, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)
    if (len(wList) > 0):
        cv2.putText(bg, str(wList[len(wList) - 1]), (656, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)

    #print("#2", "clickLight:", clickLight, "clickWater:", clickWater, "powerL:", powerL, "powerW:", powerW)
    color = (powerL == "ON") and (0, 0, 255) or (255, 0, 0)
    cv2.putText(bg, powerL, (620, 277), cv2.FONT_HERSHEY_COMPLEX, 0.8, color, 2)
    # color=(0,0,0) if powerW=="ON" else (0,0,255)
    color = (powerW == "ON") and (0, 0, 255) or (255, 0, 0)
    cv2.putText(bg, powerW, (760, 277), cv2.FONT_HERSHEY_COMPLEX, 0.8, color, 2)
    cv2.putText(bg, str(int(waterInterval / 60)), (960, 277), cv2.FONT_HERSHEY_COMPLEX, 1.1, (255, 0, 0), 2)
    cv2.putText(bg, str(wateringTimeLength), (1215, 277), cv2.FONT_HERSHEY_COMPLEX, 1.1, (255, 0, 0), 2)

    cv2.imshow("Plant Image", bg)
    cv2.imwrite("plantimg.jpg", bg)

    cv2.waitKey(1)






    i += 1


    #if(time.time()-app_start_time > 12 * 60 * 60):
    #  os.execv('/home/pi/works/plant/main.py', [''])
