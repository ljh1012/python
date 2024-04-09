import cv2
img_ori = cv2.imread('images/morphological.png',cv2.IMREAD_GRAYSCALE)
img_src = cv2.imread('images/morph_dot.png',cv2.IMREAD_GRAYSCALE) #글자에 구멍

height,width = img_src.shape[:2]
img_ori = cv2.hconcat([img_ori,img_src])

_, img_bin = cv2.threshold(img_src,128,255,cv2.THRESH_BINARY)

#erosion
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))

img_erode = cv2.erode(img_bin,kernel)
img_open = cv2.dilate(img_erode,kernel)

img_dst = cv2.hconcat([img_erode,img_open])
img_ori = cv2.vconcat([img_ori,img_dst])
cv2.imshow('opening',img_ori)
img_opening = cv2.morphologyEx(img_bin,cv2.MORPH_OPEN,kernel)
cv2.imshow('open',img_opening)
cv2.waitKey()
cv2.destroyAllWindows()
