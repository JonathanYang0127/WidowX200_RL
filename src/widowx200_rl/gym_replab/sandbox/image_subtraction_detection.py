#Workaround for importing opencv2 with ros
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')
import numpy as np
from scipy.cluster.vq import vq, kmeans, whiten
from gym_replab.utils import background_subtraction


image1 = cv2.imread("/home/jonathan/Desktop/Projects/image1.png")
image0 = cv2.imread("/home/jonathan/Desktop/image0.png")


def downsample_average(image, num_pixels=4):
    new_image = np.copy(image)
    height, width = image.shape

    for i in range(num_pixels, height - num_pixels):
        for j in range(num_pixels, width - num_pixels):
            new_image[i][j] = np.mean(image[i - num_pixels:i+num_pixels, \
                j-num_pixels:j+num_pixels])

    cv2.imshow("Averaged", new_image)
    return new_image


def extract_points(image, stride=4, threshold=50):
    height, width = image.shape
    new_image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
    count = 0
    points = []

    for i in range(0, height, stride):
        for j in range(0, width, stride):
            if image[i][j] > threshold:
                new_image = cv2.circle(new_image, (j, i), radius=1, color=(0, 0, 255), thickness=1)
                points.append([i, j])
    cv2.imshow("Extracted points", new_image)
    return np.array(points, dtype='float')


def k_means(points, num_objects):
    centroids, _ = kmeans(points, num_objects)
    return centroids


def plot_centroids(image, centroids):
    new_image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
    for centroid in centroids:
        new_image = cv2.circle(new_image, (int(centroid[1]), int(centroid[0])), radius=1, color=(0, 0, 255), thickness=1)

    cv2.imshow("Centroids", new_image)


img, canvas = background_subtraction(image0, image1, False)
cv2.imshow("Images", np.hstack((image0, image1, img)))
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(img.shape)
img = downsample_average(img)
points = extract_points(img, 4, 50)
centroids = k_means(points, 1)
plot_centroids(img, centroids)
cv2.waitKey(0)
