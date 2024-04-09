import cv2
import numpy as np

img_src = cv2.imread('images/penguin.jpg', cv2.IMREAD_COLOR)
height, width = img_src.shape[:2]
# split
img_b,img_g,img_r = cv2.split(img_src)

# np.ones -> 모든값을 1로
# using dtype=uint8
#img_w = np.ones((height,width,1),dtype=np.uint8)
# img_w = img_w*255

# using dtype=double (0~1사이의 값을 black~white로 표시)
img_w = np.ones((height,width,1),dtype=np.double)
cv2.imshow('w',img_w)

# using np.zeros
img_z = np.zeros((height,width,1),dtype=np.uint8)
img_dst = cv2.merge((img_z,img_z,img_r))
# cv2.imshow('0zero',img_z)
# cv2.imshow('b',img_b)
# cv2.imshow('g',img_g)
# cv2.imshow('r',img_r)
cv2.imshow('dst',img_dst)

# using np.zeros_like
img_zero = np.zeros_like(img_src)
#img_zero[:,:,0]=img_b
img_zero[:,:,1]=img_g
#img_zero[:,:,2]=img_r

cv2.imshow('dst2',img_zero)

cv2.imshow('src',img_src)

cv2.waitKey()
cv2.destroyAllWindows()