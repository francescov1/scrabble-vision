from matplotlib import pyplot as plt
from PIL import Image
import pytesseract
import cv2
import os
import json
import re
import math
import numpy as np
import sys

def alter_image(img):
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #tile_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    img = cv2.bilateralFilter(img, 9, 75, 75)
    #gray = cv2.medianBlur(gray, 3)

    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    #gray = cv2.adaptiveThreshold(gray, 255,cv2.ADAPTIVE_THRESH_MEAN_C, \
    #                     cv2.THRESH_BINARY,11,2)
    #gray = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)[1]
                         #cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # Otsu's thresholding after Gaussian filtering
    #gray = cv2.GaussianBlur(gray,(5,5),0)
    #gray = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    return img

def tesseract_recognition(filename):

    if sys.platform == 'darwin':
        pytesseract.pytesseract.tesseract_cmd = "tesseract"
    else:
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    text = pytesseract.image_to_string(Image.open(filename), config="-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ| --psm 10 ")

    #print(text)
    #os.remove(filename)
    # #print("lol")
    #print(text)

    # show the output images
    #cv2.imshow("Image", img)
    #cv2.imshow("Output", gray)
    #cv2.waitKey(0)
    if not text:
        return " "
    for x in text:
        if x.isalpha():
            return ich(x)
    return ich(text[0])

def ich(x):
    return {
        '|': 'I',
    }.get(x, x)

'''
[['f', 'g', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'u', 'r']
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
 [' ', ' ', 's', 'i', 'd', ' ', ' ', ' ', ' ', ' ', ' ', 't', ' ', ' ', ' ']
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'h', ' ', ' ', ' ']
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ']
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
 [' ', 'l', 't', 'h', ' ', ' ', ' ', ' ', ' ', ' ', 'c', ' ', ' ', ' ', ' ']
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ']
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'z', ' ', ' ', ' ', ' ']
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 's', ' ', ' ', ' ', ' ']
 [' ', ' ', 'p', 'k', 'e', 'a', ' ', ' ', ' ', ' ', 'c', ' ', ' ', ' ', ' ']
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
 ['n', 'm', 'y', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'e', 'w', 'a']]
'''

def matrix_match(matrix):
    #refrence = "test_img/board_frame_00.png"
    string = ""
    for i, img in enumerate(matrix):
        if isinstance(img, int):
            string += " "
        else:
            cv2.imwrite("Tiles/pre_alter/{}.png".format(i), img)

            img = alter_image(img)

            filename = "Tiles/final/{}.png".format(i)
            cv2.imwrite(filename, img)

            string += tesseract_recognition(filename)
    return string.lower()

def sort_tiles(name):
    i = name.split('.')[0]
    if i.isdigit():
        return int(i)
    else:
        return -1

# stage = pre_alter or final
def match_from_last(stage):
    i = 0;
    string = ""
    for root, subdirs, files in os.walk("Tiles/" + stage):
            files.sort(key=sort_tiles)

            for filename in files:
                if not filename.endswith(".png"):
                    continue

                while int(filename.split('.png')[0]) != i:
                    string += " "
                    i += 1

                    # if weve gone over whole board
                    if i == 225:
                        return string.lower()

                path = os.path.join(root, filename)

                if stage == "pre_alter":
                    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
                    img = alter_image(img)

                    path = "Tiles/final/{}.png".format(i)
                    cv2.imwrite(path, img)

                string += tesseract_recognition(path)
                i += 1

            break

    return string.lower()
