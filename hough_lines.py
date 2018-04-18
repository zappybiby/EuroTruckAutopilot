import cv2
import numpy as np

starty = 1
endy = 1000


def hough_lines(warped, original):
    linesP = cv2.HoughLinesP(warped, 1, np.pi / 180, 50, None, 25, 150)

    if linesP is not None:
        for i in range(0, len(linesP)):
            #print("# of lines:", len(linesP))

            l = linesP[i][0]
            x1 = l[0]
            y1 = l[1]
            x2 = l[2]
            y2 = l[3]

            slope = (y2 - y1) / (x2 - x1)

            if slope < 0:
                for x1, y1, x2, y2 in linesP[i]:
                    if (np.isnan(x1) == False) and (np.isnan(y1) == False) and (np.isnan(x2) == False) and (
                            np.isnan(y2) == False):
                        if ((x2 - x1) != 0) and ((y2 - y1) != 0):
                            left_avg_slope = (y2 - y1) / (x2 - x1)
                            left_avg_intercept = y1 - left_avg_slope * x1
                            left_startx = int((starty - left_avg_intercept) / left_avg_slope)
                            left_endx = int((endy - left_avg_intercept) / left_avg_slope)
                            cv2.line(original, (left_startx, starty), (left_endx, endy), (0, 0, 255), 3)

            if slope > 0:
                for x1, y1, x2, y2 in linesP[i]:
                    if (np.isnan(x1) == False) and (np.isnan(y1) == False) and (np.isnan(x2) == False) and (
                            np.isnan(y2) == False):
                        if ((x2 - x1) != 0) and ((y2 - y1) != 0):
                            right_avg_slope = (y2 - y1) / (x2 - x1)
                            right_avg_intercept = y1 - right_avg_slope * x1
                            right_startx = int((starty - right_avg_intercept) / right_avg_slope)
                            right_endx = int((endy - right_avg_intercept) / right_avg_slope)
                            cv2.line(original, (right_startx, starty), (right_endx, endy), (255, 0, 0), 3)

            cv2.namedWindow("Test2", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Test2", 500, 500)
            cv2.moveWindow("Test2", -940, 0)
            cv2.imshow("Test2", original)
            cv2.waitKey(1)
