import cv2
import numpy as np

lowerBound=np.array([33,80,40])
upperBound=np.array([102,255,255])

cam= cv2.VideoCapture(0)
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

font = cv2.FONT_HERSHEY_SIMPLEX

while True:



    ret, img=cam.read()
    img=cv2.resize(img,(680,440))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(gray, 50, 100, 255)
    cv2.imshow("cam",edged)



    #Convertir BGR to HSV
    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #cv2.imshow("cam",imgHSV[:,:,0])
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

    maskFinal=maskClose
    h, conts, _ = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.drawContours(img,conts,-1,(255,0,0),3)
    for i in range(len(conts)):
        x,y,w,h=cv2.boundingRect(conts[i])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255), 2)
        #Arreglar esto
        #cv2.putText(np.array(img), str(i+1),(x,y+h),font,(0,255,255))

    #cv2.imshow("maskClose",maskClose)
    #cv2.imshow("maskOpen",maskOpen)
    #cv2.imshow("mask",mask)
    cv2.imshow("cam",img)
    cv2.imshow("cam2",edged)
    cv2.waitKey(10)