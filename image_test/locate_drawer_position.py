import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')
import numpy as np


img = cv2.imread("/home/jonathan/Desktop/Projects/image0.png")

for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        if np.linalg.norm(img[i][j]) < 75:
            img[i][j] = [255, 255, 255]
        else:
            img[i][j] = [0, 0, 0]

cv2.imwrite("/home/jonathan/Desktop/Projects/handle_filtered.png", img[:200, 100:300])
cv2.waitKey(0)
