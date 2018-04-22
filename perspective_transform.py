import cv2
import keyboard
import numpy as np

import image_process

a = 20
b = 40
c = 60
d = -70


def perspective_transform(window):
    global a, b, c, d

    window_resized = cv2.resize(window, (640, 360))
    original_resized = window_resized.copy()

    # Remove upper half of image
    cropped_window = window_resized[int(window_resized.shape[0] / 2):int(window_resized.shape[0])]
    cropped_original = original_resized[int(original_resized.shape[0] / 2):int(original_resized.shape[0])]

    width = cropped_window.shape[1]
    height = cropped_window.shape[0]
    window_size = (width, height)

    width_original = cropped_original.shape[1]
    height_original = cropped_original.shape[0]
    original_size = (width_original, height_original)

    # Cut my life into pieces. This is my last resort.
    if keyboard.is_pressed('t'):
        a += 100
        print("a:", a)
    if keyboard.is_pressed('y'):
        b += 100
        print("b:", b)
    if keyboard.is_pressed('u'):
        c += 10
        print("c:", c)
    if keyboard.is_pressed('i'):
        d += 10
        print("d:", d)
    if keyboard.is_pressed('g'):
        a -= 100
        print("a", a)
    if keyboard.is_pressed('h'):
        b -= 100
        print("b:", b)
    if keyboard.is_pressed('j'):
        c -= 10
        print("c:", c)
    if keyboard.is_pressed('k'):
        d -= 10
        print("d:", d)

    src = np.float32(
        [[(-a), height - b],
         [width + a, height - b],
         [width / 2 + c, (height / 2) + d],
         [width / 2 - c, (height / 2) + d]])

    dst = np.float32(
        [[0, height],
         [width, height],
         [width, 0],
         [0, 0]])

    m = cv2.getPerspectiveTransform(src, dst)

    warped = cv2.warpPerspective(cropped_window, m, window_size, flags=cv2.INTER_LINEAR)
    original_warped = cv2.warpPerspective(cropped_original, m, original_size, flags=cv2.INTER_LINEAR)

    cv2.namedWindow("original_warped", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("original_warped", 450, 500)
    cv2.moveWindow("original_warped", -1820, 300)
    cv2.imshow("original_warped", original_warped)
    cv2.waitKey(1)

    image_process.pre_process(warped, original_warped)
