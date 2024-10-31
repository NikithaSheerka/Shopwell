from flask import Flask, request
import os


import json
import numpy as np
import imutils
import cv2
import preprocessing
import textDetection
from detect_table_class import NutritionTableDetector
from preprocessing import load_image,wrap_transform
from textDetection import load_and_resize, detectTexts,readText,matchText
import matplotlib.pyplot as plt

from crop import crop
from process import *

app = Flask(__name__)

tessdata_path = './tessdata'
# tessdata_path = './tessdata'

def load_model():
    """
    load trained weights for the model
    """
    global obj
    obj = NutritionTableDetector()
    print("Weights Loaded!")

def preprocesss_image(img_path):
    image = cv2.imread(img_path)
    # plt.imshow(image)
    # plt.show()
    boxes, scores, classes, num = obj.get_classification(image)
    # Get the dimensions of the image
    width = image.shape[1]
    height = image.shape[0]

    # print("Time taken to detect the table: %.5fs" % time_taken)

    # Select the bounding box with most confident output
    ymin = boxes[0][0][0] * height
    xmin = boxes[0][0][1] * width
    ymax = boxes[0][0][2] * height
    xmax = boxes[0][0][3] * width

    # print(xmin, ymin, xmax, ymax, scores[0][0])
    coords = (xmin, ymin, xmax, ymax)

    # Crop the image with the given bounding box
    cropped_image = crop(image, coords, "./output.jpg", 0, True)
    # plt.imshow(cropped_image)
    # plt.show()

    # Apply several filters to the image for better results in OCR
    cropped_image = preprocess_for_ocr(cropped_image, 3)

    # plt.imshow(cropped_image)
    # plt.show()
    return cropped_image


@app.route('/')
def index():
    return "Hello world!!!"

@app.route('/upload',methods=["POST"])
def upload_image():
    if request.method == "POST":
        print(request.files)
        f = request.files['image']
        path = './uploads/'+f.filename
        f.save(path)
        #Preprocessing tasks
        resized, original = load_image(path)
        load_model()
        resized =  preprocesss_image(path)
        if(resized is not None):
            T, warped = None, None#wrap_transform(resized, original)
 
            if T is not None:
                # plt.imshow(T)
                # plt.show()
                keyval = detectTexts(T)
                print(keyval)
                return dict(
                    status='success',
                    data=keyval,
                    msg='success',
                    code='200'
                )
            else:
                # plt.imshow(resized)
                # plt.show()
                keyval = detectTexts(resized)
                print(keyval)
                if(bool(keyval)):
                    return dict(
                        status='success',
                        data=keyval,
                        msg='success',
                        code='200'
                    )
                else:
                    return dict(
                        status='failed',
                        data=keyval,
                        msg='failed',
                        code='400'
                    )
            
        else:
            return dict(
                status='failed',
                msg="Image not found",
                code='400',
                data={}
            )
             