
import cv2

# cap = cv2.VideoCapture('rtsp://Foscam1:Longhorn1!@192.168.1.14:88/videoMain')
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    try:
        cv2.imshow('frame',frame)
    except:
        pass
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()    