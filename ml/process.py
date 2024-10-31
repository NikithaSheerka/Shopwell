import os
import argparse
import csv
import cv2
import pytesseract
# from skimage import io
from PIL import Image, ImageEnhance
import numpy as np

# from crop import crop

def preprocess_for_ocr(img='/home/saicharan/Pictures/Recall@10.jpg', enhance=1):
    print("img : ", img)
    """
    @param img: image to which the pre-processing steps being applied
    """
    if enhance > 1:
        img = Image.fromarray(img)

        contrast = ImageEnhance.Contrast(img)

        img = contrast.enhance(enhance)

        img = np.asarray(img)

    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #img = cv2.GaussianBlur(img, (5,5), 0)

    #img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    return img

def ocr(img, oem=1, psm=3):
    """
    @param img: The image to be OCR'd
    @param oem: for specifying the type of Tesseract engine( default=1 for LSTM OCR Engine)
    """
    config = ('-l eng --oem {oem} --psm {psm}'.format(oem=oem,psm=psm))
    # config = ('-l eng --tessdata-dir "/usr/share/tesseract-ocr/tessdata" --oem {oem} -- psm {psm}'.format(oem=oem,psm=psm))

    try:
        img = Image.fromarray(img)
        text = pytesseract.image_to_string(img, config=config)

        return text
    except:

        return ""


if __name__ == '__main__':

    # ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--image", required=True, help="path to the input image")
    # args = vars(ap.parse_args())

    filename = 'name_truncated'
    # filename = "0044738018340_2"
    image = '/home/saicharan/Downloads/name_truncated.png'
    # print("@@@@@@@@@@@@@@ image : ", image)


    with open(os.path.join("/home/saicharan/Downloads/", "res_{}.txt".format(filename)), 'r') as f:
        c = csv.reader(f,delimiter=',')
        l = []
        for row in c:
            l.append(tuple(map(int, row)))
        coordinates_list = tuple(l)

    # coordinates_list = ((31, 952, 1853, 2241), (31, 1152, 1683, 2241), (39, 752, 1853, 2241))

    # for blob_cord in coordinates_list:
    #     cropped_image = crop(image, blob_cord, 'testing/ocr/cropped{}.jpg'.format(blob_cord[1]), 0.005)
    #     text = ocr(cropped_image)
    #     print(text)


