#!/usr/bin/env python

import cv2
import numpy as np
import constants
import math
import logging
#from networktables import NetworkTable
import socket
import pickle
import struct
import time

def get_center(contour):
    #get moments data from contour
    moments = cv2.moments(contour)
    #get center x and y value from image
    center = (0,0)

    if moments["m00"] > 0:
        center_x = int(moments["m10"]/moments["m00"])
        center_y = int(moments["m01"]/moments["m00"])
        #return a tuple with center coordinates
        center = (center_x, center_y)
    return center

def get_delta_x(x):
    #returns difference of X value of center of the tracked object to the targets X value
    return constants.TARGET_X-x

def get_delta_y(y):
    #returns difference of Y value of center of the tracked object to the targets Y value
    return constants.TARGET_Y-y

def get_offset_angle(center_x, center_y):
    delta_x = get_delta_x(center_x)
    tan_ratio = float(math.fabs(delta_x)/constants.DIST_CAM_TO_CENTER)
    angle_radians = math.atan(tan_ratio)
    degrees = float(angle_radians*constants.RADIAN_TO_DEGREE)
    if(delta_x<0):
        #direction = 1 #turn right
        direction = "right"
    else:
        #direction = 0 #turn left
        direction = "left"

    return (degrees, direction)

def main():
    cap = cv2.VideoCapture(1)

    #Set camera values
    #cap.set(3, constants.CAM_WIDTH)
    #cap.set(4, constants.CAM_HEIGHT)
    #time.sleep(2)
    #cap.set(10, constants.CAM_BRIGHTNESS)
    #cap.set(15, constants.CAM_EXPOSURE)
    #logging.basicConfig(level=logging.DEBUG)
    #print cap.get(15)
    #NetworkTable.setIPAddress('10.32.56.2')
    #NetworkTable.setClientMode()
    #NetworkTable.initialize()

    #nt = NetworkTable.getTable('SmartDashboard')

    while cap.isOpened():

        _,frame=cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #Range for green light reflected off of the tape. Need to tune.
        lower_green = np.array(constants.LOWER_GREEN, dtype=np.uint8)
        upper_green = np.array(constants.UPPER_GREEN, dtype=np.uint8)

        #Threshold the HSV image to only get the green color.
        mask = cv2.inRange(hsv, lower_green, upper_green)
        #Gets contours of the thresholded image.
        _,contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #Draw the contours around detected object
        cv2.drawContours(frame, contours, -1, (0,0,255), 3)

        #Get centroid of tracked object.
        #Check to see if contours were found.
        if len(contours)>0:
            #find largest contour
            cnt = max(contours, key=cv2.contourArea)
            #get center
            center = get_center(cnt)
            cv2.circle(frame, center, 3, (0,0,255), 2)
            if(center[0] != 0 and center[1]!=0):
                center_str_x = "x = "+str(center[0])
                center_str_y = "y = "+str(center[1])
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, "Center", constants.TEXT_COORDINATE_1, font, 0.7, (0,0,255), 2)
                cv2.putText(frame, center_str_x, constants.TEXT_COORDINATE_2, font, 0.7, (0,0,255), 2)
                cv2.putText(frame, center_str_y, constants.TEXT_COORDINATE_3, font, 0.7, (0,0,255), 2)
                angle, direction = get_offset_angle(center[0], center[1])
                cv2.putText(frame, "Angle: "+str(angle),constants.TEXT_COORDINATE_4, font, 0.7, (0,0,255), 2)
                #nt.putNumber('CameraAngle', angle)
                cv2.putText(frame, "Turn "+direction, constants.TEXT_COORDINATE_5, font, 0.7, (0,0,255), 2)
                '''if direction == right:
                    nt.putNumber('Direction', 0)
                else:
                    nt.putNumber('Direction', 1)'''

        #show image
        cv2.imshow('frame',frame)
        cv2.imshow('mask', mask)
        cv2.imshow('HSV', hsv)

        #close if delay in camera feed is too long
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    #runs main
    main()
