import datetime

import cv2
import numpy as np

import monitors

window_x_position = monitors.get_window_x_position(450)

starty = 1
endy = 1000


def hough_lines(warped, original):
    lines_p = cv2.HoughLinesP(warped, 1, np.pi / 180, 50, None, 50, 300)
    if lines_p is not None:
        length = len(lines_p)
        extrapolated_lines = []
        start_time = datetime.datetime.now().time().microsecond
        for i in range(0, length):
            for j in range(0, length):
                if i != j:
                    line_1 = lines_p[i][0]
                    line_2 = lines_p[j][0]

                    if False not in (line_1.all(), line_2.all()):
                        line_1_x1 = line_1[0]
                        line_1_y1 = line_1[1]
                        line_1_x2 = line_1[2]
                        line_1_y2 = line_1[3]

                        line_2_x1 = line_2[0]
                        line_2_y1 = line_2[1]
                        line_2_x2 = line_2[2]
                        line_2_y2 = line_2[3]

                        line_x_distance = np.sqrt(np.square(line_2_x1 - line_1_x1) + np.square(line_2_x2 - line_1_x2))
                        line_y_length = np.abs((line_2_y1 + line_1_y1) / 2 - (line_2_y2 + line_1_y2) / 2)
                        distance = (np.sqrt(np.square(line_2_x1 - line_1_x1) + np.square(line_2_y1 - line_1_y1)) +
                                    np.sqrt(np.square(line_2_x2 - line_1_x2) + np.square(line_2_y2 - line_1_y2))) / 2

                        if line_x_distance < 20 and line_y_length > 40 and 10 < distance <= 100:
                            line_3_x1 = (line_2_x1 + line_1_x1) / 2
                            if line_3_x1 not in extrapolated_lines:
                                line_3_y1 = (line_2_y1 + line_1_y1) / 2
                                line_3_x2 = (line_2_x2 + line_1_x2) / 2
                                line_3_y2 = (line_2_y2 + line_1_y2) / 2

                                if 0 not in (
                                        line_3_x1, line_3_x2, line_3_y1, line_3_y2,
                                        np.abs(line_3_x1) - np.abs(line_3_x2),
                                        np.abs(line_3_y1) - np.abs(line_3_y2)):
                                    line_3_avg_slope = (line_3_y2 - line_3_y1) / (line_3_x2 - line_3_x1)
                                    line_3_avg_intercept = line_3_y1 - line_3_avg_slope * line_3_x1
                                    line_3_startx = int((starty - line_3_avg_intercept) / line_3_avg_slope)
                                    right_endx = int((endy - line_3_avg_intercept) / line_3_avg_slope)
                                    extrapolated_lines.append(line_3_x1)
                                    cv2.line(original, (line_3_startx, starty), (right_endx, endy), (0, 0, 255), 3)

        print("# of lines:", length, "found:", len(extrapolated_lines),
              datetime.datetime.now().time().microsecond - start_time)
        cv2.namedWindow("Test2", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Test2", 450, 500)
        cv2.moveWindow("Test2", window_x_position, 0)
        cv2.imshow("Test2", original)
        cv2.waitKey(1)
