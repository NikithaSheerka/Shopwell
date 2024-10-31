from imutils.object_detection import non_max_suppression
import numpy as np
import argparse
import time
import cv2
import tesserocr
from PIL import Image

import re
from fuzzywuzzy import fuzz

from os import path
import os
import matplotlib.pyplot as plt


# tessdata_path = path.abspath('./tessdata')
# tessdata_path = os.environ['TESSDATA_PREFIX']
# if(not tessdata_path ):
tessdata_path = path.abspath('./tessdata')
H = W = None
rW = rH = None
# Note: width and height should be multiple of 32


def load_and_resize(width, height,path=None,image=None):
    global W, H, rW, rH
    # load the input image and grab the image dimensions
    if path is None and image is None:
        return Exception("Either path or image should be provided")

    if path is not None and image is None:
        image = cv2.imread(path)

    orig = image.copy()
    (H, W) = image.shape[:2]
    # set the new width and height and then determine the ratio in change
    # for both the width and height
    (newW, newH) = (width, height)
    rW = W / float(newW)
    rH = H / float(newH)
    # print(W, H, rW, rH)
    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]
    
    return image, orig


# load the pre-trained EAST text detector
# print("[INFO] loading EAST text detector...")
# net = cv2.dnn.readNet('./models/frozen_east_text_detection.pb')


def detectTextsArea(image, orig, confidence):
    global W, H, rW, rH

    readTexts = []
    # define the two output layer names for the EAST detector model that
    # we are interested -- the first is the output probabilities and the
    # second can be used to derive the bounding box coordinates of text
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]

    # construct a blob from the image and then perform a forward pass of
    # the model to obtain the two output layer sets
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                                 (123.68, 116.78, 103.94), swapRB=True, crop=False)
    start = time.time()
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    end = time.time()

    # show timing information on text prediction
    print("[INFO] text detection took {:.6f} seconds".format(end - start))

    # grab the number of rows and columns from the scores volume, then
    # initialize our set of bounding box rectangles and corresponding
    # confidence scores
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    # loop over the number of rows
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the geometrical
        # data used to derive potential bounding box coordinates that
        # surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]

        # loop over the number of columns
        for x in range(0, numCols):
            # if our score does not have sufficient probability, ignore it
            if scoresData[x] < confidence:
                continue

            # compute the offset factor as our resulting feature maps will
            # be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)

            # extract the rotation angle for the prediction and then
            # compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # use the geometry volume to derive the width and height of
            # the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]

            # compute both the starting and ending (x, y)-coordinates for
            # the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            # add the bounding box coordinates and probability score to
            # our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])

    # apply non-maxima suppression to suppress weak, overlapping bounding
    # boxes
    boxes = non_max_suppression(np.array(rects), probs=confidences)
   
    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective
        # ratios
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)

        # print(startX, endX)
        # print(startY, endY)
        box_offset_neg = -15
        box_offset_pos = 15

        text = readText(orig[startY+box_offset_neg:endY+box_offset_pos,
                             startX+box_offset_neg:endX+box_offset_pos])
        readTexts.append(text.replace('\n',''))
        # draw the bounding box on the image
        cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)
       # print(text)
        cv2.putText(orig, text, (startX, startY-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
    
    return readTexts

def detectTexts(orig):
    # global W, H, rW, rH

    texts = []
    matched = []
    result = []
    text = readText(orig)

    texts = text.split('\n')
    print("texts : ", texts)
    keywords = findKeyword(texts)
    # print('KEYWORSDS:',keywords)
    validKeys = [i.lower() for i in dbTexts]
    visited = {}
    for key,value in keywords.items():
        newKey =  matchTextV2(key,dbTexts).lower().strip()
        newValues = matchText(value,dbTexts)
        print("newKey :: ", newKey, "newValues :: ", newValues)
        # if len(newValues[0])>=2 and newValues[0][-1] == '9':
        #     newValues[0] = newValues[0][:-2]
        #     newValues[1] = 'g'
        # print(nutriDetails[newKey])
        if not visited.get(newKey) and validKeys.count(newKey) and ['mg', 'ug', 'kg', 'g', ''].count(newValues[1].lower()):
            if len(newValues[0])>=2 and newValues[0][-1] == '9':
                newValues[0] = newValues[0][:-1]
                newValues[1] = 'g'
            visited[newKey] = True
            try:
                if('.' in newValues):
                    index = newValues.index('.')
            
                    if(index != 0 and index != -1):
                        newValues[index-1] = newValues[index-1]+'.'+newValues[index+1]
                        newValues.pop(index) 
                        newValues.pop(index)
                if(',' in newValues):
                    index = newValues.index(',')
                    if(index != 0 and index != -1):
                        newValues[index-1] = newValues[index-1]+'.'+newValues[index+1]
                        newValues.pop(index)
                        newValues.pop(index)
            except:
                pass
            try:
                nutriInfo = nutriDetails.get(newKey)
                limit = nutriInfo['limit'] if nutriInfo else 0
                descr = nutriInfo['descr'] if nutriInfo else ''
                keyval = dict(
                    type=newKey,
                    unit=newValues[1],
                    value=float(newValues[0]),
                    fullResult = newValues,
                    isDanger= False if float(newValues[0]) <= int(limit)  else True,
                    descr=descr
                )
                
                result.append(keyval)
            except:
                nutriInfo = nutriDetails.get(newKey)
                limit = nutriInfo['limit'] if nutriInfo else 0
                descr = nutriInfo['descr'] if nutriInfo else ''
                keyval = dict(
                    unit='',
                    type=newKey,
                    value=float(newValues[0]),
                    fullResult = newValues,
                    isDanger= False if float(newValues[0]) <= int(limit)  else True 
                )
                result.append(keyval)


        # keyval[newKey] = newValues

    # for line in texts:
    #     words = line.lower().replace('total ','').replace('total','').split(' ')
    #     print(words)
    #     result = matchText(words,dbTexts)
    #     matched.extend(result)
    #     keyval[result[0]] = ' '.join(result[1:])


    # print("Texts: ",texts)
    # print("Matched: ", matched)
    
    return result

def findKeyword(texts):
    # print ("Keywords",texts)
    keywords = {}
    pattern = re.compile(r'(\d+)')
    # pattern = re.compile(r'(\d+(\.\d{1,4})?)')
    for text in texts:
        # print("text : ", text)
        if(len(text)>2):
            patterns = re.split(pattern,text)
            print(patterns, type(patterns))
            if(len(patterns)>1):
                p = map(lambda x: x.strip(),patterns[1:])
                keywords[patterns[0]] = list(p)

    return keywords

def readText(roi):
    # cv2.imshow("Area", roi)
    # cv2.waitKey(0)
    img = Image.fromarray(roi)

    return tesserocr.image_to_text(img, path=tessdata_path)
def matchText(readTexts,dbTexts):
    '''
        Match the texts read by application to the keywords defined in database
        readTexts: list of texts that application read
        dbTexts: list of tags user set to track
    '''

    matchRatio = 40

    # print("Matching Texts")
    for i,text in enumerate(readTexts):
        maxRatio = 0
        maxj = 0
        # print(text)
        # print("TEXT:",text)
        newText = re.sub(r'^[0-9]+','',text,5)
        if(len(newText)==0): continue

        if(newText != text):
            continue
        # print(text)
        for j,tag in enumerate(dbTexts):
            ratio = fuzz.ratio(text,tag)
            # print(text,tag,ratio)
            if ratio > matchRatio and ratio > maxRatio:
                maxRatio = ratio
                maxj = j
        if(maxRatio > matchRatio):
            readTexts[i] = dbTexts[maxj]
    return readTexts

def matchTextV2(text,dbTexts):
    '''
        Match the texts read by application to the keywords defined in database
        text: text that application read
        dbTexts: list of tags user set to track
    '''
    # print('text : ', text,  'dbTexts :')
    matchRatio = 40

    # print("Matching Texts")

    maxRatio = 0
    maxj = 0
    # print(text)
    newText = re.sub(r'^[0-9]+','',text,5)

    if(len(newText)==0): return text
    if(newText != text):
        return text
    # print("KEYWORD TEXT:",text)
    for j,tag in enumerate(dbTexts):
        ratio = fuzz.ratio(text,tag)
        # print(text,tag,ratio)
        if ratio > matchRatio and ratio > maxRatio:
            maxRatio = ratio
            maxj = j
    if(maxRatio > matchRatio):
        text = dbTexts[maxj]
    if('ENERGY' in text):
        text = 'ENERGY'
    
    return text

dbTexts = [
            'Cholesterol',
            'Carbohydrate',
            'Calories',
            'Protein',
            'Fat',
            'Total Fat',
            'Energy',
            'Saturated Fat',
            'Trans Fat',
            'Carbs',
            'Sugar',
            'Total Sugars',
            'Potassium',
            'Sodium',
            'Sucrose',
            'Fucrose',
            'Ash',
            'KCal',
            'Iron',
            'Calcium',
            'Vitamin D',
            'Vitamin A',
            'Cholesterol / Cholestérol',
            # 'Protein/ Protéines',
            'g',
            'gm',
            'mg',
            'J',
            'KJ'
        ]

nutriDetails = {
        'cholesterol': {'limit': 300, 'descr': 'Cholesterol'},
        'carbohydrate':{ 'limit': 300, 'descr': 'Humans need calcium to build and maintain strong bones, and 99\% of the body\'s calcium is in the bones and teeth. It is also necessary for maintaining healthy communication between the brain and other parts of the body. It plays a role in muscle movement and cardiovascular function.'},
        'calories': {'limit': 2000, 'descr': 'Your body needs calories just to operate — to keep your heart beating and your lungs breathing. As a kid, your body also needs calories and nutrients from a variety of foods to grow and develop. And you burn off some calories without even thinking about it — by walking your dog or making your bed.'},
        'protein': {'limit': 20, 'descr': 'Protein is also a critical part of the processes that fuel your energy and carry oxygen throughout your body in your blood. It also helps make antibodies that fight off infections and illnesses and helps keep cells healthy and create new ones.'},
        'fat': {'limit': 10, 'descr': 'descr'},
        'total fat': {'limit': 20, 'descr': 'descr'},
        'energy': {'limit': 300, 'descr': 'descr'},
        'saturated fat': {'limit': 300, 'descr': 'descr'},
        'trans fat': {'limit': 300, 'descr': 'descr'},
        'carbs': {'limit': 300, 'descr': 'descr'},
        'sugar': {'limit': 35, 'descr': 'descr'},
        'total sugars': {'limit': 35, 'descr': 'descr'},
        'potassium': {'limit': 14, 'descr': 'descr'},
        'sodium': {'limit': 13, 'descr': 'descr'},
        'sucrose': {'limit': 20, 'descr': 'descr'},
        'fucrose': {'limit': 20, 'descr': 'descr'},
        'ash': {'limit': 20, 'descr': 'descr'},
        'kcal': {'limit': 20, 'descr': 'descr'},
        'iron': {'limit': 20, 'descr': 'descr'},
        'calcium': {'limit': 40, 'descr': 'Humans need calcium to build and maintain strong bones, and 99\% of the body\'s calcium is in the bones and teeth. It is also necessary for maintaining healthy communication between the brain and other parts of the body. It plays a role in muscle movement and cardiovascular function.'},
        'vitamin d': {'limit': 40, 'descr': 'descr'},
        'vitamin a': {'limit': 10, 'descr': 'descr'},
        # 'Protein/ Protéines': {'limit': 10, 'descr': 'Protein/ Protéines descr'},
        'Cholesterol / Cholestérol': {'limit': 10, 'descr': 'Cholesterol / Cholestérol descr'}
    }





if __name__ == "__main__":
    image, orig = load_and_resize(640,480,path='./images/threshold_cropped.jpg')

    

    # texts = detectTextsArea(image, orig, 0.4)
    texts = detectTexts(orig)
    # print(orig.shape)
    print("Final",texts)
    cv2.imshow("TextDetection", orig)
    cv2.imshow("Thresh ", image)


    cv2.waitKey(0)
   
    
