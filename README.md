# visual_area_number_game
Game that shows a simple number adding questions on different parts of screen for a short time to determine the "heatmap" of visual area of understanding of what you see

Recuirements:
- Python 3.x

Imports:
  import sys
  from cv2 import WND_PROP_OPENGL, cv2
  from time import sleep
  from time import perf_counter_ns as pt
  from datetime import datetime
  import numpy as np
  import string
  import random
  import csv
  
 Run:
 - python3 numberadding.py
 
 Commandline arguments (optional):
 -myname -maxtimenumbershowinginms -mintimenumbershowinginms
 
 How to run exmaples:
 - python3 numberadding.py (name input will be propted)
 - python3 numberadding.py -muburns (no name input prompt)
 - python3 numberadding.py -mrburns -2000 -200 (custom times for max and min times for number question on screen)

##################################################################################################################
###                             README
##################################################################################################################

How much do you understand of what you see?
To be more spesific, how far off from the center of your vision can something that requires thinking be at?

Description of the test environment (COMPLETELY UNDETERMINED)
- The subject will be sitting and staring a screen from a distance of 50cm(?)
- The center of the screen will be leveled to eyesight level (+-?)
- The minimum size of the screen/monitor for this game is still indeterminate!! But it will need to be a lot bigger than 15". Closer to 32". THIS IS VITAL TO FIGURE OUT THE CORRECT SCALE!
- The subject will use a 9-digit keypad to insert required data (voice?)

PROCEDURE:
- The screen will be in full screen mode displaying a crosshair(?) or a circle(?) in the center of the screen. Or nothing?
- A random numbers whose sum is from 0 to 9 will appear on the center of the screen. i.ex. 0+0, 2+2, 8+1, 5+0, 3+3, 7+1. Gradyally appearing a shorter and shorter amount of time
(The size and color of the numbers and the backgroud will vary and will be recorded?)
- The subject must give a correct answer to the sum by pressing a corresponding number from the 9-digit keypad
- The system will record the time it took the pair of numbers to appear to the point the subject gave the correct or incorrect input from the keypad
- Gradually every other appearing pair of nubers will start to appear in off center of the screen. In random position but slowly moving away from the center
Every other on the center, and every other randomly off center.
- After hundreds of tests it will be possible to create an area where the subjects will get the answer right and where the answers will start to go wrong as a heatmap. This will represent the visual area of understanding of the subject.
