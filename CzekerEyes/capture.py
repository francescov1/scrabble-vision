import time
import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt
from letters import matrix_match, match_from_last

BOARD_SIZE = np.float32([[0, 0], [3000, 0], [0, 3000], [3000, 3000]])

def board_detection_BRISK(testImg):
    start = time.time()

    # Load and resize images
    refImg = cv2.imread('test_img/reference4.png', 0)
    colorTestImg = cv2.cvtColor(testImg, cv2.COLOR_RGB2BGR)
    testImg = cv2.cvtColor(testImg, cv2.COLOR_RGB2GRAY)

    if (testImg.size > 307200):
        testImg = cv2.resize(testImg, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        testImgBlur = cv2.blur(testImg, (5, 5))
        colorTestImg = cv2.resize(colorTestImg, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    if (refImg.size > 300000):
        refImg = cv2.resize(refImg, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
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


        matrix = cv2.getPerspectiveTransform(dst2, BOARD_SIZE)

        warpped_board = cv2.warpPerspective(colorTestImg, matrix, (3000, 3000))

        if len(sys.argv) > 1:
            if sys.argv[1] == "final":
                print("Using final tiles from previous run")
                print(match_from_last("final"))
            if sys.argv[1] == "pre":
                print("Using pre altered tiles from previous run")
                print(match_from_last("pre_alter"))

            print('finished!')
            print('total time: ', time.time() - start)
        else:
            tiles = detect_tiles(warpped_board)
            print(matrix_match(tiles))

            grid_board = draw_grid(warpped_board)

            # at this point grid_board is saved

            grid_board = cv2.cvtColor(grid_board, cv2.COLOR_RGB2BGR)

            img3 = cv2.drawMatches(refImg, kp1, img2, kp2, good, None, **draw_params)

            print('finished!')
            print('total time: ', time.time() - start)

            plt.figure(dpi=450)
            plt.subplot(2,1,1), plt.imshow(grid_board, 'gray'), plt.title('warpped board'), plt.axis('off')
            plt.subplot(2,1,2), plt.imshow(img3, 'gray'), plt.title('matching'), plt.axis('off')
            plt.show()

            # Plot results
            plt.figure(dpi=450)
            result = np.zeros((1000,1000,3), np.uint8)
            result = cv2.drawMatchesKnn(refImg, kp1, testImg, kp2, good, result)
            plt.imshow(result), plt.show()

    else:
        # print('Not enough matches found!')
        matchesMask = None

vertical_start = 207
horizontal_start = 180

def draw_grid(refImg):
    refImg = cv2.cvtColor(refImg, cv2.COLOR_RGB2BGR)
    h, w, r = refImg.shape
    print(h, w, r)

    width = ((w - 190) / 16 - 1)
    height = ((h - 645) / 16 - 1)

    for i in range(0, 16):
        widthDist = int(width * i)
        heightDist = int(height * i)
        cv2.line(refImg, (vertical_start + widthDist, horizontal_start), (vertical_start + widthDist, h - 613), (0, 255, 0), 8, 1)
        cv2.line(refImg, (vertical_start, horizontal_start + heightDist), (w - 159, horizontal_start + heightDist), (0, 255, 0), 8, 1)

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
    refImg = cv2.cvtColor(refImg, cv2.COLOR_RGB2BGR)

    tiles = []
    tile_indicies = []
    h, w, r = refImg.shape
    print(h,w,r)

    width = int((w - 190) / 16 * 1)
    height = int((h - 645) / 16 * 1)

    start = [vertical_start, horizontal_start]

    print(width, height, start)

    f = open('wynik.txt', "w+")

    min_letter_black = 5000
    min_letter = []
    max_non_letter_black = 0
    max_non_letter = []

    for i in range(0, 15):
        for j in range(0, 15):
            tile = refImg[start[1] + height * i: start[1] + height * (i + 1),
                   start[0] + width * j: start[0] + width * (j + 1)]

            #cv2.imwrite("Tiles/og_tiles/" + str(i) + "," + str(j) + ".png",tile)

            tile_HSV = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)
            lower_black_HSV = np.array([0,0,0])
            upper_black_HSV = np.array([180,255,50])
            shapeMask_HSV = cv2.inRange(tile_HSV, lower_black_HSV, upper_black_HSV)

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

            cv2.imwrite("Tiles/hsv_mask/" + str(i) + "," + str(j) + ".png",shapeMask_HSV)

            # skip center star for now as it causes issues (7,7)
            if (black_pixels > 1000 and idx != [7,7]):
                tiles.append(shapeMask_HSV)
                tile_indicies.append(idx)
            else:
                tiles.append(0)

    f.close()
    print("Max non letter black: " + str(max_non_letter) + ", black: " + str(max_non_letter_black))
    print("Min letter black: " + str(min_letter) + ", black: " + str(min_letter_black))
    print("Tiles with letters inside:")
    print(tile_indicies)
    return tiles


def start_capture():
    with open("test_img/IMG_0990.png", "r+b") as image:
        frameRaw = image.read()
    frame = np.array(bytearray(frameRaw), dtype=np.uint8)
    frame = cv2.imdecode(frame, -1)

    #img_counter = 0
    #img_name = 'board_frame_{}.png'.format(img_counter)
    #cv2.imwrite(img_name, frame)

    board_detection_BRISK(frame)



def main():
    testImg = cv2.imread('test_img/board_frame_11.png', 1)
    board_detection_BRISK(testImg)
    # show_ip_webcam()


if __name__ == '__main__':
    main()
