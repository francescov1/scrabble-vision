import time

import cv2
import numpy as np
from matplotlib import pyplot as plt
#import urllib.request
import urllib.request
from letters import matrix_match
import sys

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
        sys.stdout.flush()

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


def draw_grid(refImg):
    # print('Drawing grid...')
    refImg = cv2.cvtColor(refImg, cv2.COLOR_RGB2BGR)
    h, w, r = refImg.shape
    print(h, w, r)

    for i in range(0, 16):
        widthDist = int((w - 190) / 16 * i)
        heightDist = int((h - 645) / 16 * i)
        # #print('widthDist', widthDist, 'heightDist', heightDist)

        # vertical
        cv2.line(refImg, (190 + widthDist, 180), (190 + widthDist, h - 645), (0, 255, 0), 8, 1)
        # horizontal
        cv2.line(refImg, (190, 180 + heightDist), (w - 195, 180 + heightDist), (0, 255, 0), 8, 1)

    # for i in range(0, 15):
    #     widthDist = int((w - 230) / 15 * i)
    #     heightDist = int((h - 230) / 15 * i)
    #     # #print('widthDist', widthDist, 'heightDist', heightDist)

    #     # vertical
    #     cv2.line(refImg, (210 + widthDist, 140), (210 + widthDist, h - 270), (0, 255, 0), 8, 1)
    #     # horizontal
    #     cv2.line(refImg, (210, 140 + heightDist), (w - 195, 140 + heightDist), (0, 255, 0), 8, 1)

    return refImg


def detect_tiles(refImg):
    # print('Detecting tiles...')
    refImg = cv2.cvtColor(refImg, cv2.COLOR_RGB2BGR)
    tiles = []
    h, w, r = refImg.shape
    print(h,w,r)

    width = (190 + int((w - 190) / 16 * 1)) - (190 + int((w - 190) / 16 * 0))
    height = (180 + int((h - 645) / 16 * 1)) - (180 + int((h - 645) / 16 * 0))
    start = [(190 + int((w - 190) / 16 * 0)), (180 + int((h - 645) / 16 * 0))]

    print(width, height, start)
	
    f = open('wynik.txt', "w+")

    for i in range(0, 15):
        for j in range(0, 15):
            tile = refImg[start[1] + height * i: start[1] + height * (i + 1),
                   start[0] + width * j: start[0] + width * (j + 1)]

            tile_HSV = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)

            h, s, v = tile_HSV.T

            # result = abs(result)
            # #print('hist correl',  result)
            #print(np.average(s))
            f.write(str(i)+" ")
            f.write(str(j)+" ")
            f.write(str(np.median(s))+"\n")
            f.write(str(np.average(s))+"\n")
            if (np.median(s) < 40):
                tiles.append(tile)
            else:
                tiles.append(0)
            # tiles.append(tile)

    # for i in range(0, tiles.__len__()):
    #     cv2.imshow('{}'.format(i), tiles[i])
    #     cv2.waitKey()
    f.close()
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
