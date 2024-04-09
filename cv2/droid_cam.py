import cv2

th = 'THRESH'
title_trackbar = 'Min Threshold:'


def on_trackbar(value):
    global thresh1
    thresh1 = value


def window(named):
    cv2.namedWindow(named)
    cv2.createTrackbar(title_trackbar, th, 0, 255,on_trackbar)


def onChange(frame_gray):
    # _, thresh_cv1 = cv2.threshold(frame_gray, thresh=thresh1, maxval=255, type=cv2.THRESH_BINARY)
    _, thresh_cv2 = cv2.threshold(frame_gray, thresh=thresh1, maxval=255, type=cv2.THRESH_BINARY_INV)
    # _, thresh_cv3 = cv2.threshold(frame_gray, thresh=thresh1, maxval=255, type=cv2.THRESH_TRUNC)
    # _, thresh_cv4 = cv2.threshold(frame_gray, thresh=thresh1, maxval=255, type=cv2.THRESH_TOZERO)
    # _, thresh_cv5 = cv2.threshold(frame_gray, thresh=thresh1, maxval=255, type=cv2.THRESH_TOZERO_INV)
    # img_u = cv2.hconcat([frame, thresh_cv1, thresh_cv2])
    # img_d = cv2.hconcat([thresh_cv3, thresh_cv4, thresh_cv5])
    # img_all = cv2.vconcat([img_u, img_d])
    print(thresh_cv2.shape)
    contours, hierarchy = cv2.findContours(thresh_cv2, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for i, contour in enumerate(contours):
        # print(f'{i} : {cv2.contourArea(contour)}')
        area = cv2.contourArea(contour)
        if area >= 500:
            cv2.drawContours(frame, [contour], 0, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(contour)
            pt1 = (x, y);
            pt2 = (x + w, y + h)
            cv2.rectangle(frame, pt1, pt2, (255, 0, 0), 1)
            #### moment
            mu = cv2.moments(contour)
            cX = int(mu['m10'] / (mu['m00']) + 1e-5)
            cY = int(mu['m01'] / (mu['m00']) + 1e-5)
            cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)
            cv2.putText(frame, f'{i}:{area}', (cX - 60, cY + 25), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 1)
    cv2.imshow(th, frame)
    # cv2.imshow(th, img_all)


video = cv2.VideoCapture('http://192.168.0.20:4747/video')
thresh1 = 0

window(th)


while True:
    ret, frame = video.read()
    if not ret:
        break
    frame = cv2.pyrDown(frame)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # frame_gray = cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2BGR)
    onChange(frame_gray)
    # Press 'Esc' to stop
    key = cv2.waitKey(25)
    if key == 27:
        break

if video.isOpened():
    video.release()