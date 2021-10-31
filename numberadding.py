import sys
from cv2 import cv2
from time import sleep
import numpy as np
import string
import random

#############################################################################################
######### 2021                        VERSION 0.1a                           J.PALO #########
#############################################################################################

#Data that will be collected
round_no, x_coordinate, y_coordinate, number1, number2, time_showing, time_took_to_answer, correct_false = ([] for i in range(8))
screen_size = ""

#Test if name, maxtime and mintime is given as commandline argument
#name=player name, maxtime(mt)=time the number question will be visible at the beginning, mintime(it)=minimun time that the question will be visible
try:
    name = sys.argv[1]
except:
    print("No name given, name prompt will appear")
    name = ""
try:
    mt = float(sys.argv[2])
except:
    print("No max visibility time given. Default 1s will be used")
    mt = 1000 #max time that question is visible
try:
    it = float(sys.argv[3])
except:
    print("No min visibility time given. Default 100ms will be used")
    it = 100 #mIn time that question is visible

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

#Create blank image to fill page
blank_image = np.zeros((height,width,3), np.uint8)

#Ask for player name in cv2 style if not given as argument
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
        #print (war)
        if (war == 0):
            return 0
        else:
            wh = np.random.randint(war*(-1),war,1)
            #print (wh)
            return wh
    else:
        har = int((height/2)*remap(correct/100,0,100,0,100))
        #print (har)
        if (har == 0):
            return 0
        else:
            wh = np.random.randint(har*(-1),har,1)
            #print (wh)
            return wh

#Save data on each cycle to a data table. (round_no, x_coordinate, y_coordinate, number1, number2, time_showing, time_took_to_answer, correct_false)
def saveData(rd,x,y,n1,n2,t1,t2,cf):
    #append new values to the end of every list
    round_no.append(rd)
    x_coordinate.append(x)
    y_coordinate.append(y)
    number1.append(n1)
    number2.append(n2)
    time_showing.append(t1)
    time_took_to_answer.append(t2)
    correct_false.append(cf)

#Create file from game data
def dataToFile():
    pass

#Main loop
correct = 0
center = True
round = 0
while True:
    #Ask player name
    if (name==""):name=name_input()

    #increment round number
    round += 1

    #Generate numbers that add to 0-9
    a, b = question()
    answer = a+b

    #Form a question string from the generated numbers 
    qstring = str(a)+"+"+str(b)

    #Blank screen images before every cycle
    image = np.zeros((height,width,3), np.uint8)
    blank_image = np.zeros((height,width,3), np.uint8)
    cv2.imshow('appi', image)

    x=int(width/2+(radius(1)))
    y=int(height/2+(radius(2)))

    #If previous question was in a center, place question away from center of screen with a 66% chanse
    if(center == True and random.randrange(3) != 0):
        image = cv2.putText(blank_image, qstring, (x,y), font, 1, (255,255,0), 2)
        center = False
    #If previous question was away from a center, place question directly to center of screen
    else:
        image = cv2.putText(blank_image, qstring, (int(width/2),int(height/2)), font, 1, (255,255,0), 2)
        center = True

    #Show question
    cv2.imshow('appi', image)

    #Time for how long the question will be visible
    #t1 = int(1000*(1-correct/100)) # <-- ok from 1sec to lower with 10ms increment but not scalable
    kt = mt/it
    print("Time step is: " + str(kt))           #print only for testing
    t1 = int(mt-(kt*correct))
    print(t1)                                   #print only for testing
    key = cv2.waitKey(t1)
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
    elif key == ord('j'):
        correct += 1
        pass
    else:
        print(name + ": " + str(correct),"Correct")
        exit()
    key = None

    #Save data on each cycle to a data table. (round_no, x_coordinate, y_coordinate, number1, number2, time_showing, time_took_to_answer, correct_false)
    #saveData(round,x,y,a,b,t1)
