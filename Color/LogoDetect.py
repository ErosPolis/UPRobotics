import cv2
import imutils
import numpy as np
import math as mth
import os
from matplotlib import pyplot as plt

from pyimagesearch.shapedetector import ShapeDetector

def getconthist(contour,image,numbins):
    c = contour.astype("float")
    c *= ratio
    c = c.astype("int")
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    mask = np.zeros(image.shape, np.uint8)
    cv2.drawContours(mask, [c], -1, (1, 1, 1), cv2.FILLED)

    sign = cv2.cvtColor(image, cv2.COLOR_RGB2HSV) * mask

    stain = np.zeros((len(image), len(image[0]), 3), np.uint8)
    stainn = mask[:, :, 0] != 1
    stain[stainn] = (1, 1, 1)

    #cv2.imshow("mask", imutils.resize(image*mask, width=600))
    #cv2.imshow("mask2", imutils.resize(cv2.cvtColor(image, cv2.COLOR_RGB2HSV)[:, :, 1], width=600))
    #cv2.imshow("mask3", imutils.resize(cv2.cvtColor(image, cv2.COLOR_RGB2HSV)[:, :, 2], width=600))

    hist = cv2.calcHist([sign], [0], mask[:, :, 0], [numbins], [0, 256])


    #plt.figure()
    #plt.title("Hue Histogram")
    #plt.xlabel("Bins")
    #plt.ylabel("# of Pixels")
    #plt.plot(hist)
    #plt.xlim([0, numbins])
    #plt.show()

    return hist,stain,imutils.resize(image*mask, width=600)

def entropy(hist,numbins):
    prob = hist/numbins
    H =0
    for p in prob:
        if(p>0):
            H += p* mth.log(p,2)
    #print(H)
    return H/100000

def distanceE(v1,v2):
    if(len(v1)!= len(v2)):
        print("v1 and v2 differ lenght "+str(len(v1))+" "+str(len(v2)))
        return 0
    res = v1-v2
    res = res**2
    return mth.sqrt(sum(res))

def learn(dir,databins):

    files = os.listdir(dir)
    i = 0
    centers = []
    labels = []



    for ff in files:
        #plt.figure()
        #plt.title(ff)
        #plt.xlabel("numbins")
        #plt.ylabel("# of Pixels")
        im = os.listdir(dir+"/"+ff)
        logodata = []
        for f in im:
            image = cv2.imread(dir+"/"+ff+'/'+f)

            massk = np.zeros((len(image), len(image[0]), 3), np.uint8)
            m = image[:, :, 0] < 255
            massk[m] = (1, 1, 1)

            sign = cv2.cvtColor(image, cv2.COLOR_RGB2HSV) * massk
            # cv2.imshow("mask", imutils.resize(sign[:, :, 0], width=600))

            hist = cv2.calcHist([sign], [0], massk[:,:,0], [databins], [0, 256])
            #kdata = (hist / sum(hist))

            kdata = np.insert((hist / sum(hist)), len(hist),[entropy(hist, databins)])

            logodata.append(kdata)
            #print ( entropy(hist, numbins))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.01)
        compactness, labelss, cent = cv2.kmeans(np.array(logodata), 1,None, criteria, 3,cv2.KMEANS_RANDOM_CENTERS)
        centers.append(cent)
        #print(cent[0,100])
        labels.append(os.path.splitext(ff)[0])
        i +=1

        #plt.plot(cent[0])
        #plt.xlim([0, databins])
        #plt.show()
    return centers,labels

if __name__ == "__main__":
    cam = cv2.VideoCapture(0)
    sd = ShapeDetector()
    ratio = 0
    bins = 100
    minimError = 0.7

    # names = np.array([
    #     'Corrosive8',
    #     'DangerousWhenWet4',
    #     'ExplosiveS1',
    #     'FlamableLiquid3',
    #     'FlamableSolid4',
    #     'InfectiousSubstance6',
    #     'InhalationHazard2',
    #     'Non-FlamableGas2',
    #     'OrganicPeroxide52',
    #     'Oxidizer51',
    #     'RadioactiveII7',
    #     'SpontaneouslyCombustible4'
    # ])
    # centers = np.array([
    #     [6.1667204e-01, 3.5797948e-01, 1.4221043e-02, 1.3449433e-03, 6.5455498e-04,
    #      4.2999964e-04, 3.6072193e-04, 9.8183251e-04, 4.2044409e-04, 4.8589958e-03,
    #      4.2283299e-04, 9.4599923e-04, 3.2249972e-04, 3.8461079e-04, 0.0000000e+00,
    #      0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00,
    #      2.7633200e+05],
    #     [2.1014380e-01, 7.8919572e-01, 2.4644807e-05, 0.0000000e+00, 0.0000000e+00,
    #      0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 4.9289615e-06,
    #      2.4644808e-06, 3.2038247e-04, 1.2815300e-04, 1.7990709e-04, 0.0000000e+00,
    #      0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00,
    #      2.7506297e+05],
    #     [5.3515766e-02, 4.7590719e-03, 1.1474651e-03, 3.6486218e-04, 5.1556615e-04,
    #      3.9658934e-04, 4.9705862e-04, 5.5152355e-03, 8.8726288e-01, 1.2524291e-02,
    #      1.7399697e-02, 6.8583516e-03, 4.9996697e-03, 4.2249984e-03, 1.8507502e-05,
    #      0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00,
    #      2.5372841e+05],
    #     [1.7101380e-01, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00,
    #      0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 8.2898617e-01,
    #      0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00,
    #      0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00,
    #      2.2157308e+05],
    #     [5.4137766e-01, 9.3099382e-03, 2.0856841e-03, 2.9760060e-05, 5.2080104e-05,
    #      2.4800049e-06, 0.0000000e+00, 9.9944195e-04, 1.8996838e-03, 4.4386137e-01,
    #      2.2816045e-04, 1.2648026e-04, 2.4800049e-05, 2.4800049e-06, 0.0000000e+00,
    #      0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00,
    #      2.6583241e+05],
    #     [9.6082336e-01, 2.7911091e-02, 1.0157798e-02, 5.3773415e-06, 1.4787690e-04,
    #      0.0000000e+00, 0.0000000e+00, 1.2099018e-04, 0.0000000e+00, 5.6462086e-05,
    #      0.0000000e+00, 5.8344158e-04, 1.8551828e-04, 8.0660120e-06, 0.0000000e+00,
    #      0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00,
    #      2.5854662e+05],
    #     [1.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00,
    #      0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00,
    #      0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00,
    #      0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00,
    #      2.9634516e+05],
    #     [1.7718884e-01, 2.4722185e-05, 8.1382710e-01, 6.3016848e-03, 4.7713815e-04,
    #      4.9444370e-06, 0.0000000e+00, 2.1261079e-04, 1.4338866e-04, 1.4487200e-03,
    #      2.3238853e-04, 1.3844423e-04, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00,
    #      0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00,
    #      2.7394669e+05],
    #     [1.9646606e-01, 7.4871782e-06, 7.2625629e-04, 1.4974356e-05, 1.7470082e-05,
    #      4.9914520e-06, 1.7470082e-05, 4.0502140e-01, 1.6871109e-03, 3.9537293e-01,
    #      8.4854684e-05, 9.2341863e-05, 1.9466663e-04, 2.8950421e-04, 2.4957260e-06,
    #      0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00,
    #      2.5521995e+05],
    #     [1.7845549e-01, 9.9201179e-06, 7.4400887e-06, 0.0000000e+00, 1.2400148e-05,
    #      2.4800295e-06, 2.4800295e-06, 8.2060957e-01, 1.3640162e-04, 1.1408136e-04,
    #      7.4400887e-06, 7.6880919e-05, 2.0088239e-04, 3.6456436e-04, 0.0000000e+00,
    #      0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00,
    #      2.7438931e+05],
    #     [6.2816417e-01, 7.2029911e-02, 1.3951107e-02, 1.1312352e-03, 7.2637206e-04,
    #      3.1436430e-04, 1.7290037e-03, 2.7380893e-01, 4.0010002e-04, 6.4492314e-03,
    #      1.7385298e-04, 6.0015003e-04, 2.7149645e-04, 2.5006253e-04, 0.0000000e+00,
    #      0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00,
    #      2.7211122e+05],
    #     [4.2250833e-01, 1.6166905e-01 ,9.2843613e-03, 8.7717618e-04, 2.1655286e-04,
    #      1.4802348e-04, 7.6752913e-05, 1.9517170e-03, 1.7817640e-04, 3.9954826e-01,
    #      2.1737521e-03, 6.6336448e-04, 5.6742330e-04, 1.3705877e-04, 0.0000000e+00,
    #      0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00,
    #      2.2882162e+05]
    # ])
    print("Learning...")
    centers,names = learn('vision_logos',bins)
    print("Done")
    stains = []
    while True:


        ret, image=cam.read()
        #image = cv2.imread('seniales.png')
        image2 = image
        if(len(stains) == 0):
            stains = np.uint8(np.ones(image.shape))
        else:
            image= stains*image
            #cv2.imshow("Camara", image)

        resized = imutils.resize(image, width=600)

        if(ratio==0):
            ratio = image.shape[0] / float(resized.shape[0])
        blurred = cv2.GaussianBlur(resized, (3, 3), 0)

        edged = cv2.Canny(blurred, 50, 100, 255)
        #cv2.imshow("ss", edged)

        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        for c in cnts:
            M = cv2.moments(c)
            if(M["m00"] == 0):
                continue
            cX = int((M["m10"] / M["m00"]) * ratio)
            cY = int((M["m01"] / M["m00"]) * ratio)

            area = cv2.contourArea(c, False)
            shape = sd.detect(c)
            if (area < 2000):
                continue
            if shape is not "square":
                continue

            hist, stain, selec = getconthist(c,image,bins)
            stains= stains*stain
            #cv2.imshow("stains",imutils.resize(stains, width=600))

            #plt.figure()
            #plt.xlabel("Bins")
            #plt.ylabel("# of Pixels")
            #plt.plot(hist/sum(hist))
            #plt.xlim([0, bins])
            #plt.title("muestra")
            #plt.show()

            #kdata = (hist/sum(hist))
            kdata = np.insert((hist/sum(hist)),len(hist),[entropy(hist,bins)])

            imin =0
            min= 1000000
            i=0

            for x in centers:
                d = distanceE(kdata,x[0])
                #if(not cv2.waitKey(22)):
                    #plt.figure()
                    #plt.xlabel("Bins")
                    #plt.ylabel("# of Pixels")
                    #plt.plot(kdata)
                    #plt.plot(x)
                    #plt.title(names[i])
                    #plt.show()
                if(min>d):
                    min = d
                    imin=i
                i+=1
            if(min<minimError):
                print(names[imin])
                print(min)
                cv2.imshow("Found",selec)
                if(cv2.waitKey(3000)==13):
                    stains = np.ones(image.shape)

        if (cv2.waitKey(20) == 13):
            stains = np.uint8(np.ones(image.shape))





        cv2.imshow("Camara", imutils.resize(image2, width=600))
        #cv2.imshow("Stained Camera", imutils.resize(image, width=600))



