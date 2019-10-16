import capture
import time
import sys
import capture as cap
import cv2
begin = "               " + \
        "               " + \
        "               " + \
        "               " + \
        "               " + \
        "               " + \
        "  scrabble     " + \
        "               " + \
        "      czeker   " + \
        "               " + \
        "               " + \
        "               " + \
        "               " + \
        "               " + \
        "               "

ex1 = "               " + \
      "               " + \
      "               " + \
      "               " + \
      "               " + \
      "       o       " + \
      "       s       " + \
      "       i       " + \
      "       e       " + \
      "       m       " + \
      "               " + \
      "               " + \
      "               " + \
      "               " + \
      "               "

ex2 = "               " + \
      "               " + \
      "               " + \
      "               " + \
      "               " + \
      "       o       " + \
      "       s       " + \
      "       i       " + \
      "    apteka     " + \
      "       m       " + \
      "               " + \
      "               " + \
      "               " + \
      "               " + \
      "               "

ex3 = "               " + \
      "               " + \
      "               " + \
      "               " + \
      "               " + \
      "       o       " + \
      "    t  s       " + \
      "    r  i       " + \
      "    apteka     " + \
      "    m  m       " + \
      "    w          " + \
      "    a          " + \
      "    j          " + \
      "               " + \
      "               "

ex4 = "               " + \
      "               " + \
      "               " + \
      "               " + \
      "               " + \
      "       o       " + \
      "    t  s       " + \
      "    r  i       " + \
      "    apteka     " + \
      "    m  m       " + \
      "    w          " + \
      "    a          " + \
      "  maj          " + \
      "               " + \
      "               "

ex5 = "               " + \
      "               " + \
      "               " + \
      "               " + \
      "               " + \
      "       o       " + \
      "    t  s       " + \
      "    r  i       " + \
      "    apteka     " + \
      "    m  m       " + \
      "    w          " + \
      "    akord      " + \
      "  maj          " + \
      "               " + \
      "               "

ex6 = "               " + \
      "               " + \
      "               " + \
      "               " + \
      "               " + \
      "       o       " + \
      "    t  s       " + \
      "    r  i       " + \
      "    apteka     " + \
      "    m  m       " + \
      "    w          " + \
      "    akord      " + \
      "  maj   o      " + \
      "        m      " + \
      "               "

ex7 = "               " + \
      "               " + \
      "               " + \
      "               " + \
      "               " + \
      "       o       " + \
      "    t  s       " + \
      "    r  i       " + \
      "    apteka     " + \
      "    m  m       " + \
      "    w          " + \
      "    akordeon   " + \
      "  maj   o      " + \
      "        m      " + \
      "               "

ex8 = "               " + \
      "               " + \
      "               " + \
      "               " + \
      "               " + \
      "       o j     " + \
      "    t  s a     " + \
      "    r  i v     " + \
      "    apteka     " + \
      "    m  m       " + \
      "    w          " + \
      "    akordeon   " + \
      "  maj   o      " + \
      "        m      " + \
      "               "

ex9 = "               " + \
      "               " + \
      "               " + \
      "               " + \
      "               " + \
      "       o       " + \
      "    t  s       " + \
      "    r  i       " + \
      "    apteka     " + \
      "    m  m       " + \
      "    w          " + \
      "    akordeon   " + \
      "  maj   o      " + \
      "        m      " + \
      "               "

ex10 = "               " + \
       "               " + \
       "               " + \
       "               " + \
       "               " + \
       "      koń      " + \
       "    t  s       " + \
       "    r  i       " + \
       "    apteka     " + \
       "    m  m       " + \
       "    w          " + \
       "    akordeon   " + \
       "  maj   o      " + \
       "        m      " + \
       "               "

ex11 = "               " + \
       "               " + \
       "               " + \
       "               " + \
       "               " + \
       "      koń      " + \
       "    t  s       " + \
       "    r  i       " + \
       "    apteka     " + \
       "    m  m       " + \
       "    w          " + \
       "    akordeon   " + \
       "  maj   o      " + \
       "       ćma     " + \
       "               "

ex12 = "               " + \
       "               " + \
       "               " + \
       "               " + \
       "               " + \
       "      koń      " + \
       "    t  s       " + \
       "    r  i       " + \
       "    apteka     " + \
       "    m  m       " + \
       "    w          " + \
       "    akordeon   " + \
       "  maj   o  ó   " + \
       "       ćma ż   " + \
       "               "

ex13 = "               " + \
       "               " + \
       "               " + \
       "               " + \
       "               " + \
       "      koń      " + \
       "    t  s       " + \
       "    r  i       " + \
       "    apteka     " + \
       "    m  m       " + \
       "    w          " + \
       "    akordeon   " + \
       "  maj   o  ó   " + \
       "       ćma żółć" + \
       "               "

ex14 = "               " + \
       "      p        " + \
       "      a        " + \
       "      j        " + \
       "      ą        " + \
       "      koń      " + \
       "    t  s       " + \
       "    r  i       " + \
       "    apteka     " + \
       "    m  m       " + \
       "    w          " + \
       "    akordeon   " + \
       "  maj   o  ó   " + \
       "       ćma żółć" + \
       "               "

ex15 = "               " + \
       "      p        " + \
       "     maź       " + \
       "      j        " + \
       "      ą        " + \
       "      koń      " + \
       "    t  s       " + \
       "    r  i       " + \
       "    apteka     " + \
       "    m  m       " + \
       "    w          " + \
       "    akordeon   " + \
       "  maj   o  ó   " + \
       "       ćma żółć" + \
       "               "


def main():
    print(begin)
    sys.stdout.flush()
    time.sleep(15)

    #testImg = cv2.imread('board_frame_0.png', 1)
    #cap.board_detection_BRISK(testImg)
    cap.show_ip_webcam()



if __name__ == '__main__':
    main()
