import cv2
import numpy as np

start_y = 1
end_y = 1000


def hough_lines(warped, original):
    hough_lines_p = cv2.HoughLinesP(warped, 1, np.pi / 180, 50, None, 25, 150)

    if hough_lines_p is not None:
        for i in range(0, len(hough_lines_p)):
            line = hough_lines_p[i][0]
            x1 = line[0]
            y1 = line[1]
            x2 = line[2]
            y2 = line[3]

            slope = (y2 - y1) / (x2 - x1)

            if slope < 0:
                for x1, y1, x2, y2 in hough_lines_p[i]:
                    if not np.isnan(x1) and not np.isnan(y1) and not np.isnan(x2) and not np.isnan(y2) and \
                            ((x2 - x1) != 0) and ((y2 - y1) != 0):
                            left_avg_slope = (y2 - y1) / (x2 - x1)
                            left_avg_intercept = y1 - left_avg_slope * x1
                            left_start_x = int((start_y - left_avg_intercept) / left_avg_slope)
                            left_end_x = int((end_y - left_avg_intercept) / left_avg_slope)
                            cv2.line(original, (left_start_x, start_y), (left_end_x, end_y), (0, 0, 255), 3)
            elif slope > 0:
                for x1, y1, x2, y2 in hough_lines_p[i]:
                    if not np.isnan(x1) and not np.isnan(y1) and not np.isnan(x2) and not np.isnan(y2) and \
                            ((x2 - x1) != 0) and ((y2 - y1) != 0):
                            right_avg_slope = (y2 - y1) / (x2 - x1)
                            right_avg_intercept = y1 - right_avg_slope * x1
                            right_start_x = int((start_y - right_avg_intercept) / right_avg_slope)
                            right_end_x = int((end_y - right_avg_intercept) / right_avg_slope)
                            cv2.line(original, (right_start_x, start_y), (right_end_x, end_y), (255, 0, 0), 3)

            cv2.namedWindow("Test2", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Test2", 500, 500)
            cv2.moveWindow("Test2", -940, 0)
            cv2.imshow("Test2", original)
            cv2.waitKey(1)
