from builtins import print
from scipy import ndimage
import numpy as np
from math import pi, sqrt, exp
import cv2
import os


def part1(img, mask, back, set, flag):

    h = img.shape[0]
    w = img.shape[1]

##applying mask
    for y in range(0, h):
      for x in range(0, w):
         if mask[y, x, 0] == 0 and mask[y, x, 1] == 0 and mask[y, x, 2] == 0:
             img[y, x] = [0, 0, 0]

    for y in range(0, h):
      for x in range(0, w):
         if mask[y, x, 0] != 0 and mask[y, x, 1] != 0 and mask[y, x, 2] != 0:
             if set == 2: ##placement of image set 2
                back[y+15, x-17, 0] = img[y, x, 0]
                back[y+15, x-17, 1] = img[y, x, 1]
                back[y+15, x-17, 2] = img[y, x, 2]
             else:
                 back[y, x, 0] = img[y, x, 0]
                 back[y, x, 1] = img[y, x, 1]
                 back[y, x, 2] = img[y, x, 2]

    if flag == 0:
        cv2.imwrite("part1/" + str(set) + ".jpg", back)
    else:
        cv2.imwrite("part2/" + str(set) + ".jpg", back)
    return

def gauss(n=11,sigma=1):
    r = range(-int(n/2),int(n/2)+1)
    return [1 / (sigma * sqrt(2*pi)) * exp(-float(x)**2/(2*sigma**2)) for x in r]

def part2(img, imgg, mask, back, set):

    g = gauss(100,3)
    gm = np.asmatrix(g)
    gat = np.vstack(g)

    gausss = np.matmul(gat, gm)
    gausst = gausss[:,:,None]
    imgg = imgg[:, :, None]

    back = ndimage.convolve(back, gausst, mode='reflect')

    img_blurred = ndimage.convolve(imgg, gausst, mode='reflect')
    img_diff = imgg - img_blurred
    alpha = 0.01
    unsharpen_img = img + alpha*img_diff
    part1(unsharpen_img, mask, back, set ,1)

    return



def main():
    try:
        if not os.path.exists("part1/"):
            os.makedirs("part1/")
    except OSError:
        print('Error: Creating directory. ')
        
    try:
        if not os.path.exists("part2/"):
            os.makedirs("part2/")
    except OSError:
        print('Error: Creating directory. ')

    for set in range(1, 6):
        imgg = cv2.imread("images/im" + str(set) + ".jpg", 0)
        img = cv2.imread("images/im" + str(set) + ".jpg",)
        mask = cv2.imread("images/mask" + str(set) + ".png")
        back = cv2.imread("images/back" + str(set) + ".jpg")
        back1 = cv2.imread("images/back" + str(set) + ".jpg")
        part1(img, mask, back, set, 0)
        part2(img, imgg, mask, back1, set)
    return

main()
