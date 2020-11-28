
import cv2
import board
import neopixel
import random
import time

#methods
def centroid(person_object):
    x, y, w, h = person_object
    return (x+(w/2),y+(h/2))

def random_color():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

#hardcodes
num_pixels = 50
limit=10
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(board.D18,num_pixels,brightness = .1, auto_write=False, pixel_order=ORDER)




# cap = cv2.VideoCapture('rtsp://Foscam1:Longhorn1!@192.168.1.14:88/videoMain')
cap = cv2.VideoCapture(0)

# classifier = cv2.CascadeClassifier('/home/pi/tflite1/haarcascade/haarcascade_fullbody.xml')
classifier = cv2.CascadeClassifier('/home/pi/tflite1/haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    if ret==False:
        continue
    scale_percent = 100 #percent of original
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)

    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    persons_detected = classifier.detectMultiScale(frame,1.3,5)
    
    try:
        human_count = persons_detected.shape[0]
    except:
        human_count = 0
    
    for (x,y,w,h) in persons_detected:
        cv2.rectangle(frame, (x,y) , (x+w ,y+h), (255,0,0),2 )
        
    try:
        cv2.imshow('frame',frame)
    except:
        pass
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    if human_count>0:
        person1_pos = centroid(persons_detected[0])
        person1_pos_x = person1_pos[0]
        person1_pos_x_pct = person1_pos_x/width
        pix_i = int(person1_pos_x_pct*num_pixels)
        for i in range(num_pixels):
            if pix_i == i:
                pixels[pix_i]=(255,0,255)
            else:
                pixels[i] = (0,0,0)
        pixels.show()
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break 

pixels.deinit()
cap.release()
cv2.destroyAllWindows()    