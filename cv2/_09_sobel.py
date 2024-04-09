import cv2


window_name = ('Sobel Demo - Simple Edge Detector')
scale = 1
delta = 0
ddepth = cv2.CV_16S

src = cv2.imread('images/penguin.jpg', cv2.IMREAD_COLOR)
# Check if image is loaded fine

src = cv2.GaussianBlur(src, (3, 3), 0)
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
# Gradient-Y
# grad_y = cv.Scharr(gray,ddepth,0,1)
grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)

abs_grad_x = cv2.convertScaleAbs(grad_x)
abs_grad_y = cv2.convertScaleAbs(grad_y)

grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
cv2.imshow(window_name, grad)
cv2.waitKey()
cv2.destroyAllWindows()


#흑백

##이진화
### _, thresh_cv1 = cv2.threshold(img_src, thresh=thresh1, maxval=255, type=cv2.THRESH_BINARY)
### _, thresh_cv2 = cv2.threshold(img_src, thresh=thresh1, maxval=255, type=cv2.THRESH_BINARY_INV)
### _, thresh_cv3 = cv2.threshold(img_src, thresh=thresh1, maxval=255, type=cv2.THRESH_TRUNC)
### _, thresh_cv4 = cv2.threshold(img_src, thresh=thresh1, maxval=255, type=cv2.THRESH_TOZERO)
### _, thresh_cv5 = cv2.threshold(img_src, thresh=thresh1, maxval=255, type=cv2.THRESH_TOZERO_INV)

##엣지 검출
###소벨, 캐니

##블러링
###cv2.blur
###cv2.GaussianBlur



#컬러

##BGR
###src = cv2.imread("Image/tomato.jpg", cv2.IMREAD_COLOR) or src = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)
###b, g, r = cv2.split(src)
###inverse = cv2.merge((r, g, b))

##hsv
###hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
###h, s, v = cv2.split(hsv)
### lower_red = cv2.inRange(hsv, (0, 100, 100), (5, 255, 255))  HSV에서 색은 180까지, 빨강은 180 전후
### upper_red = cv2.inRange(hsv, (170, 100, 100), (180, 255, 255)) cv2.inRange -> 1 channel로 반환
### added_red = cv2.addWeighted(lower_red, 1.0, upper_red, 1.0, 0.0)
### red = cv2.bitwise_and(hsv, hsv, mask = added_red)
### red = cv2.cvtColor(red, cv2.COLOR_HSV2BGR)


#morphology
###dialation   팽창
#### kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
#### img_dial = cv2.dilate(img_bin,kernel)
#### img_dst = cv2.erode(img_dial,kernel)
###erosion    수축
#### kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
#### img_dial2 = cv2.erode(img_bin2,kernel)
#### img_dst2 = cv2.dilate(img_dial2,kernel)