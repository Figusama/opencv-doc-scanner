import cv2 as cv
import numpy as np

def hsv_detect(img):
    
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    lower_white = np.array([0, 0, 180])
    upper_white = np.array([180, 30, 255])

    mask = cv.inRange(hsv, lower_white, upper_white)

    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    doc_contours = None
    for c in contours:
        area = cv.contourArea(c)
        h, w = img.shape[:2]
        if area > 0.9 * h * w or area < 0.05 * h * w:
            continue
        

        peri = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, 0.02*peri, True)
        if len(approx) == 4:
            doc_contours = approx
            break
    
    return doc_contours


