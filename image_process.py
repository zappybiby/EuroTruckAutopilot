import cv2
import numpy as np

import hough_lines


def pre_process(warped, original):
    blur = cv2.GaussianBlur(warped, (15, 15), 0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 23, -3)
    merged_lines = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))

    # TODO: Filter out the HSV values that contain guardrails and other artifacts
    # remove_guardrails = cv2.inRange(hsv, np.array([10,100,75]), np.array([35,255,255]))'

    cv2.namedWindow("adaptiveThreshold", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("adaptiveThreshold", 450, 500)
    cv2.moveWindow("adaptiveThreshold", -1380, 300)
    cv2.imshow("adaptiveThreshold", adaptive_thresh)
    cv2.waitKey(1)

    cv2.namedWindow("merged_lines", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("merged_lines", 450, 500)
    cv2.moveWindow("merged_lines", -940, 300)
    cv2.imshow("merged_lines", merged_lines)
    cv2.waitKey(1)

    hough_lines.hough_lines(merged_lines, original)
