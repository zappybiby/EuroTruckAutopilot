import cv2
import numpy as np

import hough_lines


def pre_process(capture, warped, original):

    #blur = cv2.GaussianBlur(original, (15, 15), 0)
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    #adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 23, -3)
    edges = cv2.Canny(gray, 150, 200)

    cv2.namedWindow("threshold", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("threshold", 450, 500)
    cv2.moveWindow("threshold", -940, 300)
    cv2.imshow("threshold", edges)
    cv2.waitKey(1)

    hough_lines.hough_lines(edges, original)
