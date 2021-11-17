#############################################################################################
######### 2021-11-06                  VERSION 0.2a                           J.PALO #########
#############################################################################################

###
#current status: only number input by keyboard input
#in development: number input data collection and data file write in csv format for analysis
#future development: ansver input as voice input
###

#############################################################################################
# THIS PROGRAM PRINTS SIMPLE QUESTIONS ON A SCREEN FOR A SHORT AMOUNT OF TIME.
# QUESTIONS ARE IN A FORM X+X WHERE THE ANSWER IS BETWEEN 0 AND 9.
# USER GIVES ANSWER BY PRESSING THE CORRECT NUMBER KEY  A KEYBOARD.
#############################################################################################
import sys
from cv2 import WND_PROP_OPENGL
import cv2
from time import sleep
from time import perf_counter_ns as pt
from datetime import datetime
import numpy as np
import string
import random
import csv

#Data that will be collected
round_no, x_coordinate, y_coordinate, number1, number2, time_showing, time_took_to_answer, correct_false = ([] for i in range(8))
screen_size = ""
headers = "round_no", "x_coordinate", "y_coordinate", "number1", "number2", "time_showing", "time_took_to_answer", "correct_false"
filedata = [round_no, x_coordinate, y_coordinate, number1, number2, time_showing, time_took_to_answer, correct_false]

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
try:
    steps = float(sys.argv[3])
except:
    print("No number of steps given. Default 100 will be used")
    steps = 100 #How many rounds from maxtime to mintime

# setup text
font = cv2.FONT_HERSHEY_SIMPLEX

#Create initial fullscreen window
cv2.namedWindow('appi', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('appi', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
sleep(1)

#Get screen size in windows
window_size = cv2.getWindowImageRect('appi')
if window_size[2] > 1:
    width = window_size[2]
    print ("Width = " + str(width))
    height = window_size[3]
    print ("Height = " + str(height))
#Get screen size in Ubuntu
else:
    import subprocess
    resl = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
    resl = resl.decode("utf-8")
    window_size = resl.split('x')
    width = int(window_size[0])
    height = int(window_size[1])
    print(str(width) + " x " + str(height))

#Screen size string variable if screen size is detected
if width > 0 and height > 0: screen_size = str(width)+"x"+str(height)

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

def countDown():
    namebox = np.zeros((height,width,3), np.uint8)
    while True:
        namebox = np.zeros((height,width,3), np.uint8)
        cv2.imshow('appi', namebox)
        namebox = cv2.putText(namebox, "Start in 3", (int(width/2)-100,int(height/2)), font, 1, (255,255,0), 2)
        cv2.imshow('appi', namebox)
        cv2.waitKey(1000)
        namebox = np.zeros((height,width,3), np.uint8)
        namebox = cv2.putText(namebox, "Start in 2", (int(width/2)-100,int(height/2)), font, 1, (255,255,0), 2)
        cv2.imshow('appi', namebox)
        cv2.waitKey(1000)
        namebox = np.zeros((height,width,3), np.uint8)
        namebox = cv2.putText(namebox, "Start in 1", (int(width/2)-100,int(height/2)), font, 1, (255,255,0), 2)
        cv2.imshow('appi', namebox)
        cv2.waitKey(1000)
        break

#Generate random answer between 0 and 9 and two integers that add to it
def question_old():
    answ = np.random.randint(10)
    if answ == 0: num1 = 0
    else: num1 = np.random.randint(answ)
    if num1 == 9: num2 = 0
    else: num2 = answ - num1
    return num1, num2

def question():
    answ = np.random.randint(10) #random number (0-9)
    if answ == 0:
        if np.random.choice([0, 1]) == '0': #if answer is 0 then 50/50 chance to try new random generation
            num1 = 0
        else:
            answ = np.random.randint(10)
            num1 = np.random.randint(answ+1)
    else: num1 = np.random.randint(answ+1)

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
def dataToFile(name, screensize, headers, filedata):
    timestamp= datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = "./saves/"+name+"_"+timestamp+"_"+screensize+".csv"
    try:
        with open(filename, 'w', newline='') as f:
            write = csv.writer(f, delimiter=";")
            write.writerow(headers)
            for row in filedata:
                write.writerow(row)
    except Exception as e:
        print(e)
        exit("Error saving filedata to .csv file!")

#Translate linux numpad keypresses to correct numbers
def findKey(key):
    if key==176: key=ord('0')
    if key==177: key=ord('1')
    if key==178: key=ord('2')
    if key==179: key=ord('3')
    if key==180: key=ord('4')
    if key==181: key=ord('5')
    if key==182: key=ord('6')
    if key==183: key=ord('7')
    if key==184: key=ord('8')
    if key==185: key=ord('9')
    if key==ord('q'): return key
    if key==ord('j'): return key

    return key

#How long will question stay visible on each round
def timeVisible(round):
    #How much less showing each round: maxtime-mintime / steps
    kt = int(((mt-it)/steps))
    print("Time step is: " + str(kt))           #print only for testing
    if int(mt-(kt*round)) >= it:
        return int(mt-(kt*round))
    else:
        return int(it)
        
#Main loop
correct = 0     #Number of correct answers
wrong = 0       #Number of wrong aswers
center = True   #Was the last question on center
round = 0       #Round number 
while True:

    #Ask player name
    if (name==""):name=name_input()
    #Countown before first round
    if (round == 0):countDown()

    #Correct / False = False before correct answer
    cf = False

    #answer time starts here
    start = pt()

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

    #Calculate the area where the numbers can appear
    x=int(width/2+(radius(1)))
    if x < 10: x = 10
    if x > width-80: x = width - 80

    y=int(height/2+(radius(2)))
    if y < 30: y = 30
    if y > height-50: y = height - 50

    #If previous question was in a center, place question away from center of screen with a 66% chance
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
    t1 = timeVisible(round)
    print(t1)

    #Here we wait if key is pressed while question is still visible
    key = cv2.waitKey(t1)

    #Print blanc screen after t1 has passed to hide the question
    image = np.zeros((height,width,3), np.uint8)
    blank_image = np.zeros((height,width,3), np.uint8)
    
    #If key NOT pressed while question was visible: hide number and wait for key to be pressed:
    cv2.imshow('appi', blank_image)
    if key == -1:
        key = cv2.waitKey(0) #Wait till key is pressed
    else: pass
 
    #Translate keypad keypresses to correct format
    key = findKey(key)

    #QUIT WHEN q IS PRESSED (no file saving)
    if key == ord('q'):
        t2 = pt() - start
        cv2.destroyAllWindows()
        print(name + ": " + str(correct),"Correct")
        exit()

    #CORRECT ANSWER
    elif key == ord(str(answer)):
        t2 = pt() - start
        # number pressed = answer
        correct += 1
        cf = True #was correct
        #Save data on each cycle to a data table. (round_no, x_coordinate, y_coordinate, number1, number2, time_showing, time_took_to_answer, correct_false)
        saveData(round,x,y,a,b,t1,t2,cf)
        pass
    
    #CHEAT AND MARK CORRECT ANSWER AND CONTINUE GAME
    elif key == ord('j'):
        t2 = pt() - start
        correct += 1
        cf = True #was correct
        #Save data on each cycle to a data table. (round_no, x_coordinate, y_coordinate, number1, number2, time_showing, time_took_to_answer, correct_false)
        saveData(round,x,y,a,b,t1,t2,cf)
        pass
    
    #WRONG ANSWER
    else:
        t2 = pt() - start
        wc = False #was false
        #Save data on each cycle to a data table. (round_no, x_coordinate, y_coordinate, number1, number2, time_showing, time_took_to_answer, correct_false)
        saveData(round,x,y,a,b,t1,t2,cf)
        print(name + ": " + str(correct),"Correct")
        
        #Save data to file
        filedata = zip(round_no, x_coordinate, y_coordinate, number1, number2, time_showing, time_took_to_answer, correct_false)
        dataToFile(str(name),str(screen_size),headers,filedata)

        cv2.destroyAllWindows()
        exit()

    #print the time that took to answer. For testing!
    print("kierroksen aika oli: " +str(t2/1000000000))
    key = None
