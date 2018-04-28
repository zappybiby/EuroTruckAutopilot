import datetime
import keyboard
import cv2
import numpy as np

starty = 1
endy = 1000

a = 10
def hough_lines(warped, original):
    global a
    lines_p = cv2.HoughLinesP(warped, 1, np.pi / 180, 50, None, 50, 300)
    if keyboard.is_pressed('r'):
        a += 5
        print("a:", a)
    if keyboard.is_pressed('f'):
        a -= 5
        print("a", a)
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

                        line_1_slope = (line_1_y2 - line_1_y1) / (line_1_x2 - line_1_x1)
                        line_2_slope = (line_2_y2 - line_2_y1) / (line_2_x2 - line_2_x1)

                        if line_x_distance < 20 and line_y_length > 100 and 5 < distance <= 100:
                            #if line_1_x1 not in extrapolated_lines and line_2_x1 not in extrapolated_lines:

                                if 0 not in (
                                        line_1_x1, line_1_x2, line_1_y1, line_1_y2,
                                        np.abs(line_1_x1) - np.abs(line_1_x2),
                                        np.abs(line_1_y1) - np.abs(line_1_y2)) and line_1_slope < -1:
                                    extrapolated_lines.append(line_1_x1)
                                    line_1_intercept = line_1_y1 - line_1_slope * line_1_x1
                                    line_1_startx = int((starty - line_1_intercept) / line_1_slope)
                                    line_1_endx = int((endy - line_1_intercept) / line_1_slope)
                                    cv2.line(original, (line_1_startx, starty), (line_1_endx, endy), (255, 0, 0), 3)
                                if 0 not in (
                                        line_2_x1, line_2_x2, line_2_y1, line_2_y2,
                                        np.abs(line_2_x1) - np.abs(line_2_x2),
                                        np.abs(line_2_y1) - np.abs(line_2_y2)) and line_2_slope > 1:
                                    extrapolated_lines.append(line_2_x1)
                                    line_2_intercept = line_2_y1 - line_2_slope * line_2_x1
                                    line_2_startx = int((starty - line_2_intercept) / line_2_slope)
                                    line_2_endx = int((endy - line_2_intercept) / line_2_slope)
                                    cv2.line(original, (line_2_startx, starty), (line_2_endx, endy), (0, 0, 255), 3)
                            # line_3_x1 = (line_2_x1 + line_1_x1) / 2
                            # if line_3_x1 not in extrapolated_lines:
                            #     line_3_y1 = (line_2_y1 + line_1_y1) / 2
                            #     line_3_x2 = (line_2_x2 + line_1_x2) / 2
                            #     line_3_y2 = (line_2_y2 + line_1_y2) / 2
                            # 
                            #     if 0 not in (
                            #             line_3_x1, line_3_x2, line_3_y1, line_3_y2,
                            #             np.abs(line_3_x1) - np.abs(line_3_x2),
                            #             np.abs(line_3_y1) - np.abs(line_3_y2)):
                            #         line_3_avg_slope = (line_3_y2 - line_3_y1) / (line_3_x2 - line_3_x1)
                            #         line_3_avg_intercept = line_3_y1 - line_3_avg_slope * line_3_x1
                            #         line_3_startx = int((starty - line_3_avg_intercept) / line_3_avg_slope)
                            #         right_endx = int((endy - line_3_avg_intercept) / line_3_avg_slope)
                            #         extrapolated_lines.append(line_3_x1)
                            #         cv2.line(original, (line_3_startx, starty), (right_endx, endy), (0, 0, 255), 3)
                            #         # iterate through previous 10 lines
                            #         previous_lines = extrapolated_lines[::10]
                            #         print(previous_lines)

        # print("# of lines:", length, "found:", len(extrapolated_lines),
        #      datetime.datetime.now().time().microsecond - start_time)
        cv2.namedWindow("Test2", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Test2", 450, 500)
        cv2.moveWindow("Test2", -500, 300)
        cv2.imshow("Test2", original)
        cv2.waitKey(1)
