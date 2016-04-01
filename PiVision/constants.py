#!/usr/bin/env python

import math
#This is the constants file that has allo f the important constants for the Tower Tracker.

#Camera Constants
CAM_EXPOSURE = 0.01
CAM_BRIGHTNESS = 0.05
#CAM_EXPOSURE=0.3
#CAM_BRIGHTNESS=0.6
CAM_WIDTH = 640
CAM_HEIGHT = 480

#Threshold values
LOWER_GREEN = [30,100,100]
UPPER_GREEN = [90,255,255]

#Target values
TARGET_X = 320
TARGET_Y = 240
PIXELS_TO_DEGREES = 0

#Image Text
TEXT_COORDINATE_1 = (1,15)
TEXT_COORDINATE_2=(1,40)
TEXT_COORDINATE_3=(1,70)
TEXT_COORDINATE_4=(1,100)
TEXT_COORDINATE_5=(1,130)

#Camera Angles and Distances
HORIZ_FIELD_OF_VIEW=61 #angle in degrees
DIST_CAM_TO_CENTER= 543.252198

#Trig Data
RADIAN_TO_DEGREE = float(180.0/math.pi)
