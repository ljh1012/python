import cv2
img_src = cv2.imread('images/1.png',cv2.IMREAD_COLOR)
height,width = img_src.shape[:2]
# 이미지 색변환 -> gray
img_gray = cv2.cvtColor(img_src,cv2.COLOR_BGR2GRAY)
# 이진화
ret,img_bin = cv2.threshold(img_gray, 250.,255, cv2.THRESH_BINARY_INV)

# kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
# img_bin = cv2.morphologyEx(img_bin,cv2.MORPH_OPEN, kernel, iterations=2)

contours, hierarchy = cv2.findContours(img_bin,cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

for i, contour in enumerate(contours):
    # print(f'{i} : {cv2.contourArea(contour)}')
    area = cv2.contourArea(contour)
    if area>=500:
        cv2.drawContours(img_src, [contour],0,(0,255,0),2)
        x,y,w,h = cv2.boundingRect(contour)
        pt1 = (x,y); pt2 = (x+w,y+h)
        cv2.rectangle(img_src,pt1,pt2,(255,0,0),1)
        #### moment
        mu = cv2.moments(contour)
        cX = int(mu['m10'] / (mu['m00'])+ 1e-5)
        cY = int(mu['m01'] / (mu['m00'])+ 1e-5)
        cv2.circle(img_src,(cX,cY),5, (0,0,255),-1)
        cv2.putText(img_src,f'{i}:{area}', (cX-60,cY+25),
                cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255),1)

cv2.imshow('src',img_src)
cv2.imshow('bin',img_bin)

cv2.waitKey()
cv2.destroyAllWindows()


#사진 - 추출
# 엣지-(캐니, 소벨,
# 캐니 -
# 컬러-(bgr, hsv
# 도형-(contour