import cv2
img_ori = cv2.imread('images/morphological.png',cv2.IMREAD_GRAYSCALE)
img_src = cv2.imread('images/morph_hole.png',cv2.IMREAD_GRAYSCALE) #글자에 구멍
img_src2 = cv2.imread('images/morph_dot.png',cv2.IMREAD_GRAYSCALE)
height,width = img_src.shape[:2]


img_ori = cv2.hconcat([img_ori,img_src])

_, img_bin = cv2.threshold(img_src,128,255,cv2.THRESH_BINARY)
_, img_bin2 = cv2.threshold(img_src2,128,255,cv2.THRESH_BINARY)

#dialation
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
img_dial = cv2.dilate(img_bin,kernel)
img_dst = cv2.erode(img_dial,kernel)

#erosion
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
img_dial2 = cv2.erode(img_bin2,kernel)
img_dst2 = cv2.dilate(img_dial2,kernel)

img_dst2 = cv2.hconcat([img_src2, img_dial2, img_dst2])
img_gray = cv2.hconcat([img_dial,img_dst])
img_ori = cv2.vconcat([img_ori,img_gray])

img_closing = cv2.morphologyEx(img_bin, cv2.MORPH_CLOSE, kernel)

cv2.imshow('ori',img_ori)
cv2.imshow('opening',img_dst2)

cv2.waitKey()
cv2.destroyAllWindows()
