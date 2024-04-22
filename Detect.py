import cv2
import numpy as np
import serial
from time import sleep
# Serial communication using arduino
# arduino = serial.Serial('COM6', 9600) 
# Initialize video capture
cap = cv2.VideoCapture(0)
cv2.namedWindow('Circle Detection', cv2.WINDOW_NORMAL)
LaserX = 0
LaserY = 0
CircleX = 0
CircleY = 0
theta2 = 122
theta1 = 90
while True:
    # Capture frame
    ret, frame = cap.read()
    if not ret:
        print("End of video.")
        break
    
    # Laser Point Detection 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        moments = cv2.moments(largest_contour)
        if moments["m00"] != 0:
            cX = int(moments["m10"] / moments["m00"])
            cY = int(moments["m01"] / moments["m00"])
            center = (cX, cY)
            LaserX = cX
            LaserY = cY
            print("LX",cX,"LY",cY)
            cv2.circle(frame, center, 5, (0, 255, 0), -1)
            # Draw circle around laser point
            cv2.circle(frame, center, 20, (0, 255, 255), 2)  # Yellow circle with radius 20
    
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply median blur to reduce noise
    frame_blurred = cv2.medianBlur(frame, 5)

    # Use Randomized Hough Transform for circle detection
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=500,
                               param1=100, param2=50, minRadius=10, maxRadius=500)

    # Draw circles if detected
    if circles is not None:
        circles = np.uint16(np.around(circles))  # Convert circles to integers
        for circle in circles[0, :]:
            x, y, radius = circle[0], circle[1], circle[2]
            print("CX",x,"CY",y)
            cv2.circle(frame, (x, y), radius, (0, 255, 0), 4)  # Draw the circle
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 4)  # Draw the center of the circle
            CircleX = x
            CircleY = y
            
               
                # Limit theta1 and theta2 within specified ranges
            if   LaserY - CircleY > 0 and abs(LaserY - CircleY) > 20:
                    theta2 = max(theta2 - 1, 70)
            elif LaserY - CircleY < 0 and abs(LaserY - CircleY) > 20:
                    theta2 = min(theta2 + 1, 180)

            if LaserX - CircleX > 0 and abs(LaserX - CircleX) > 20:
                    theta1 = min(theta1 + 1, 180)
            elif LaserX - CircleX < 0 and abs(LaserX - CircleX) > 20:
                    theta1 = max(theta1 - 1, 0)
            if abs(CircleY - LaserY) <= (radius-20) and abs(LaserX - CircleX) <= (radius-20):
                    theta1=theta1
                    theta2=theta2
            

            print("theta1",theta1,"theta2",theta2)   
    # Show frame of Circle Detection
    cv2.imshow('Circle Detection', frame)
    print(str(int(CircleY - LaserY)) + " " + str(int(CircleX - LaserX)) + "\n")
    # arduino.write(f"{theta1},{theta2}\n".encode())
    sleep(0.2) 
    # Check for exit key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()