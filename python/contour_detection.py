import cv2 as cv

def contour_detection(img, edged):

    contours, _ = cv.findContours(edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv.contourArea, reverse=True)
    img_area = img.shape[0] * img.shape[1]
    doc_contour = None
    for c in contours:
        area = cv.contourArea(c)
        if area > 0.90 * img_area:
            continue
        peri = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            doc_contour = approx
            break

    return doc_contour
