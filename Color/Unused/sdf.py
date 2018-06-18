import cv2
import numpy as np


image= cv2.imread('fcwqcfwe.png')
empty_img = np.zeros((len(image),len(image[0]), 3), np.uint8)
mask = image[:,:,0] < 255
empty_img[mask] = (1,1,1)
#cv2.imshow("t",empty_img*255)
mask = empty_img[:,:,0] !=1
empty_img = np.zeros((len(image),len(image[0]), 3), np.uint8)
empty_img[mask] = (1,1,1)
image = empty_img*image
cv2.imshow("t",image)
print(cv2.waitKey(0))