import cv2

ryan_path = 'C:/Users/HKIT/Downloads/Hello/images/ryan.jpg'
viviz_path = 'C:/Users/HKIT/Downloads/Hello/images/viviz.mp4'
img_src = cv2.imread(ryan_path, cv2.IMREAD_COLOR)
height, width = img_src.shape[:2]

img_gray = cv2.resize(img_src,dsize=(width//3,height//3),interpolation=cv2.INTER_LINEAR)
img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
img_b1 = cv2.flip(img_gray,1)
img_b2 = cv2.flip(img_gray,0)
img_dst = cv2.hconcat([img_b1,img_b2])
img_b3 = img_b1.copy()
img_dst = cv2.hconcat([img_dst,img_b3])
if (width//3)*3 != width:
    img_dst = cv2.resize(img_dst,dsize=(width,height//3),interpolation=cv2.INTER_LINEAR)
img_dst = cv2.cvtColor(img_dst,cv2.COLOR_GRAY2BGR)
img_dst = cv2.vconcat([img_src,img_dst])

# cv2.imshow('src',img_src)
cv2.imshow('dst',img_dst)

cv2.waitKey()
cv2.destroyAllWindows()