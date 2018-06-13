import cv2
import imutils
import numpy as np

from pyimagesearch.shapedetector import ShapeDetector

#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,help="path to the input image")
#args = vars(ap.parse_args())

#image = cv2.imread(args["image"])
#image = cv2.imread("test2.jpg")
#def detectcolorshape(image):

	#image = cv2.imread("try.png")
cam = cv2.VideoCapture(0)
sd = ShapeDetector()
ratio = 0
while True:


    ret, image=cam.read()
    #image = cv2.imread('Unused/try.png')
    resized = imutils.resize(image, width=600)
    if(ratio==0):
        ratio = image.shape[0] / float(resized.shape[0])
    blurred = cv2.GaussianBlur(resized, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 100, 255)
    cv2.imshow("ss", edged)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    for c in cnts:
        M = cv2.moments(c)
        if(M["m00"] == 0):
            continue
        cX = int((M["m10"] / M["m00"]) * ratio)
        cY = int((M["m01"] / M["m00"]) * ratio)
        shape = sd.detect(c)
        if shape is not "square":
            continue
        area = cv2.contourArea(c, False)
        if(area<2000):
            continue
        #print(area)
        c = c.astype("float")
        c *= ratio
        c = c.astype("int")
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        mask = np.zeros(image.shape, np.uint8)
        cv2.drawContours(mask, [c], -1, (1,1,1), cv2.FILLED)
        sign=image*mask
        cv2.imshow("mask", mask)
        




    cv2.imshow("Image", image)
    cv2.waitKey(10)

