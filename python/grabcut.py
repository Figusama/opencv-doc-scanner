import cv2 as cv
import numpy as np


def grabcut_detection(img):
    mask = np.zeros(img.shape[:2], np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)

    h, w = img.shape[:2]

    margin = int(min(h, w) * 0.02)
    rect = (margin, margin, w - margin*2, h - margin*2)

    cv.grabCut(img, mask, rect, bgd_model, fgd_model, 5, cv.GC_INIT_WITH_RECT)

    mask2 = np.where((mask == cv.GC_FGD) | (mask == cv.GC_PR_FGD), 255, 0).astype('uint8')


    contours, _ = cv.findContours(mask2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None

    c = max(contours, key=cv.contourArea)

    peri = cv.arcLength(c, True)

    approx = cv.approxPolyDP(c, 0.02 * peri, True)

    if len(approx) != 4:

        for epsilon in [0.03, 0.04, 0.05, 0.08, 0.1]:
            approx = cv.approxPolyDP(c, epsilon*peri, True)
            if len(approx) == 4:
                break

    if len(approx) != 4:
        return None

    return np.array(approx, dtype="float32").reshape(4, 2)

