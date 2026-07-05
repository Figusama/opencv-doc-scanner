from find_contour import find_contour
from pathlib import Path
import cv2 as cv
import numpy as np
from order import order_points
import os


def process(image_path: Path):
    img = cv.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not load image at {os.path.join(image_path)}")

    orig = img.copy()

    contour, ratio = find_contour(img)
    print("Contour:", contour)
    print("Ratio:", ratio)
    if contour is None:
        print("No contour found")
        return
    rect = order_points(contour) * ratio
    print("Contour after order_points:", rect)

    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

    width = int(max(widthA, widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

    height = int(max(heightA, heightB))

    dst = np.array([
        [0, 0],
        [width-1, 0],
        [width-1, height-1],
        [0, height-1]
    ], dtype="float32")

    M = cv.getPerspectiveTransform(rect, dst)
    warped = cv.warpPerspective(orig, M, (width, height))
    cv.imshow("warped", warped)
    cv.waitKey(0)