from PIL import Image
import pytesseract
import cv2
import sys
import numpy as np

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
        return ''
    for x in text:
        if x.isalpha():
            return x

    return { '|': 'I' }.get(x, x)


prev_board = np.array([
    ['f', 'g', '', '', '', '', '', '', '', '', '', '', '', 'u', 'r'],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', 's', 'i', 'd', '', '', '', '', '', '', 't', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', 'h', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', 'o', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', 'l', 't', 'h', '', '', '', '', '', '', 'c', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', 'o', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', 'z', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', 's', '', '', '', ''],
    ['', '', 'p', 'k', 'e', 'a', '', '', '', '', 'c', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['n', 'm', 'y', '', '', '', '', '', '', '', '', '', 'e', 'w', 'a']
])

def get_idx_to_check():
    check = {}

    for i in range(0, 15):
        for j in range(0, 15):

            if prev_board[i,j] == '' and i != 14 and j != 14:
                if prev_board[i+1,j] != '' or prev_board[i,j+1] != '' or prev_board[i-1,j] != '' or prev_board[i,j-1] != '':
                    key = str(i)+","+str(j)
                    check[key] = True

    print(check)
    return check


def matrix_match(matrix):
    check = get_idx_to_check()

    board_arr = np.empty((15,15), dtype=str)

    board_str = "\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"

    row = 0
    for i, img in enumerate(matrix):
        col = i%15

        if isinstance(img, int):
            board_str += ("|   ")
            board_arr[row, col] = ""
        else:

            idx = str(row)+","+str(col)


            if idx in check:
                # now check all around this word
                img = alter_image(img)
                filename = "Tiles/final/{}.png".format(i)
                cv2.imwrite(filename, img)
                char = tesseract_recognition(filename).lower()

                board_arr[row, col] = char
                board_str += ("| " + char + " ")
            else:
                char = prev_board[row, col]
                board_arr[row, col] = char
                board_str += ("| " + char + " ")

        if col == 14:
            row += 1
            board_str += "|\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"

    print(board_str)
    return board_arr
