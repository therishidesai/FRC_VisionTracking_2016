import cv2
import numpy as np

cap = cv2.VideoCapture(1)
cap.open(1)

while True:

    frame,_=cap.read()

    if frame:
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
            #get moments data from contour
            moments = cv2.moments(cnt)
            #get center x and y value from image
            center_x = int(moments["m10"]/moments["m00"])
            center_y = int(moments["m01"]/moments["m00"])
            print "x = "+str(center_x)+" , y = "+str(center_y)

        #show image
        cv2.imshow('frame',frame)

        #close if delay in camera feed is too long
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

cv2.destroyAllWindows()
        

        
