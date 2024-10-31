import os
import cv2
import numpy as np
import imutils
from helpers.transform import four_point_transform
import matplotlib.pyplot as plt
from pytesseract import Output
import pytesseract
import argparse

ratio = None
R_H = 600

def correct_orientation(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pytesseract.image_to_osd(rgb, output_type=Output.DICT)
    # display the orientation information
    print("[INFO] detected orientation: {}".format(
        results["orientation"]))
    print("[INFO] rotate by {} degrees to correct".format(
        results["rotate"]))
    print("[INFO] detected script: {}".format(results["script"]))
    rotated = imutils.rotate_bound(image, angle=results["rotate"])
    # show the original image and output image after orientation
    # correction
    cv2.imshow("Original", image)
    cv2.imshow("rotated", rotated)
    cv2.waitKey(0)
    return rotated
    return {}

def load_image(imgPath):
    if not os.path.exists(imgPath):
        return None, None
    global ratio
    image = cv2.imread(imgPath)
    # correct_orientation(image)
    ratio = image.shape[0]/R_H
    orig = image.copy()
    image = imutils.resize(image, height=R_H)
    # cv2.imshow("re-sized", image)
    return image, orig


def wrap_transform(image, orig):
    return image, orig
    global ratio
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 1)
    gray = cv2.equalizeHist(gray)
    bigrayl = cv2.bilateralFilter(gray,7,20,20)
    edged = cv2.Canny(gray, 75, 200)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:3]
    screenCnt = None
    for i, c in enumerate(cnts):
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break
    if screenCnt is not None:
        warped = four_point_transform(orig, screenCnt.reshape(4, 2)*ratio)
        warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        T = cv2.adaptiveThreshold(
            warped, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, 9)
        return T, warped
    else:
        return None, None



if __name__ == "__main__":
    resized, original = load_image(
        './images/labels_2_cropped.jpg')

    if(resized is not None):
        T, warped = wrap_transform(resized, original)

        if T is not None:
            cv2.imwrite('./images/threshold_cropped.jpg', T)
            cv2.imwrite('./images/WARPED_cropped.jpg',  imutils.resize(warped, height=R_H))
            cv2.imshow("Threshold", imutils.resize(T, height=R_H))
            cv2.imshow("Warped", imutils.resize(warped, height=R_H))
            cv2.waitKey(0)
        else:
            print("T is none")
    else:
        print("Image doesnot exist")
