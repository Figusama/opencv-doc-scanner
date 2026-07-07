import cv2 as cv
import numpy as np
from contour_detection import contour_detection
from grabcut import grabcut_detection
from match_points import match_points_generation
from hsv_detection import hsv_detect

def find_contour(img):
    height = 500
    ratio = img.shape[0] / height
    img = cv.resize(img, (int(img.shape[1] / ratio), height)) # interpolation is not needed as we are about to blur it anyway.

    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    blur_gray_img = cv.GaussianBlur(gray_img, (5, 5), 0)

    low, up = 70, 200
    edged_blur_gray_img = cv.Canny(blur_gray_img, low, up)

    kernel = np.ones((5, 5), np.uint8)

    edged = cv.morphologyEx(edged_blur_gray_img, cv.MORPH_CLOSE, kernel)

    contour = contour_detection(img, edged)

    if contour is not None:
        print("Its CONTOUR DETECTION")
        return contour, ratio

    contour = hsv_detect(img)
    if contour is not None:
        print("Its HSV")
        return contour, ratio
    

    # corners = hough_lines_detection(img, edged)
    # if corners is not None:
    #     contour = np.array(corners, dtype="float32")
    #     return contour, ratio

    contour = grabcut_detection(img)
    if contour is not None:
        print("Its GRABCUT")
        return contour, ratio

    print("Its Match points")
    return match_points_generation(img), ratio

