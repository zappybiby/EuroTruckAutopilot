import cv2
import numpy as np

import hough_lines


def pre_process(warped, original):
    blur = cv2.GaussianBlur(warped, (15, 15), 0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 23, -3)
    #merged_lines = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))

    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    # TODO: Filter out the HSV values that contain guardrails and other artifacts
    remove_guardrails = cv2.inRange(hsv, np.array([1,90,1]), np.array([179,255,255]))
    final = cv2.subtract(adaptive_thresh,remove_guardrails)
    cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("mask", 450, 500)
    cv2.moveWindow("mask", -1380, 300)
    cv2.imshow("mask", remove_guardrails)
    cv2.waitKey(1)

    cv2.namedWindow("threshold", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("threshold", 450, 500)
    cv2.moveWindow("threshold", -940, 300)
    cv2.imshow("threshold", final)
    cv2.waitKey(1)

    hough_lines.hough_lines(final, original)
