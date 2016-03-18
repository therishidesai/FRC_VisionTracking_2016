#!/usr/bin/env python

import cv2
import numpy as np


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
    
                   
def main():
    cap = cv2.VideoCapture(0)
    #cap.open(0)

    while cap.isOpened():

        _,frame=cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #Range for green light reflected off of the tape. Need to tune.
        lower_green = np.array([50,100,100], dtype=np.uint8)
        upper_green = np.array([70,255,255], dtype=np.uint8)

        #Threshold the HSV image to only get the green color.
        mask = cv2.inRange(hsv, lower_green, upper_green)
        #Gets contours of the thresholded image.
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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
            text_coordinate_1 = (1,15)
            text_coordinate_2=(1,40)
            text_coordinate_3=(1,70)
            #cv2.line(frame, center, (center, (0,0,255), 3)
            center_str_x = "x = "+str(center[0])
            center_str_y = "y = "+str(center[1])
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, "Center", text_coordinate_1, font, 0.7, (0,0,255), 2)
            cv2.putText(frame, center_str_x, text_coordinate_2, font, 0.7, (0,0,255), 2)
            cv2.putText(frame, center_str_y, text_coordinate_3, font, 0.7, (0,0,255), 2)

        
        #show image
        cv2.imshow('frame',frame)
        cv2.imshow('mask', mask)
        cv2.imshow('HSV', hsv)
        #close if delay in camera feed is too long
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    #runs main
    main()
        

        
