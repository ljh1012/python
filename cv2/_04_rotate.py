import cv2

ryan_path = 'C:/Users/HKIT/Downloads/Hello/images/ryan.jpg'
viviz_path = 'C:/Users/HKIT/Downloads/Hello/images/viviz.mp4'

img_src = cv2.imread(ryan_path, cv2.IMREAD_COLOR)
height, width = img_src.shape[:2]

rotate_matrix = cv2.getRotationMatrix2D((width//2, height//2),90,1)
img_dst = cv2.warpAffine(img_src,rotate_matrix, (width,height))
cv2.imshow('src',img_src)
cv2.imshow('dst',img_dst)
cv2.waitKey()
cv2.destroyAllWindows()