import time

import cv2
import numpy as np
from matplotlib import pyplot as plt
#import urllib.request
import urllib.request
from letters import matrix_match
import sys
import os

GOOD_MATCH_RATIO = 0.1


def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    img_counter = 0
    while True:
        ret_val, frame = cam.read()
        if mirror:
            img = cv2.flip(frame, 1)
        cv2.imshow('my webcam', frame)

        k = cv2.waitKey(10000)
        if k == 27:
            break  # esc to quit
        elif k == 32:
            # Spacebar pressed
            img_name = 'opencv_frame_{}.png'.format(img_counter)
            cv2.imwrite(img_name, frame)
            # print("{} written!".format(img_name))
            img_counter += 1

    cv2.destroyAllWindows()


def plot_test_images(img):
    alphabet = cv2.imread(img)

    alphabetBlur = cv2.cvtColor(alphabet, cv2.COLOR_RGB2GRAY)
    alphabetBlur = cv2.medianBlur(alphabetBlur, 15)

    th1 = cv2.adaptiveThreshold(alphabetBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 11)
    th1 = cv2.bitwise_not(th1)

    kernel = np.ones((5, 5), np.uint8)
    dilation1 = cv2.dilate(th1, kernel, iterations=1)
    closing1 = cv2.morphologyEx(dilation1, cv2.MORPH_CLOSE, kernel)
    edges1 = cv2.Canny(alphabetBlur, 180, 220)

    titles = ['Alphabet', 'Alphabet threshold', 'Alphabet after dilation and closing', 'Alphabet edges']
    images = [alphabet, th1, closing1, edges1]

    plt.figure(dpi=300)
    for i in range(4):
        plt.subplot(2, 2, i + 1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    plt.show()

    cv2.waitKey()
    cv2.destroyAllWindows()
    return images


def board_detection_ORB(testImg):
    refImg = cv2.imread('test_img/reference2.jpg', 0)
    #cv2.imshow('reference', refImg)

    orb = cv2.ORB_create(500)
    testImg = cv2.resize(testImg, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_AREA)
    refImg = cv2.resize(refImg, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_AREA)

    kp = orb.detect(refImg, None)
    kp1, des1 = orb.detectAndCompute(refImg, None)
    kp2, des2 = orb.detectAndCompute(testImg, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)

    # for m in matches:
    # print(m.distance)

    plt.figure(dpi=500)
    result = np.zeros((1000, 1000, 3), np.uint8)
    result = cv2.drawMatches(refImg, kp1, testImg, kp2, matches[:int(len(matches) * 0.5)], result)

    plt.imshow(result), plt.show()


def board_detection_BRISK(testImg):
   # print('Detecting board...')
    start = time.time()

    # Load and resize images
    refImg = cv2.imread('test_img/reference4.png', 0)
    colorTestImg = cv2.cvtColor(testImg, cv2.COLOR_RGB2BGR)
    testImg = cv2.cvtColor(testImg, cv2.COLOR_RGB2GRAY)

    if (testImg.size > 307200):
        testImg = cv2.resize(testImg, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        #testImgLowRes = cv2.resize(testImg, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
        testImgBlur = cv2.blur(testImg, (5, 5))
        colorTestImg = cv2.resize(colorTestImg, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    if (refImg.size > 300000):
        refImg = cv2.resize(refImg, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        #refImgLowRes = cv2.resize(refImg, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
        refImgBlur = cv2.blur(refImg, (5, 5))

    # Create BRISK, detect keypoints and descriptions
    brisk = cv2.BRISK_create(40)
    kp1, des1 = brisk.detectAndCompute(refImgBlur, None)
    kp2, des2 = brisk.detectAndCompute(testImgBlur, None)

    # Create BFMatcher and knnMatch descriptions
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Filter for only close enough matches
    good = []
    for m, n in matches:
        if m.distance < 0.65 * n.distance:
            good.append(m)

    # If there is enough matches warp the board, draw grid, find tiles and plot results
    if len(good) > 10:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()

        h, w = refImg.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)

        pts2 = np.float32([[0, 0], [w - 1, 0], [0, h - 1], [w - 1, h - 1]]).reshape(-1, 1, 2)
        dst2 = cv2.perspectiveTransform(pts2, M)

        img2 = cv2.polylines(testImg, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

        draw_params = dict(matchColor=(0, 255, 0),
                           singlePointColor=None,
                           matchesMask=matchesMask,
                           flags=2)

        board_size = np.float32([[0, 0], [3000, 0], [0, 3000], [3000, 3000]])
        matrix = cv2.getPerspectiveTransform(dst2, board_size)

        warpped_board = cv2.warpPerspective(colorTestImg, matrix, (3000, 3000))
        print(matrix_match(detect_tiles(warpped_board)))
        #sys.stdout.flush()

        #detect_tiles(warpped_board)
        warpped_board = draw_grid(warpped_board)
        warpped_board = cv2.cvtColor(warpped_board, cv2.COLOR_RGB2BGR)

        #cv2.imshow('warpped', warpped_board)
        #cv2.waitKey()

        img3 = cv2.drawMatches(refImg, kp1, img2, kp2, good, None, **draw_params)

        print('finished!')
        print('total time: ', time.time() - start)

        plt.figure(dpi=450)
        plt.subplot(2,1,1), plt.imshow(warpped_board, 'gray'), plt.title('warpped board'), plt.axis('off')
        plt.subplot(2,1,2), plt.imshow(img3, 'gray'), plt.title('matching'), plt.axis('off')
        plt.show()
    else:
        # print('Not enough matches found!')
        matchesMask = None

    # Plot results
    plt.figure(dpi=450)
    result = np.zeros((1000,1000,3), np.uint8)
    result = cv2.drawMatchesKnn(refImg, kp1, testImg, kp2, good, result)
    plt.imshow(result), plt.show()

vertical_start = 207
horizontal_start = 180

def draw_grid(refImg):
    # print('Drawing grid...')
    refImg = cv2.cvtColor(refImg, cv2.COLOR_RGB2BGR)
    h, w, r = refImg.shape
    print(h, w, r)

    width = ((w - 190) / 16 - 1)
    height = ((h - 645) / 16 - 1)

    for i in range(0, 16):
        widthDist = int(width * i)
        heightDist = int(height * i)
        # #print('widthDist', widthDist, 'heightDist', heightDist)

        cv2.line(refImg, (vertical_start + widthDist, horizontal_start), (vertical_start + widthDist, h - 613), (0, 255, 0), 8, 1)
        # horizontal

        cv2.line(refImg, (vertical_start, horizontal_start + heightDist), (w - 159, horizontal_start + heightDist), (0, 255, 0), 8, 1)

    # for i in range(0, 15):
    #     widthDist = int((w - 230) / 15 * i)
    #     heightDist = int((h - 230) / 15 * i)
    #     # #print('widthDist', widthDist, 'heightDist', heightDist)

    #     # vertical
    #     cv2.line(refImg, (210 + widthDist, 140), (210 + widthDist, h - 270), (0, 255, 0), 8, 1)
    #     # horizontal
    #     cv2.line(refImg, (210, 140 + heightDist), (w - 195, 140 + heightDist), (0, 255, 0), 8, 1)
    cv2.imwrite("GridDrawnImage.png",refImg)
    return refImg

letter_indicies = [
    [0,0],
    [0,1],
    [0,13],
    [0,14],
    [2,2],
    [2,3],
    [2,4],
    [2,11],
    [3,11],
    [4,11],
    [7,1],
    [7,2],
    [7,3],
    [7,10],
    [8,7],
    [8,8],
    [8,9],
    [8,10],
    [8,11],
    [9,10],
    [10,10],
    [11,2],
    [11,3],
    [11,4],
    [11,5],
    [11,10],
    [14,0],
    [14,1],
    [14,2],
    [14,12],
    [14,13],
    [14,14]
]

def detect_tiles(refImg):
    # print('Detecting tiles...')
    refImg = cv2.cvtColor(refImg, cv2.COLOR_RGB2BGR)

    tiles = []
    tile_indicies = []
    h, w, r = refImg.shape
    print(h,w,r)

    width = int((w - 190) / 16 * 1)
    height = int((h - 645) / 16 * 1)

    start = [vertical_start, horizontal_start]

    print(width, height, start)

    os.remove("wynik.txt")
    f = open('wynik.txt', "w+")

    min_letter_black = 5000
    min_letter = []
    max_non_letter_black = 0
    max_non_letter = []

    for i in range(0, 15):
        for j in range(0, 15):
            tile = refImg[start[1] + height * i: start[1] + height * (i + 1),
                   start[0] + width * j: start[0] + width * (j + 1)]
            lower_black_RGB = np.array([0,0,0])
            upper_black_RGB = np.array([30,30,30])

            shapeMask = cv2.inRange(tile, lower_black_RGB, upper_black_RGB)
            #cv2.imwrite("SavedTiles/TileBlackMaskedRBG" + str(i) + str(j) + ".png",shapeMask)

            ## TODO: try doing bgr mask then converting to hsv

            tile_HSV = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)
            #_, tile_HSV_frame = tile_HSV
            #cv2.imwrite("SavedTiles/TileHSV" + str(i) + str(j) + ".png",tile_HSV)
            lower_black_HSV = np.array([0,0,0])
            upper_black_HSV = np.array([180,255,35])
            shapeMask_HSV = cv2.inRange(tile_HSV, lower_black_HSV, upper_black_HSV)
            tiles.append(tile)
            #shapeMask_HSV = cv2.inRange(tile_HSV_frame, lower_black_HSV, upper_black_HSV)
            #shapeMask_RGB = cv2.cvtColor(shapeMask_HSV, cv2.COLOR_HSV2BGR)
            #shapeMask_HSV = cv2.cvtColor(shapeMask_RGB, cv2.COLOR_BGR2HSV)

            maskHeightHSV = shapeMask_HSV.shape[0]
            maskWidthHSV = shapeMask_HSV.shape[1]

            black_pixels = 0
            white_pixels = 0
            for x in range(maskHeightHSV):
                for y in range(maskWidthHSV):
                    color = shapeMask_HSV[x,y]
                    if (color == 0):
                        shapeMask_HSV[x,y] = 255
                        # since inverted, this is white now
                        white_pixels += 1
                    elif (color == 255):
                        shapeMask_HSV[x,y] = 0
                        # since inverted, this is black now
                        black_pixels += 1
                    else:
                        print("Should not get here")

            idx = [i,j]

            # skip center star for now as it causes issues (7,7)
            if idx != [7,7]:
                if idx in letter_indicies:
                    if black_pixels < min_letter_black:
                        min_letter_black = black_pixels
                        min_letter = idx
                else:
                    if black_pixels > max_non_letter_black:
                        max_non_letter_black = black_pixels
                        max_non_letter = idx


            f.write("[" + str(i)+ "," + str(j) + "]: ")
            f.write('black(' + str(black_pixels) + ')\n')

            cv2.imwrite("SavedTiles/TileBlackMaskedHSV," + str(i) + "," + str(j) + ".png",shapeMask_HSV)

            # skip center star for now as it causes issues (7,7)
            if (black_pixels > 1000 and idx != [7,7]):
                tiles.append(tile)
                tile_indicies.append(idx)
            else:
                tiles.append(0)

    f.close()
    print("Max non letter black: " + str(max_non_letter) + ", black: " + str(max_non_letter_black))
    print("Min letter black: " + str(min_letter) + ", black: " + str(min_letter_black))
    print("Tiles with letters inside:")
    print(tile_indicies)
    return tiles


def show_ip_webcam():
    #url = "/cygdrive/c/Users/Murtadha/Documents/GitHub/scrabble-vision/CzekerEyes/test_img/IMG_0990.png"
    #photoUrl = "/cygdrive/c/Users/Murtadha/Documents/GitHub/scrabble-vision/CzekerEyes/test_img/IMG_0990.png"
    img_counter = 0
    #while True:
    #frameRaw = urllib.request.urlopen('file://test_img/IMG_0990.png')
    with open("test_img/IMG_0990.png", "r+b") as image:
        frameRaw = image.read()
        #frame = np.array(bytearray(frameRaw), dtype=np.uint8)
    frame = np.array(bytearray(frameRaw), dtype=np.uint8)
    frame = cv2.imdecode(frame, -1)
        # frameResized = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    #cv2.imshow('frame', frame)
    #k = cv2.waitKey(1)
        #if k == 27:
        #    break  # esc to quit
        # elif k == 32:
        #     # Spacebar pressed
        #     img_name = 'board_frame_{}.png'.format(img_counter)
        #     cv2.imwrite(img_name, frame)
        #     #print("{} written!".format(img_name))
        #     img_counter += 1
    #elif k == 32:
            # Spacebar pressed
            #frameRaw = urllib.request.urlopen(photoUrl)
        #with open("test_img/IMG_0990.png", "rb") as image:
            #frameRaw = image.read()
            #frame = np.array(bytearray(frameRaw), dtype=np.uint8)
            #frame = np.array(bytearray(frameRaw))
            #frame = cv2.imdecode(frame, -1)
            # frame = cv2.resize(frame, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_AREA)
    img_name = 'board_frame_{}.png'.format(img_counter)
    cv2.imwrite(img_name, frame)
            # print("{} written!".format(img_name))
    img_counter += 1

    board_detection_BRISK(frame)
            #print("get photo")

def main():
    # testImg = cv2.imread('test_img/one_place.jpg', 0)
    testImg = cv2.imread('test_img/board_frame_11.png', 1)

    board_detection_BRISK(testImg)

    # show_ip_webcam()


if __name__ == '__main__':
    main()
