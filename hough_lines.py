import datetime

import cv2
import numpy as np

starty = 1
endy = 1000


def hough_lines(warped, original):
    global a
    lines_p = cv2.HoughLinesP(warped, 1, np.pi / 180, 50, None, 50, 300)
    if lines_p is not None:
        length = len(lines_p)
        extrapolated_lines = []
        previous_line_1 = []
        data = []
        previous_line_2 = []
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

                        # TODO: DO I STILL NEED TO CALCULATE SLOPE HERE TO DETERMINE LEFT/RIGHT LANE? ALTERNATIVES?
                        line_1_slope = (line_1_y2 - line_1_y1) / (line_1_x2 - line_1_x1)
                        line_2_slope = (line_2_y2 - line_2_y1) / (line_2_x2 - line_2_x1)

                        if line_x_distance < 20 and line_y_length > 75 and 5 < distance <= 200:

                            if line_1_x1 not in extrapolated_lines and line_2_x1 not in extrapolated_lines:

                                if 0 not in (
                                        line_1_x1, line_1_x2, line_1_y1, line_1_y2,
                                        np.abs(line_1_x1) - np.abs(line_1_x2),
                                        np.abs(line_1_y1) - np.abs(line_1_y2)):

                                    # TODO: USE SLOPE/XPOS FOR CALCULATING LEFT/RIGHT LANES? HIST?
                                    # if line_1_slope > -1 and line_1_x1 < 400 and line_1_x2 < 400:
                                    if line_1_x1 < 320 and line_1_x2 < 320:
                                        extrapolated_lines.append(line_1_x1)
                                        line_1_intercept = line_1_y1 - line_1_slope * line_1_x1
                                        line_1_startx = int((starty - line_1_intercept) / line_1_slope)
                                        line_1_endx = int((endy - line_1_intercept) / line_1_slope)
                                        # cv2.line(original, (line_1_startx, starty), (line_1_endx, endy), (255, 0, 0), 5)
                                        previous_line_1.append([line_1_startx, line_1_endx])

                                        for i in range(0, len(previous_line_1)):
                                            value = [line_1_startx, line_1_endx]
                                            lasts = [data[j]['value'] for j in range(i - 9, i) if j >= 0]
                                            lasts.append(value)
                                            avg10 = (np.mean(lasts, axis=0)).astype(int)
                                            # WHAT THE HECK IS THIS DOING? IT WORKS SOMEHOW
                                            data += [{'value': value, 'avg10': avg10}]
                                            # TODO: DRAW NEW LINE EVERY 10 LINES
                                            # Drawing here would draw each avg line, creating tons of lines.
                                            # cv2.line(original, (avg10[0], starty), (avg10[1], endy), (0, 255, 255), 1)

                                if 0 not in (
                                        line_2_x1, line_2_x2, line_2_y1, line_2_y2,
                                        np.abs(line_2_x1) - np.abs(line_2_x2),
                                        np.abs(line_2_y1) - np.abs(line_2_y2)):

                                    # if line_2_slope > 1 and line_2_x1 > 400 and line_2_x2 > 400:
                                    if line_2_x1 > 320 and line_2_x2 > 320:

                                        extrapolated_lines.append(line_2_x1)
                                        line_2_intercept = line_2_y1 - line_2_slope * line_2_x1
                                        line_2_startx = int((starty - line_2_intercept) / line_2_slope)
                                        line_2_endx = int((endy - line_2_intercept) / line_2_slope)
                                        # cv2.line(original, (line_2_startx, starty), (line_2_endx, endy), (0, 0, 255), 5)
                                        previous_line_2.append([line_2_startx, line_2_endx])

                                        for i in range(0, len(previous_line_2)):
                                            value = [line_2_startx, line_2_endx]
                                            lasts = [data[j]['value'] for j in range(i - 9, i) if j >= 0]
                                            lasts.append(value)
                                            avg10 = (np.mean(lasts, axis=0)).astype(int)
                                            data += [{'value': value, 'avg10': avg10}]
                                            # TODO: DRAW NEW LINE EVERY 10 LINES
                                            # Drawing here would draw each avg line, creating tons of lines.
                                            # cv2.line(original, (avg10[0], starty), (avg10[1], endy), (0, 255, 255), 1)

        # print("# of lines:", length, "found:", len(extrapolated_lines),
        #      datetime.datetime.now().time().microsecond - start_time)
        cv2.namedWindow("Test2", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Test2", 450, 500)
        cv2.moveWindow("Test2", -500, 300)
        cv2.imshow("Test2", original)
        cv2.waitKey(1)
