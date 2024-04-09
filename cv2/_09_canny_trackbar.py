from __future__ import print_function
import cv2

max_lowThreshold = 100
window_name = 'Edge Map'
title_trackbar = 'Min Threshold:'
ratio = 3
kernel_size = 3


def CannyThreshold(val):
    low_threshold = val
    img_blur = cv2.blur(src_gray, (3,3))
    detected_edges = cv2.Canny(img_blur, low_threshold, low_threshold*ratio, kernel_size)
    cv2.imshow(window_name, detected_edges)
    #color mode
    # mask = detected_edges != 0
    # dst = src * (mask[:,:,None].astype(src.dtype))
    # cv2.imshow(window_name, mask)


src = cv2.imread('images/pawn.png',cv2.IMREAD_COLOR)
src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
cv2.namedWindow(window_name)
cv2.createTrackbar(title_trackbar, window_name , 0, max_lowThreshold, CannyThreshold)
CannyThreshold(0)
cv2.waitKey()