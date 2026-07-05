import cv2 as cv
import numpy as np

# highest sum is the bottom-right
#lowest sum is the top-left
def order_points(pts):
    pts = np.array(pts, dtype="float32").reshape(4, 2)

    # find centroid
    center = pts.mean(axis=0)

    # compute angle of each point relative to centroid
    angles = np.arctan2(pts[:, 1] - center[1], pts[:, 0] - center[0])

    # sort by angle
    sorted_idx = np.argsort(angles)
    sorted_pts = pts[sorted_idx]

    # sorted_pts now goes clockwise or counterclockwise from the "rightmost" point
    # rotate so top-left comes first
    # top-left = point with smallest sum of coordinates
    sums = sorted_pts.sum(axis=1)
    tl_idx = np.argmin(sums)

    # reorder starting from top-left, going clockwise
    ordered = np.roll(sorted_pts, -tl_idx, axis=0)

    return ordered.astype("float32")
