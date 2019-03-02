import cv2

import hough_lines


def pre_process(capture, warped):
    gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray, 3, 75, 75)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl1 = clahe.apply(blur)

    canny = cv2.Canny(cl1, 100, 200)

    cv2.namedWindow("threshold", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("threshold", 450, 500)
    cv2.moveWindow("threshold", -940, 300)
    cv2.imshow("threshold", canny)
    cv2.waitKey(1)

    hough_lines.hough_lines(canny, warped)
