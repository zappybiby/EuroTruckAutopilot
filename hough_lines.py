import cv2
import numpy as np

starty = 1
endy = 180
previous_lines = [[0 for x in range(4)] for y in range(2)]


def hough_lines(warped, original):
    global previous_lines
    lines_p = cv2.HoughLinesP(warped, 1, np.pi / 180, 50, None, 50, 300)
    cv2.line(original, (previous_lines[0][0], previous_lines[0][1]), (previous_lines[0][2], previous_lines[0][3]),
             (255, 0, 0), 5)
    cv2.line(original, (previous_lines[1][0], previous_lines[1][1]), (previous_lines[1][2], previous_lines[1][3]),
             (0, 0, 255), 5)
    # cv2.line(original, (int((previous_lines[0][0] + previous_lines[0][2]) / 2), 90),
    #          (int((previous_lines[1][0] + previous_lines[1][2]) / 2), 90), (0, 255, 255), 3)
    if lines_p is not None:
        length = len(lines_p)
        extrapolated_lines = []
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

                        line_1_slope = (line_1_y2 - line_1_y1) / (
                                line_1_x2 - line_1_x1) if line_1_x2 - line_1_x1 != 0 else 0
                        line_2_slope = (line_2_y2 - line_2_y1) / (
                                line_2_x2 - line_2_x1) if line_2_x2 - line_2_x1 != 0 else 0

                        if line_x_distance < 20 and line_y_length > 75 and 5 < distance <= 200:
                            if line_1_x1 not in extrapolated_lines and line_2_x1 not in extrapolated_lines:
                                if 0 not in (
                                        line_1_x1, line_1_x2, line_1_y1, line_1_y2,
                                        np.abs(line_1_x1) - np.abs(line_1_x2),
                                        np.abs(line_1_y1) - np.abs(line_1_y2)):
                                    if line_1_slope < -1 and line_1_x1 < 320 and line_1_x2 < 320:
                                        extrapolated_lines.append(line_1_x1)
                                        line_1_intercept = line_1_y1 - line_1_slope * line_1_x1
                                        line_1_startx = int((starty - line_1_intercept) / line_1_slope)
                                        line_1_endx = int((endy - line_1_intercept) / line_1_slope)
                                        previous_lines[0] = [line_1_startx, starty, line_1_endx, endy]

                                if 0 not in (
                                        line_2_x1, line_2_x2, line_2_y1, line_2_y2,
                                        np.abs(line_2_x1) - np.abs(line_2_x2),
                                        np.abs(line_2_y1) - np.abs(line_2_y2)):
                                    if line_2_slope > 1 and line_2_x1 > 320 and line_2_x2 > 320:
                                        extrapolated_lines.append(line_2_x1)
                                        line_2_intercept = line_2_y1 - line_2_slope * line_2_x1
                                        line_2_startx = int((starty - line_2_intercept) / line_2_slope)
                                        line_2_endx = int((endy - line_2_intercept) / line_2_slope)
                                        previous_lines[1] = [line_2_startx, starty, line_2_endx, endy]

        # print("# of lines:", length, "found:", len(extrapolated_lines),
        #      datetime.datetime.now().time().microsecond - start_time)
        cv2.namedWindow("Test2", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Test2", 450, 500)
        cv2.moveWindow("Test2", -500, 300)
        cv2.imshow("Test2", original)
        cv2.waitKey(1)
