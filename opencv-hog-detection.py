import numpy as np
import cv2
import subprocess

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)


if __name__ == '__main__':

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
    #cap=cv2.VideoCapture('videos/General_public.mov')
    #https://www.youtube.com/watch?v=uuQlMCMT71I
    #https://www.youtube.com/watch?v=tI7fktKY6OU
    #
    videoUrl = subprocess.Popen("C:\Python27\Scripts\youtube-dl.exe -f22 -g https://www.youtube.com/watch?v=tI7fktKY6OU", shell=True, stdout=subprocess.PIPE).stdout.read()
    videoUrl = videoUrl.decode("utf-8").rstrip()
    print(videoUrl)

    procWidth = int(1280/4)
    procHeight = int(720/4)

    cap=cv2.VideoCapture(videoUrl)
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, procWidth)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, procHeight)

    while True:
        _,frame=cap.read() 

        #(heihht,witdth) = frame.shape()
        #(height, width, channels) = frame.shape()
        #height, width = frame.shape[:2]
        #width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
        #height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # float

        #frame = cv2.resize(frame, (int(width/2), int(height/2)))       
        
         # Start timer
        timer = cv2.getTickCount()

        found,w=hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05)
        draw_detections(frame,found)
        
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
 
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(round(fps,2)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)
         
        cv2.imshow('feed',frame)
        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            break
    cv2.destroyAllWindows()