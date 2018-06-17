from pyimagesearch.shapedetector import ShapeDetector
from pyimagesearch.colorlabeler import ColorLabeler
#import argparse
import imutils
import cv2
import numpy as np

#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,help="path to the input image")
#args = vars(ap.parse_args())

#image = cv2.imread(args["image"])
#image = cv2.imread("test2.jpg")
#def detectcolorshape(image):


cam = cv2.VideoCapture(0)
ret, image=cam.read()
image = cv2.imread("seniales.png")
resized = imutils.resize(image, width=600)
cv2.imshow("ss", resized)

ratio = image.shape[0] / float(resized.shape[0])

blurred = cv2.GaussianBlur(resized, (1, 1), 0)
cv2.waitKey(0)
edged = cv2.Canny(blurred, 50, 100, 255)
cv2.imshow("ss", edged)

#gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
#thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
#cv2.imshow("Thresh", thresh)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)

#contours = np.array([])
#hierarchy = np.array([])
#cv2.findContours(edged.copy(),cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE, contours, hierarchy,(0,0) )

#for i in range(len(contours)):
#    if (hierarchy[i][3] >= 0)  : #has parent, inner (hole) contour of a closed edge (looks good)
#        cv2.drawContours(resized, contours, i, (255, 0, 0), 1, 8)


# cv2.imshow("ss", resized)
#cv2.waitKey(0)

cnts = cnts[0] if imutils.is_cv2() else cnts[1]

sd = ShapeDetector()
cl = ColorLabeler()


cv2.waitKey(0)
if(len(cnts)>0):
    for c in cnts:
        M = cv2.moments(c)
        if(M["m00"] == 0):
            continue
        cX = int((M["m10"] / M["m00"]) * ratio)
        cY = int((M["m01"] / M["m00"]) * ratio)
        shape = sd.detect(c)
        if shape == "square":
            color = cl.label(lab, c)
            c = c.astype("float")
            c *= ratio
            c = c.astype("int")
            text = "{} {}".format(color, shape)
            cv2.drawContours(image, [c], -1, (0, 255, 0), cv2.FILLED)
            cv2.putText(image, text, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 2, (100, 100, 100), 2)

            resized = imutils.resize(image, width=600)
            cv2.imshow("Image", resized)
            cv2.waitKey(0)
