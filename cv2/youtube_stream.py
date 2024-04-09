import cv2

from cap_from_youtube import cap_from_youtube
youtube_url = 'https://youtu.be/hP0xTps7evY?si=bg9F2-wz-uPYWjpz'
capture = cap_from_youtube(youtube_url, '720p')
# Resolution examples: '144p', '240p', '360p', '480p', '720p', '1080p', '1440p', '2160p', 'best'
# from : https://pypi.org/project/cap-from-youtube/

# capture = cv2.VideoCapture('images/viviz.mp4')

while cv2.waitKey(33) < 0:
    ret, frame = capture.read()
    cv2.imshow("YouTubeVideoFrame", frame)

capture.release()
cv2.destroyAllWindows()