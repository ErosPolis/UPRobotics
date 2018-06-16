import numpy as np
import cv2
import imutils

img = cv2.imread('seniales.png')
print(img.shape)
img = imutils.resize(img, width=600)
Z = img.reshape((-1,3))
print(Z.shape)
# convert to np.float32
Z = np.float32(Z)

# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 3, 1.0)
K = 8
ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

# Now convert back into uint8, and make original image
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))
#cv2.imshow('res2',res2)
cv2.waitKey(0)
cv2.destroyAllWindows()