import cv2
import numpy as np

def draw_lines():
    pt1 = (100,100); pt2 = (700,100)
    green_color = (0,255,0)
    cv2.line(img_src,pt1,pt2,green_color,2)

height,width,channel = (600,800,3)
img_src = np.zeros((height,width,channel),dtype=np.uint8)
draw_lines()   # 선그리기 함수
cv2.imshow('src',img_src)
cv2.waitKey()
cv2.destroyAllWindows()