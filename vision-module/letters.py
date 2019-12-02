from PIL import Image
import pytesseract
import cv2
import sys

def alter_image(img):

    img = cv2.bilateralFilter(img, 9, 75, 75)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    return img

def tesseract_recognition(filename):

    if sys.platform == 'darwin':
        pytesseract.pytesseract.tesseract_cmd = "tesseract"
    else:
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    text = pytesseract.image_to_string(Image.open(filename), config="-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ| --psm 10 ")

    if not text:
        return " "
    for x in text:
        if x.isalpha():
            return x

    return { '|': 'I' }.get(x, x)


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
    string = ""
    for i, img in enumerate(matrix):
        if isinstance(img, int):
            string += " "
        else:

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
