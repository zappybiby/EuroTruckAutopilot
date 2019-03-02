import cv2
import numpy as np

import image_process


def perspective_transform(capture):

    capture_width = capture.shape[1]
    capture_height = capture.shape[0]

    # ROI values determined on 1920x1080 window and are then scaled for different resolutions
    roi_top_left = (int(capture_width * (85 / 192)), int(capture_height * (103 / 216)))
    roi_top_right = (int(capture_width * (55 / 96)), int(capture_height * ( 103/216)))
    roi_bottom_left = (int(capture_width * (25 / 96)), int(capture_height * (13 / 18)))
    roi_bottom_right = (int(capture_width * (35/48)), int(capture_height * (13 / 18)))
    roi = np.float32([roi_top_left, roi_top_right, roi_bottom_right, roi_bottom_left])

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((roi_bottom_right[0] - roi_bottom_left[0]) ** 2) + ((roi_bottom_right[1] - roi_bottom_left[1]) ** 2))
    widthB = np.sqrt(((roi_top_right[0] - roi_top_left[0]) ** 2) + ((roi_top_right[1] - roi_top_left[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((roi_top_right[0] - roi_bottom_right[0]) ** 2) + ((roi_top_right[1] - roi_bottom_right[1]) ** 2))
    heightB = np.sqrt(((roi_top_left[0] - roi_bottom_left[0]) ** 2) + ((roi_top_left[1] - roi_bottom_left[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(roi, dst)
    warped = cv2.warpPerspective(capture, M, (maxWidth, maxHeight))
    resized_warped = cv2.resize(warped, None, fx=0.5, fy=0.5)
    image_process.pre_process(capture, resized_warped)
