import cv2 as cv
import numpy as np
from order import order_points


def match_points_generation(img):
    points = []
    clone = img.copy()

    def draw_points(event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN and len(points) < 4:
            points.append([x, y])

            cv.circle(clone, (x, y), 8, (0, 255, 0), -1)

            cv.putText(clone, str(len(points)), (x+12, y), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            if len(points) > 1:
                cv.line(clone, tuple(points[-2]), tuple(points[-1]), (0, 255, 0 ), 1)
            
            cv.imshow("Click 4 corners - press R to reset", clone)

            if len(points) == 4:
                cv.line(clone, tuple(points[-1]), tuple(points[0]), (0, 255, 0), 1)
                cv.imshow("Click 4 corners - press R to reset", clone)

    cv.imshow("Click 4 corners - press R to reset", clone)

    cv.setMouseCallback("Click 4 corners - press R to reset", draw_points)

    while True:

        key = cv.waitKey(1) 

        if key == ord("r"):
            points.clear()
            clone = img.copy()
            cv.putText(clone, "Reset - click 4 corners",
                       (10, 30), cv.FONT_HERSHEY_SIMPLEX,
                       0.7, (0, 0, 255), 2)
            cv.imshow("Click 4 corners - press R to reset", clone)

        elif len(points) == 4:
            cv.waitKey(500)
            break
    try:
        cv.destroyAllWindows("Clock 4 corners - press R to reset")
    except:
        pass
    
    corners = np.array(points, dtype="float32").reshape(4, 2)

    return order_points(corners)