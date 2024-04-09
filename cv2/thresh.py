import cv2

th = 'THRESH'
title_trackbar = 'Min Threshold:'


def window(named):
    cv2.namedWindow(named)
    cv2.createTrackbar(title_trackbar, named, 127, 255, onChange)


def onChange(val):
    thresh1 = val
    # thresh1 = cv2.getTrackbarPos('T', window_name)
    _, thresh_cv1 = cv2.threshold(img_src, thresh=thresh1, maxval=255, type=cv2.THRESH_BINARY)
    _, thresh_cv2 = cv2.threshold(img_src, thresh=thresh1, maxval=255, type=cv2.THRESH_BINARY_INV)
    _, thresh_cv3 = cv2.threshold(img_src, thresh=thresh1, maxval=255, type=cv2.THRESH_TRUNC)
    _, thresh_cv4 = cv2.threshold(img_src, thresh=thresh1, maxval=255, type=cv2.THRESH_TOZERO)
    _, thresh_cv5 = cv2.threshold(img_src, thresh=thresh1, maxval=255, type=cv2.THRESH_TOZERO_INV)
    img_u=cv2.hconcat([img_src, thresh_cv1,thresh_cv2])
    img_d=cv2.hconcat([thresh_cv3, thresh_cv4, thresh_cv5])
    img_all=cv2.vconcat([img_u, img_d])
    cv2.imshow(th, img_all)


img_src = cv2.imread('images/penguin.jpg', cv2.IMREAD_GRAYSCALE)

window(th)
onChange(0)

th2 = cv2.adaptiveThreshold(img_src, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 5)
th3 = cv2.adaptiveThreshold(img_src, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 5)
cv2.imshow('mean_c', th2)
cv2.imshow('gaussian_c', th3)

cv2.waitKey()
cv2.destroyAllWindows()