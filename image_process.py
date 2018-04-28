import cv2
import numpy as np

import hough_lines


def pre_process(warped, original):
    blur = cv2.GaussianBlur(warped, (15, 15), 0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, -3)
    merge = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

    # median = np.median(merge)
    # lower = int(max(0, (1.0 - 0.33) * median))
    # upper = int(min(255, (1.0 + 0.33) * median))
    # canny = cv2.Canny(merge, lower, upper)
    # merge = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, np.ones((21, 21), np.uint8))

    cv2.namedWindow("adaptiveThreshold", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("adaptiveThreshold", 450, 500)
    cv2.moveWindow("adaptiveThreshold", -1380, 300)
    cv2.imshow("adaptiveThreshold", adaptive_thresh)
    cv2.waitKey(1)

    # cv2.namedWindow("canny", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("canny", 450, 500)
    # cv2.moveWindow("canny", -540, 300)
    # cv2.imshow("canny", canny)
    # cv2.waitKey(1)

    cv2.namedWindow("merge", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("merge", 450, 500)
    cv2.moveWindow("merge", -940, 300)
    cv2.imshow("merge", merge)
    cv2.waitKey(1)

    hough_lines.hough_lines(merge, original)
