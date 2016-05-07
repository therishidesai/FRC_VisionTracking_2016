# FRC_VisionTracking_2016

This is the on board goal tracker written in Python. The script tracks the goal by its green color then using contours it finds the center of the goal. After getting the center the script calculates the angle the robot has to turn to face the center of the goal.

## Angle Calculation
The program calculates the distance between the center x value and the x value of the centroid of the tracked goal. With the calculated delta_x, the program then calculates the offset angle with the equation:

offset_angle=arctan((delta_x)/(240/tan((Horizontal_Field_of_View/2)))
