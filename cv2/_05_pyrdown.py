import cv2

capture = cv2.VideoCapture('images/vvv.mp4')

while cv2.waitKey(33) < 0:
    # 동영상 재생이 끝나면 다시 처음부터 재생
    if capture.get(cv2.CAP_PROP_POS_FRAMES) == capture.get(cv2.CAP_PROP_FRAME_COUNT):
        capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

    ret, frame = capture.read()
    frame = cv2.pyrDown(frame)

    height, width = frame.shape[:2]
    #img_src1 = cv2.resize(frame, (0, 0), img_src1, 0.33, 0.2, cv2.INTER_LINEAR)
    img_src1 = cv2.resize(frame, dsize=(width//3, height//4), interpolation=cv2.INTER_LINEAR)

    flipCode_ud = 0
    img_ud = cv2.flip(img_src1, flipCode_ud)
    flipCode_lr = 1
    img_lr_1 = cv2.flip(img_src1, flipCode_lr)
    img_lr_2 = cv2.flip(img_src1, flipCode_lr)

    img_b = cv2.hconcat([img_lr_1, img_ud, img_lr_2])
    if (width//3)*3 != width:
        img_b = cv2.resize(img_b, dsize=(width, height//4), interpolation=cv2.INTER_LINEAR)

    img_a = cv2.vconcat([frame, img_b])

    cv2.imshow("YouTubeVideoFrame", img_a)


capture.release()
cv2.destroyAllWindows()

