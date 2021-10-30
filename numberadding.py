import sys
from cv2 import cv2
import pandas as pd
from time import sleep
import numpy as np
import string

# setup text
font = cv2.FONT_HERSHEY_SIMPLEX

#Create initial fullscreen window
cv2.namedWindow('appi', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('appi', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
sleep(2)
window_size = cv2.getWindowImageRect('appi')
width = window_size[2]
print ("Width = " + str(width))
height = window_size[3]
print ("Height = " + str(height))
print(width, height)

#Create blank image to fill page
blank_image = np.zeros((height,width,3), np.uint8)

def name_input():
    text = ""
    namebox = np.zeros((height,width,3), np.uint8)
    letters = string.ascii_lowercase + string.digits
    while True:
        key = cv2.waitKey(1)
        for letter in letters:
            if key == ord(letter):
                text = text + letter
        if key == ord("\n") or key == ord("\r"): # Enter Key
            break
        elif key == ord("\b"): # backspace
            text = text[:-1]
            namebox = np.zeros((height,width,3), np.uint8)
        namebox = cv2.putText(namebox, "Name: "+text, (int(width/2)-200,int(height/2)), font, 1, (255,255,0), 2)
        cv2.imshow('appi', namebox)
    return text

#Generate random answer between 0 and 9 and two integers that add to it
def question():
    answ = np.random.randint(10)
    if answ == 0: num1 = 0
    else: num1 = np.random.randint(answ)
    if num1 == 9: num2 = 0
    else: num2 = answ - num1
    return num1, num2

#remapping function
def remap(x, in_min, in_max, out_min, out_max):
    if (x == 0 or in_max == 0):
        return 0
    else:
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

#calculate the area where the numbers can appear
def radius(wh):
    #How far off center can question appear?
    if (wh==1):
        war = int((width/2)*remap(correct/100,0,100,0,100))
        print (war)
        if (war == 0):
            return 0
        else:
            wh = np.random.randint(war*(-1),war,1)
            print (wh)
            return wh
    else:
        har = int((height/2)*remap(correct/100,0,100,0,100))
        print (har)
        if (har == 0):
            return 0
        else:
            wh = np.random.randint(har*(-1),har,1)
            print (wh)
            return wh

#Save data on each cycle to a data table. (round_no, x_coordinate, y_coordinate, number1, number2, time_showing, time_took_to_answer, correct_false, screen_size)
def saveData(rd,x,y,n1,n2,t1,t2,cf,sc):
    pass

#Create file from game data
def dataToFile():
    pass

#Main loop
correct = 0
center = True
name = ""
while True:
    #Ask player name
    if (name==""):name=name_input()

    #Generate numbers that add to 0-9
    a, b = question()
    answer = a+b

    #Form a question string from the generated numbers 
    qstring = str(a)+"+"+str(b)

    #Blank screen images before every cycle
    image = np.zeros((height,width,3), np.uint8)
    blank_image = np.zeros((height,width,3), np.uint8)
    cv2.imshow('appi', image)

    #If previous question was in a center, place question away from center of screen
    if(center == True):
        image = cv2.putText(blank_image, qstring, (int(width/2+(radius(1))),int(height/2+(radius(2)))), font, 1, (255,255,0), 2)
        center = False
    #If previous question was away from a center, place question directly to center of screen
    else:
        image = cv2.putText(blank_image, qstring, (int(width/2),int(height/2)), font, 1, (255,255,0), 2)
        center = True

    #Show question
    cv2.imshow('appi', image)

    key = cv2.waitKey(int(1000*(1-correct/100)))
    image = np.zeros((height,width,3), np.uint8)
    blank_image = np.zeros((height,width,3), np.uint8)
    cv2.imshow('appi', blank_image)

    #If key not pressed while number was showing, hide number and wait key:
    if key == -1:
        key = cv2.waitKey(0)
    else: pass
    #Wait till key is pressed
    if key == ord('q'):
        cv2.destroyAllWindows()
        print(name + ": " + str(correct),"Correct")
        exit()
    elif key == ord(str(answer)):
        # number pressed = answer
        correct += 1
        pass
    else:
        print(name + ": " + str(correct),"Correct")
        exit()
    key = None
