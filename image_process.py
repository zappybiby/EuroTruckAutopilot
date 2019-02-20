import cv2
import numpy as np
import keyboard
import hough_lines

a=0
b=0
def pre_process(capture, warped, original):
    global a, b
    #blur = cv2.GaussianBlur(original, (5, 5), 0)
    hsv = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)
    # remove road noise (gray)
    mask = cv2.inRange(hsv, np.uint8([0,0,0]), np.uint8([179, 255, 70]))
    mask_inv = cv2.bitwise_not(mask)

    noise_remove = cv2.bitwise_and(hsv, hsv, mask = mask_inv)
    gray = cv2.cvtColor(noise_remove, cv2.COLOR_BGR2GRAY)
    equ = cv2.equalizeHist(gray)
    #canny = cv2.Canny(equ, 200, 670)

    # if keyboard.is_pressed('t'):
    #     a += 10
    #     print("a:", a)
    # if keyboard.is_pressed('y'):
    #     b += 10
    #     print("b:", b)
    # if keyboard.is_pressed('g'):
    #     a -= 10
    #     print("a", a)
    # if keyboard.is_pressed('h'):
    #     b -= 10
    #     print("b:", b)
    cv2.namedWindow("threshold", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("threshold", 450, 500)
    cv2.moveWindow("threshold", -940, 300)
    cv2.imshow("threshold", equ)
    cv2.waitKey(1)

    hough_lines.hough_lines(equ, original)
