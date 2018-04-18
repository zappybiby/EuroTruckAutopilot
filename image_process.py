import cv2
import numpy as np

import hough_lines


def pre_process(warped, original):
    blur2 = cv2.GaussianBlur(warped, (21, 21), 0)

    gray = cv2.cvtColor(blur2, cv2.COLOR_BGR2GRAY)
    # ret3, th4 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # print(ret3)
    # TODO: otsu threshold almost ideal, but too  much variance. May want to average its return value...
    ret, th3 = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

    # TODO: Canny paramaters are the worst
    canny = cv2.Canny(th3, 80, 300)
    merge = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, np.ones((21, 21), np.uint8))

    cv2.namedWindow("merge", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("merge", 500, 500)
    cv2.moveWindow("merge", -1500, 0)
    cv2.imshow("merge", merge)
    cv2.waitKey(1)
    hough_lines.hough_lines(merge, original)
