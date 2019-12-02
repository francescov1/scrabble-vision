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
    if sys.platform == 'darwin' or sys.platform == 'linux':
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

def get_idx_to_check(prev_board):
    check = {}

    for i in range(0, 15):
        for j in range(0, 15):

            if prev_board[i,j] == '' and i != 14 and j != 14:
                if prev_board[i+1,j] != '' or prev_board[i,j+1] != '' or prev_board[i-1,j] != '' or prev_board[i,j-1] != '':
                    key = str(i)+","+str(j)
                    check[key] = True
    return check

def get_char(matrix, i, j):
    if i >= 0 and i <= 14 and j >= 0 and j <= 14:
        img = matrix[i][j]
        if isinstance(img, int):
            char = ''
        else:
            char = detect_tile(img)

        if char != '':
            return char

    return None

# last thing to do is stop if we have found letters then no more
def check_right(prev_board, board_arr, matrix, i, j):
    if j > 14:
        return board_arr

    for idx in range(j, 15):
        if prev_board[i,idx] == '':

            char = get_char(matrix, i, idx)
            if char != None:
                print('found right char ' + char)
                board_arr[i,idx] = char
            else:
                break
        else:
            continue

    return board_arr

def check_left(prev_board, board_arr, matrix, i, j):
    if j < 0:
        return board_arr

    for idx in range(j, -1, -1):
        if prev_board[i,idx] == '':

            char = get_char(matrix, i, idx)
            if char != None:
                print('found left char ' + char + " at " + str(i) + "," + str(idx))

                board_arr[i,idx] = char
            else:
                break
        else:
            continue

    return board_arr


def check_down(prev_board, board_arr, matrix, i, j):
    if i < 0:
        return board_arr

    for idx in range(i, -1, -1):
        if prev_board[idx,j] == '':

            char = get_char(matrix, idx, j)
            if char != None:
                print('found down char ' + char + " at " + str(idx) + "," + str(j))

                board_arr[idx,j] = char
            else:
                break
        else:
            continue

    return board_arr

def check_up(prev_board, board_arr, matrix, i, j):
    if i > 14:
        return board_arr

    for idx in range(i, 15):
        if prev_board[idx,j] == '':

            char = get_char(matrix, idx, j)
            if char != None:
                print('found up char ' + char + " at " + str(idx) + "," + str(j))

                board_arr[idx,j] = char
            else:
                break
        else:
            continue

    return board_arr

def detect_tile(img):
    img = alter_image(img)
    filename = "Tiles/final/temp.png"
    cv2.imwrite(filename, img)
    char = tesseract_recognition(filename).lower()
    return char

def matrix_match(matrix, prev_board):
    if prev_board is None:
        print('Detecting for the first time')
        board_arr = first_match(matrix)
    else:
        print('Using previous board to speed up detection')
        board_arr = match_from_prev(matrix, prev_board)

    print_board(board_arr)
    return board_arr

def first_match(matrix):
    board_arr = np.empty((15,15), dtype=str)

    for i in range(0, 15):
        for j in range(0, 15):
            img = matrix[i][j]

            if isinstance(img, int):
                board_arr[i, j] = ''
            else:
                board_arr[i, j] = detect_tile(img)
    return board_arr

def match_from_prev(matrix, prev_board):
    check = get_idx_to_check(prev_board)
    board_arr = np.copy(prev_board)

    for i in range(0, 15):
        for j in range(0, 15):
            img = matrix[i][j]

            if isinstance(img, int):
                board_arr[i, j] = ""
            else:

                idx = str(i)+","+str(j)

                if idx in check:
                    char = detect_tile(img)
                    board_arr[i, j] = char

                    # at this point, we have found the first new tile
                    # (on the edge of previous tiles). Need to now figure out what
                    # direction the word is going and then follow it until it finishes

                    board_arr = check_right(prev_board, board_arr, matrix, i, j+1)
                    board_arr = check_left(prev_board, board_arr, matrix, i, j-1)
                    board_arr = check_up(prev_board, board_arr, matrix, i+1, j)
                    board_arr = check_down(prev_board, board_arr, matrix, i-1, j)
                    return board_arr
                else:
                    char = prev_board[i, j]
                    board_arr[i, j] = char

    return board_arr

def print_board(board_arr):
    board_str = "\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
    for i in range(0, 15):
        for j in range(0, 15):
            char = board_arr[i,j]
            if char == "":
                board_str += ("|   ")
            else:
                board_str += ("| " + char + " ")
            if j == 14:
                board_str += "|\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
    print(board_str)
