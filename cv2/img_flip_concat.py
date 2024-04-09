import cv2    # opencv 라이브러리를 사용

# 이미지 로딩
img_src = cv2.imread('images/penguin.jpg', cv2.IMREAD_COLOR)
img_src = cv2.pyrDown(img_src) #이미지 절반으로 줄이기

FLIP_LR = 1
img_lr = cv2.flip(img_src, FLIP_LR)
FLIP_UD = 0
img_ud = cv2.flip(img_src, FLIP_UD)
FLIP_LR_UD = -1
img_lr_ud = cv2.flip(img_src, FLIP_LR_UD)

cv2.imshow('src', img_src)
cv2.imshow('lr', img_lr)
cv2.imshow('ud', img_ud)
cv2.imshow('lr-ud', img_lr_ud)

img_1 = cv2.hconcat([img_src, img_lr])
img_2 = cv2.hconcat([img_ud, img_lr_ud])
img_dst = cv2.vconcat([img_1, img_2])

cv2.imshow('dst', img_dst)


cv2.waitKey()
cv2.destroyAllWindows()

