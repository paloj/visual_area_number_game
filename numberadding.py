#############################################################################################
######### 2021-12-31                  VERSION 0.3a                           J.PALO #########
#############################################################################################

###
# current status: only number input by keyboard input
# in development: number input data collection and data file write in csv format for analysis
# future development: ansver input as voice input
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

# Data that will be collected
round_no, x_coordinate, y_coordinate, number1, number2, time_showing, time_took_to_answer, correct_false = ([
] for i in range(8))
screen_size = ""
headers = "round_no", "x_coordinate", "y_coordinate", "number1", "number2", "time_showing", "time_took_to_answer", "correct_false"
filedata = [round_no, x_coordinate, y_coordinate, number1,
            number2, time_showing, time_took_to_answer, correct_false]

# Test if name, maxtime and mintime is given as commandline argument
# name=player name, maxtime(mt)=time the number question will be visible at the beginning, mintime(it)=minimun time that the question will be visible
try:
    name = sys.argv[1].lower()
except:
    print("No name given, name prompt will appear")
    name = ""
try:
    wrong = int(sys.argv[2])
except:
    print("No specific number of errors given that causes quit. Default 10 will be used")
    wrong = 10
try:
    mt = float(sys.argv[3])
except:
    print("No max visibility time given. Default 1s will be used")
    mt = 1000  # max time that question is visible
try:
    it = float(sys.argv[4])
except:
    print("No min visibility time given. Default 100ms will be used")
    it = 100  # mIn time that question is visible
try:
    steps = float(sys.argv[5])
except:
    print("No number of steps given. Default 200 will be used")
    steps = 200  # How many rounds from maxtime to mintime

# setup text
font = cv2.FONT_HERSHEY_SIMPLEX

# Create initial fullscreen window
cv2.namedWindow('appi', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('appi', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
sleep(1)

# Get screen size in windows
window_size = cv2.getWindowImageRect('appi')
if window_size[2] > 1:
    width = window_size[2]
    print("Width = " + str(width))
    height = window_size[3]
    print("Height = " + str(height))
# Get screen size in Ubuntu
else:
    import subprocess
    resl = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',
                            shell=True, stdout=subprocess.PIPE).communicate()[0]
    resl = resl.decode("utf-8")
    window_size = resl.split('x')
    width = int(window_size[0])
    height = int(window_size[1])
    print(str(width) + " x " + str(height))

# Screen size string variable if screen size is detected
if width > 0 and height > 0:
    screen_size = str(width)+"x"+str(height)

# Create blank image to fill page
blank_image = np.zeros((height, width, 3), np.uint8)

# Ask for player name in cv2 style if not given as argument


def name_input():
    text = ""
    namebox = np.zeros((height, width, 3), np.uint8)
    letters = string.ascii_letters + string.digits
    while True:
        key = cv2.waitKey(1)
        for letter in letters:
            if key == ord(letter):
                text = text + letter
        if key == ord("\n") or key == ord("\r"):  # Enter Key
            break
        elif key == ord("\b"):  # backspace
            text = text[:-1]
            namebox = np.zeros((height, width, 3), np.uint8)
        namebox = cv2.putText(
            namebox, "Name: "+text, (int(width/2)-200, int(height/2)), font, 1, (255, 255, 0), 2)
        cv2.imshow('appi', namebox)
    return text.lower()


def countDown():
    namebox = np.zeros((height, width, 3), np.uint8)
    while True:
        namebox = np.zeros((height, width, 3), np.uint8)
        cv2.imshow('appi', namebox)
        namebox = cv2.putText(namebox, "Start in 3", (int(
            width/2)-100, int(height/2)), font, 1, (255, 255, 0), 2)
        cv2.imshow('appi', namebox)
        cv2.waitKey(1000)
        namebox = np.zeros((height, width, 3), np.uint8)
        namebox = cv2.putText(namebox, "Start in 2", (int(
            width/2)-100, int(height/2)), font, 1, (255, 255, 0), 2)
        cv2.imshow('appi', namebox)
        cv2.waitKey(1000)
        namebox = np.zeros((height, width, 3), np.uint8)
        namebox = cv2.putText(namebox, "Start in 1", (int(
            width/2)-100, int(height/2)), font, 1, (255, 255, 0), 2)
        cv2.imshow('appi', namebox)
        cv2.waitKey(1000)
        break

# Generate random answer between 0 and 9 and two integers that add to it


def question_old():
    answ = np.random.randint(10)
    if answ == 0:
        num1 = 0
    else:
        num1 = np.random.randint(answ)
    if num1 == 9:
        num2 = 0
    else:
        num2 = answ - num1
    return num1, num2


def question(f=False):
    answ = np.random.randint(10)  # random number (0-9)
    if answ == 0:
        # if answer is 0 then 50/50 chance to try new random generation
        if np.random.choice([0, 1]) == 0:
            num1 = 0
        else:
            answ = np.random.randint(10)
            num1 = np.random.randint(answ+1)
    else:
        num1 = np.random.randint(answ+1)

    if num1 == 9:
        num2 = 0
    else:
        num2 = answ - num1
    #return fake answers as string
    if f:
        return f"{num1}-{num2}"
    #return right ansver
    else:
        return num1, num2

# remapping function


def remap(x, in_min, in_max, out_min, out_max):
    if (x == 0 or in_max == 0):
        return 0
    else:
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# calculate the area where the numbers can appear


def radius(wh):
    # How far off center can question appear?
    if (wh == 1):
        war = int((width/2)*remap(correct/100, 0, 100, 0, 100))
        #print(war)
        if (war == 0):
            return 0
        else:
            if war > width/2:
                war = width/2  # max x coordinate off center
            wh = np.random.randint(war*(-1), war, 1)
            #minimum distance from center
            if abs(wh) < 30: wh=wh*2
            #print(wh)
            return wh
    else:
        har = int((height/2)*remap(correct/100, 0, 100, 0, 100))
        #print (har)
        if (har == 0):
            return 0
        else:
            if har > height/2:
                har = height / 2  # max y coordinate off center
            wh = np.random.randint(har*(-1), har, 1)
            #minium distance from center
            if abs(wh) < 30: wh = wh*2
            #print (wh)
            return wh

# Save data on each cycle to a data table. (round_no, x_coordinate, y_coordinate, number1, number2, time_showing, time_took_to_answer, correct_false)


def saveData(rd, x, y, n1, n2, t1, t2, cf):
    # append new values to the end of every list
    round_no.append(rd)
    x_coordinate.append(x)
    y_coordinate.append(y)
    number1.append(n1)
    number2.append(n2)
    time_showing.append(t1)
    time_took_to_answer.append(t2)
    correct_false.append(cf)

# Create file from game data


def dataToFile(name, screensize, headers, filedata):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
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

# Translate linux numpad keypresses to correct numbers


def findKey(key):
    if key == 176:
        key = ord('0')
    if key == 177:
        key = ord('1')
    if key == 178:
        key = ord('2')
    if key == 179:
        key = ord('3')
    if key == 180:
        key = ord('4')
    if key == 181:
        key = ord('5')
    if key == 182:
        key = ord('6')
    if key == 183:
        key = ord('7')
    if key == 184:
        key = ord('8')
    if key == 185:
        key = ord('9')
    if key in (ord('q'), ord('Q')):
        return key
    if key in (ord('j'), ord('J')):
        return key

    return key

# How long will question stay visible on each round


def timeVisible(round):
    # How much less showing each round: maxtime-mintime / steps
    kt = int(((mt-it)/steps))
    print("Time step is: " + str(kt))  # print only for testing
    if int(mt-(kt*round)) >= it:
        return int(mt-(kt*round))
    else:
        return int(it)

def drawDistracion(image,fa1,fa2,fa3,fa4,x,y,center):
    #if center:
    if (width/2)-80 <= x <= (width/2)+80:
        x = x + 80
    if (height/2)-80 <= y <= (height/2)+80:
        y = y + 80

    
    if x < width/2:
        if y < height/2: #left upper
            #fake left lower
            image = cv2.putText(blank_image, fa1, (x, height-y), font, 1, (255, 255, 0), 2)
            #fake right lower
            image = cv2.putText(blank_image, fa2, (width-x, height-y), font, 1, (255, 255, 0), 2)
            #fake right upper
            image = cv2.putText(blank_image, fa3, (width-x, y), font, 1, (255, 255, 0), 2)
            if center:
                #fake left upper
                image = cv2.putText(blank_image, fa4, (x, y), font, 1, (255, 255, 0), 2)
            else:
                #fake center
                image = cv2.putText(blank_image, fa4, (int(width/2), int(height/2)), font, 1, (255, 255, 0), 2)
            return image

        else: #left lower
            #fake left upper
            image = cv2.putText(blank_image, fa1, (x, height-y), font, 1, (255, 255, 0), 2)
            #fake right lower
            image = cv2.putText(blank_image, fa2, (width-x, y), font, 1, (255, 255, 0), 2)
            #fake right upper
            image = cv2.putText(blank_image, fa3, (width-x, height-y), font, 1, (255, 255, 0), 2)
            if center:
                #fake left lower
                image = cv2.putText(blank_image, fa4, (x, y), font, 1, (255, 255, 0), 2)
            else:
                #fake center
                image = cv2.putText(blank_image, fa4, (int(width/2), int(height/2)), font, 1, (255, 255, 0), 2)
            return image
    else:
        if y < height/2: #right upper
            #fake left lower
            image = cv2.putText(blank_image, fa1, (width-x, height-y), font, 1, (255, 255, 0), 2)
            #fake left upper
            image = cv2.putText(blank_image, fa2, (width-x, y), font, 1, (255, 255, 0), 2)
            #fake right lower
            image = cv2.putText(blank_image, fa3, (x, height-y), font, 1, (255, 255, 0), 2)
            if center:
                #fake right upper
                image = cv2.putText(blank_image, fa4, (x, y), font, 1, (255, 255, 0), 2)
            else:
                #fake center
                image = cv2.putText(blank_image, fa4, (int(width/2), int(height/2)), font, 1, (255, 255, 0), 2)
            return image

        else: #right lower
            #fake left lower
            image = cv2.putText(blank_image, fa1, (x, height-y), font, 1, (255, 255, 0), 2)
            #fake left upper
            image = cv2.putText(blank_image, fa2, (width-x, height-y), font, 1, (255, 255, 0), 2)
            #fake right upper
            image = cv2.putText(blank_image, fa3, (width-x, y), font, 1, (255, 255, 0), 2)
            if center:
                #fake right lower
                image = cv2.putText(blank_image, fa4, (x, y), font, 1, (255, 255, 0), 2)
            else:
                #fake center
                image = cv2.putText(blank_image, fa4, (int(width/2), int(height/2)), font, 1, (255, 255, 0), 2)
            return image
    
def xyTangent(c):
    #a = angle clockwise from 12:00 o'clock
    a = np.random.randint(1,361)
    #c = length of tangent

    if a == 360: # Straight up
        x = width/2
        y = (height/2) - c
    elif a == 90: #Right
        x = width/2 + c
        y = height/2
    elif a == 180: #Down
        x = width/2
        y = (height/2) + c
    elif a == 270: #Left
        x = width/2 - c
        y = height/2

    elif 0 < a < 90:
        x = width/2 + np.sin(a)*c #x right from center
        y = height/2 - np.cos(a)*c #y up from center (negative direction)
        
    elif 90 < a < 180:
        a = a-90
        y = height/2 + np.sin(a)*c #y down from center
        x = width/2 + np.cos(a)*c #x right from center
        
    elif 180 < a < 270:
        a = a-180
        x = width/2 - np.sin(a)*c #x left from center (negative direction)
        y = height/2 + np.cos(a)*c #y down from center
        
    else:
        a = a-270
        y = height/2 - np.sin(a)*c #y up from center (negative direction)
        x = width/2 - np.cos(a)*c #x left from center (negative direction)

    return int(x), int(y)

# Main loop
correct = 0  # Number of correct answers
wrong_total = 0
center = True  # Was the last question on center
round = 0  # Round number
while True:

    # Ask player name
    if (name == ""):
        name = name_input()
    # Countown before first round
    if (round == 0):
        countDown()

    # Correct / False = False before correct answer
    cf = False

    # answer time starts here
    start = pt()

    # increment round number
    round += 1

    # Generate numbers that add to 0-9
    a, b = question()
    answer = a+b

    # Generate fake anwers
    fa1 = question(True)
    fa2 = question(True)
    fa3 = question(True)
    fa4 = question(True)
    print(f"fa1:{fa1} fa2:{fa2} fa3:{fa3} fa4:{fa4}")

    # Form a question string from the generated numbers. 50% chance for the order
    if np.random.choice([0, 1]) == 0:
        qstring = str(a)+"+"+str(b)
        fake_st = str(a)+"-"+str(b)
    else:
        qstring = str(b)+"+"+str(a)
        fake_st = str(b)+"-"+str(a)

    # Blank screen images before every cycle
    image = np.zeros((height, width, 3), np.uint8)
    blank_image = np.zeros((height, width, 3), np.uint8)
    cv2.imshow('appi', image)

    # Calculate the area where the numbers can appear
    # x = int(width/2+(radius(1)))
    # y = int(height/2+(radius(2)))
    #Testing: get x and y from random 0-360dg + distance coordinates
    x, y = xyTangent(radius(1))
    if x < 10:
        x = 10
    if x > width-80:
        x = width - 80

    if y < 30:
        y = 30
    if y > height-50:
        y = height - 50    

    # If previous question was in a center, place question away from center of screen with a 75% chance
    if(center == True and random.randrange(4) != 0):
        image = cv2.putText(blank_image, qstring, (x, y),
                            font, 1, (255, 255, 0), 2)
        center = False

    # If previous question was away from a center, place question directly to center of screen
    else:
        image = cv2.putText(blank_image, qstring, (int(
            width/2), int(height/2)), font, 1, (255, 255, 0), 2)
        center = True

    #Draw fake distraction numbers in a-b style
    #image = drawDistracion(image,fa1,fa2,fa3,fa4,x,y,center)

    # Show question
    cv2.imshow('appi', image)

    # Time for how long the question will be visible
    t1 = timeVisible(round)
    print(t1)

    # Here we wait if key is pressed while question is still visible
    key = cv2.waitKey(t1)

    # Print blanc screen after t1 has passed to hide the question
    image = np.zeros((height, width, 3), np.uint8)
    blank_image = np.zeros((height, width, 3), np.uint8)

    # If key NOT pressed while question was visible: hide number and wait for key to be pressed:
    cv2.imshow('appi', blank_image)
    if key == -1:
        key = cv2.waitKey(0)  # Wait till key is pressed
    else:
        pass

    # Translate keypad keypresses to correct format
    key = findKey(key)

    # QUIT WHEN q IS PRESSED (no file saving)
    if key == ord('q') or key == ord('Q'):
        t2 = pt() - start
        cv2.destroyAllWindows()
        print(name + ": " + str(correct), "Correct")
        exit()

    # CORRECT ANSWER
    elif key == ord(str(answer)):
        t2 = pt() - start
        # number pressed = answer
        correct += 1
        cf = True  # was correct
        # Save data on each cycle to a data table. (round_no, x_coordinate, y_coordinate, number1, number2, time_showing, time_took_to_answer, correct_false)
        saveData(round, x, y, a, b, t1, t2, cf)
        pass

    # CHEAT AND MARK CORRECT ANSWER AND CONTINUE GAME
    elif key == ord('j') or key == ord('J'):
        t2 = pt() - start
        correct += 1
        cf = True  # was correct
        # Save data on each cycle to a data table. (round_no, x_coordinate, y_coordinate, number1, number2, time_showing, time_took_to_answer, correct_false)
        saveData(round, x, y, a, b, t1, t2, cf)
        pass

    # WRONG ANSWER
    else:
        wrong_total += 1
        t2 = pt() - start

        wc = False  # was false
        # Save data on each cycle to a data table. (round_no, x_coordinate, y_coordinate, number1, number2, time_showing, time_took_to_answer, correct_false)
        saveData(round, x, y, a, b, t1, t2, cf)

        if wrong_total < wrong:
            pass
        else: #quit game when wrong_total >= wrong
            
            print(name + ": " + str(correct), "Correct")

            # Save data to file
            filedata = zip(round_no, x_coordinate, y_coordinate, number1,
                        number2, time_showing, time_took_to_answer, correct_false)
            dataToFile(str(name), str(screen_size), headers, filedata)

            cv2.destroyAllWindows()
            exit()

    # print the time that took to answer. For testing!
    print("This round lasted: " + str(t2/1000000000))
    key = None
