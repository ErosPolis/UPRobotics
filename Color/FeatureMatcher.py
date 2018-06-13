
import cv2
import imutils
import numpy as np
import cv2
from matplotlib import pyplot as plt


def FeatureMatcher(img,img2):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img=imutils.resize(img, width=300)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    img2=imutils.resize(img2, width=600)
    # img2 = cv2.GaussianBlur(img2, (5, 5), 0)
    MIN_MATCH_COUNT = 10
    # Initiate ORB detector
    orb = cv2.ORB_create()
    # find the keypoints and descriptors with ORB
    kp1 = orb.detect(img,None)
    kp1, des1 = orb.compute(img,kp1)

    img0 = cv2.drawKeypoints(img, kp1, None, color=(0,255,0), flags=0)
    #cv2.imshow("cc",img0)
    kp2, des2 = orb.detectAndCompute(img2,None)

    FLANN_INDEX_LSH = 6
    index_params= dict(algorithm = FLANN_INDEX_LSH,
                       table_number = 6, # 12
                       key_size = 12,     # 20
                       multi_probe_level = 1) #2
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, None)
    matches = flann.knnMatch(des1,des2,k=2)

    good = []
    for aa in matches:
        if(len(aa)<2):
            continue
        m,n =aa
        if m.distance < 0.7*n.distance:
            good.append(m)

    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()
        h,w,d = img.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)
        img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
    else:
        print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
        matchesMask = None

    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)
    img3 = cv2.drawMatches(img,kp1,img2,kp2,good,None,**draw_params)
    plt.imshow(img3, 'gray'),plt.show()

if __name__ == "__main__":
    img = cv2.imread('Unused/try.png')
    img2 = cv2.imread('Unused/seniales.png')
    FeatureMatcher(img, img2)
