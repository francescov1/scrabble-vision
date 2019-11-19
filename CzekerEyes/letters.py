from matplotlib import pyplot as plt
# from capture import plot_test_images
# from capture import show_webcam
from PIL import Image
import pytesseract
import cv2
import os
import json
import re
import math
import numpy as np
import sys


def ich(x):
    return {
        '|': 'I'
#        'l': 'I',
#        '1': 'I',
#		'0': 'O'
    }.get(x, x)


def tesseract_recognition(i, img):

    gray = img

    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #tile_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    #gray = cv2.medianBlur(gray, 3)

    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    #gray = cv2.adaptiveThreshold(gray, 255,cv2.ADAPTIVE_THRESH_MEAN_C, \
    #                     cv2.THRESH_BINARY,11,2)
    #gray = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)[1]
                         #cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # Otsu's thresholding after Gaussian filtering
    #gray = cv2.GaussianBlur(gray,(5,5),0)
    #gray = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "Tiles/final/{}.png".format(i)
    #cv2.imwrite(filename, gray)
    cv2.imwrite(filename, gray)
    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
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


def template_match_json(imgTmp, imgFin):
    img = cv2.imread(imgTmp, 0)
    img2 = img.copy()
    template = cv2.imread(imgFin, 0)[25:148, 25:148]
    w, h = template.shape[::-1]

    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    # index = 1
    avg_top = [0, 0]
    avg_bottom = [0, 0]
    index = 1
    for meth in methods:

        img = img2.copy()
        method = eval(meth)

        res = cv2.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc

        bottom_right = (top_left[0] + w, top_left[1] + h)

        avg_top[0] += top_left[0] * avg_met(index)
        avg_top[1] += top_left[1] * avg_met(index)

        avg_bottom[0] += bottom_right[0] * avg_met(index)
        avg_bottom[1] += bottom_right[1] * avg_met(index)
        index += 1
        # cv2.rectangle(img, top_left, bottom_right, 0, 5)
        # plt.subplot(121), plt.imshow(template, cmap='gray')
        # plt.title('What detection'+ str(index)), plt.xticks([]), plt.yticks([])
        # plt.subplot(122), plt.imshow(img, cmap='gray')
        # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        # plt.suptitle(meth)
        # plt.show()
        # #plt.pause(10)
        # #plt.close()
        # index +=1

    avg_top[0] = math.ceil(avg_top[0] / 13)
    avg_top[1] = math.ceil(avg_top[1] / 13)
    avg_bottom[0] = math.ceil(avg_bottom[0] / 13)
    avg_bottom[1] = math.ceil(avg_bottom[1] / 13)

    tup_top = tuple(avg_top)
    tup_bottom = tuple(avg_bottom)
    cv2.rectangle(img, tup_top, tup_bottom, color=255, thickness=70, )
    plt.subplot(121), plt.imshow(template, cmap='gray')
    plt.title('What detection'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(img, cmap='gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)
    plt.show()
    return avg_top, avg_bottom


def switch(x):
    return {
        'aa': 'ą',
        'cc': 'ć',
        'ee': 'ę',
        'll': 'ł',
        'nn': 'ń',
        'oo': 'ó',
        'ss': 'ś',
        'zz': 'ź',
        'zzz': 'ż'
    }.get(x, x)


def avg_met(x):
    return {
        1: 1,
        2: 4,
        3: 4,
        4: 2,
        5: 2
    }.get(x, x)


def template_match(imgTmp, imgFin, ink):
    img = cv2.imread(imgTmp, 0)

    img2 = img.copy()
    template = cv2.cvtColor(imgFin, cv2.COLOR_BGR2GRAY)[25:148, 25:148]  # cv2.imread(imgFin, 0)
    # cv2.imwrite("test1.png",template)
    # template = template[:, :, 1]
    w, h = template.shape[::-1]

    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    index = 1
    avg_top = [0, 0]
    avg_bottom = [0, 0]
    fail = 0
    top_left_box = (1075, 855)
    bottom_right_box = (1860, 1950)
    top_box = (1390, 1790)
    for meth in methods:

        img = img2.copy()
        method = eval(meth)

        res = cv2.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc

        bottom_right = (top_left[0] + w, top_left[1] + h)

        if not (top_left_box[0] <= top_left[0] <= bottom_right_box[0]) or not (
                top_left_box[1] <= top_left[1] <= bottom_right_box[1]):
            fail += 1
        elif top_left[0] >= top_box[0] and top_left[1] >= top_box[1]:
            fail += 1

        if fail >= 2:
            avg_top = [1, 1]
            avg_bottom = [1, 1]
            break
        # print("top: ", top_left, "bottom: ", bottom_right)
        avg_top[0] += top_left[0] * avg_met(index)
        avg_top[1] += top_left[1] * avg_met(index)

        avg_bottom[0] += bottom_right[0] * avg_met(index)
        avg_bottom[1] += bottom_right[1] * avg_met(index)

        # cv2.rectangle(img, top_left, bottom_right, 255, 50)
        # plt.subplot(121), plt.imshow(template, cmap='gray')
        # plt.title('What detection'+ str(index)), plt.xticks([]), plt.yticks([])
        # plt.subplot(122), plt.imshow(img, cmap='gray')
        # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        # plt.suptitle(meth)
        # plt.show()
        # plt.pause(3)
        # plt.close()
        index += 1
    avg_top[0] = math.ceil(avg_top[0] / 13)
    avg_top[1] = math.ceil(avg_top[1] / 13)
    avg_bottom[0] = math.ceil(avg_bottom[0] / 13)
    avg_bottom[1] = math.ceil(avg_bottom[1] / 13)

    if not (top_left_box[0] <= top_left[0] <= bottom_right_box[0]) and not (
            top_left_box[1] <= top_left[1] <= bottom_right_box[1]):
        avg_top = [1, 1]
        avg_bottom = [1, 1]
    elif top_left[0] >= top_box[0] and top_left[1] >= top_box[1]:
        avg_top = [1, 1]
        avg_bottom = [1, 1]

    if fail < 2:
        ind_list = [30, 16]
        if ink in ind_list:
            index = 1
            for meth in methods:

                img = img2.copy()
                method = eval(meth)

                res = cv2.matchTemplate(img, template, method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

                if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                    top_left = min_loc
                else:
                    top_left = max_loc

                bottom_right = (top_left[0] + w, top_left[1] + h)

                cv2.rectangle(img, top_left, bottom_right, 255, 50)
                plt.subplot(121), plt.imshow(template, cmap='gray')
                plt.title('What detection' + str(index)), plt.xticks([]), plt.yticks([])
                plt.subplot(122), plt.imshow(img, cmap='gray')
                plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
                plt.suptitle(meth)
                plt.show()
                plt.pause(3)
                plt.close()
                index += 1
        tup_top = tuple(avg_top)
        tup_bottom = tuple(avg_bottom)
        cv2.rectangle(img, tup_top, tup_bottom, color=255, thickness=70, )
        plt.subplot(121), plt.imshow(template, cmap='gray')
        plt.title('What detection'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(img, cmap='gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)
        plt.show()
    # print(avg_top, avg_bottom)
    f = open("letters.json", 'r')
    letters_json = json.loads(f.read())
    for letter, cords in letters_json.items():
        # #print(cords, [avg_top, avg_bottom])
        if cords == [avg_top, avg_bottom]:
            # print(letter)
            return switch(letter)

        # else:
        # #print(letter, "NOPE")
    # print("Nope")
    return " "


def contures():
    img = cv2.imread('test_img/alfabet.jpg', 0)

    ret, thresh = cv2.threshold(img, 127, 255, 0)

    contours, hierarchy = cv2.findContours(thresh, 1, 2)

    cv2.drawContours(img, contours, -1, (255, 255, 255), 10)

    plt.imshow(img)
    plt.show()

    cnt = contours[0]

    M = cv2.moments(cnt)


def create_json():
    files = []
    folder = "test_img/letters/"
    refrence = "test_img/board_frame_00.png"
    regex = re.compile(r'/\w+\.')
    for file in os.listdir(folder):
        files.append(folder + file)
    letters_json = {}
    for file in files:
        match = re.search(regex, file)
        if match:
            name = match.group(0)[1:-1]
        # else:
        # print("FUCK")
        tmp = template_match_json(refrence, file)
        letters_json[name] = tmp
    x = json.dumps(letters_json)
    f = open("letters.json", 'w')
    f.write(x)


def matrix_match(matrix):
    #refrence = "test_img/board_frame_00.png"
    string = ""
    index = 1
    for i, img in enumerate(matrix):
        # print("index {}".format(index))
        if isinstance(img, int):
            string += " "
        else:
            string += tesseract_recognition(i, img)
            # string += template_match(refrence, img, index)
        index += 1
    return string.lower()


def main():
    # # #show_webcam(mirror=True)
    # files = []
    # folder = "test_img/letters_crop/"
    # refrence = "test_img/board_frame_00.png"
    # for file in os.listdir(folder):
    #     files.append(folder + file)
    #     # plot_test_images(folder + file)
    #     # tesseract_recognition(folder + file)
    #
    # test = ""
    # for file in files:
    #     test += template_match(refrence, file)
    # #print(test)
    create_json()


if __name__ == '__main__':
    main()
