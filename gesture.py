import cv
import numpy as np
import math
import webbrowser as wb
import os

print("Enter full website for")

print("\n2 fingers")
fingers2 = input()

print("\n3 fingers")
fingers3 = input()

print("\n4 fingers")
fingers4 = input()

tabs = 0
count = 0
cap = cv.VideoCapture(0)

while (cap.isOpened()):
    ret, img = cap.read()
    cv.rectangle(img, (400, 400), (100, 100), (0, 255, 0), 0)
    crop_img = img[100:400, 100:400]
    grey = cv.cvtColor(crop_img, cv.COLOR_BGR2GRAY)
    value = (35, 35)
    blurred = cv.GaussianBlur(grey, value, 0)
    _, thresh1 = cv.threshold(blurred, 127, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)


    cv.imshow('Thresholded', thresh1)


    (version, _, _) = cv.__version__.split('.')

    if version == '3':
        image, contours, hierarchy = cv.findContours(thresh1.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    elif version == '2':
        contours, hierarchy = cv.findContours(thresh1.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)


    cnt = max(contours, key=lambda x: cv.contourArea(x))
    x, y, w, h = cv.boundingRect(cnt)
    cv.rectangle(crop_img, (x, y), (x + w, y + h), (0, 0, 255), 0)
    hull = cv.convexHull(cnt)


    drawing = np.zeros(crop_img.shape, np.uint8)
    cv.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
    cv.drawContours(drawing, [hull], 0, (0, 0, 255), 0)


    hull = cv.convexHull(cnt, returnPoints=False)


    defects = cv.convexityDefects(cnt, hull)
    count_defects = 0
    cv.drawContours(thresh1, contours, -1, (0, 255, 0), 3)
    for i in range(defects.shape[0]):