import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')
import numpy as np


img = cv2.imread("rgbdiff.png", cv2.IMREAD_GRAYSCALE)


params = cv2.SimpleBlobDetector_Params()
params.filterByColor = False
params.filterByArea = True
params.filterByCircularity = False
params.filterByInertia = True
params.filterByConvexity = False
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3 :
    detector = cv2.SimpleBlobDetector(params)
else :
    detector = cv2.SimpleBlobDetector_create(params)

detector.empty()
keypoints = detector.detect(img)
print(keypoints)
img_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow("Keypoints", img_with_keypoints)
cv2.waitKey(0)
