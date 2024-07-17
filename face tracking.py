import cv2

cap=cv2.VideoCapture(0)
if not cap.isOpened():
    print("error opening the camera pls calibrate it")
    exit()

cv2.namedWindow('webcam',cv2.WINDOW_NORMAL)
while True:
    ret, frame = cap.read()
    if ret:
        mirrored_frame = cv2.flip(frame, 1)
        cv2.imshow("webcam",mirrored_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
