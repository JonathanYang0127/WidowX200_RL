#Workaround for importing opencv2 with ros
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')
import numpy as np
from scipy.cluster.vq import vq, kmeans, whiten
from .background_subtraction import background_subtraction
import os
from sklearn.preprocessing import PolynomialFeatures

'''
RGB_TO_ROBOT_TRANSMATRIX = [[ 1.31473611e-01, -2.80861098e-01],
 [ 1.28848446e-03,  4.03900671e-06],
 [-1.46187436e-05,  9.14655889e-04]]
'''

RGB_TO_ROBOT_TRANSMATRIX = [[ 1.07112906e-01, -3.37877220e-01],
 [ 2.18106984e-03,  5.81023424e-04],
 [-5.17897443e-05,  1.15085881e-03],
 [-5.18807412e-06, -6.94702605e-07],
 [ 1.08736536e-07, -1.58696406e-06],
 [ 5.42560104e-08, -1.46107167e-07]]


def downsample_average(image, num_pixels=4, save_dir=""):
    new_image = np.copy(image)
    height, width = image.shape

    for i in range(num_pixels, height - num_pixels):
        for j in range(num_pixels, width - num_pixels):
            new_image[i][j] = np.mean(image[i - num_pixels:i+num_pixels, \
                j-num_pixels:j+num_pixels])

    if save_dir != "":
        cv2.imwrite(os.path.dirname(save_dir) + '/averaged.png', new_image)
    return new_image


def extract_points(image, stride=4, threshold=50, save_dir=""):
    height, width = image.shape
    new_image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
    count = 0
    points = []

    for i in range(0, height, stride):
        for j in range(0, width, stride):
            if image[i][j] > threshold:
                new_image = cv2.circle(new_image, (j, i), radius=1, color=(0, 0, 255), thickness=1)
                points.append([i, j])

    if save_dir != "":
        cv2.imwrite(os.path.dirname(save_dir) + '/extracted.png', new_image)
    return np.array(points, dtype='float')


def k_means(points, num_objects):
    centroids, _ = kmeans(points, num_objects)
    return centroids


def plot_centroids(image, centroids, save_dir):
    new_image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
    for centroid in centroids:
        new_image = cv2.circle(new_image, (int(centroid[1]), int(centroid[0])), radius=1, color=(0, 0, 255), thickness=1)

    cv2.imwrite(os.path.dirname(save_dir) + '/centroids.png', new_image)


def get_rgb_centroids(image0, image1, num_centroids=1, save_dir=""):
    img, canvas = background_subtraction(image0, image1, False)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = downsample_average(img, save_dir=save_dir)
    points = extract_points(img, 6, 50, save_dir=save_dir)
    centroids = k_means(points, num_centroids)
    if save_dir != "":
        plot_centroids(img, centroids, save_dir)

    return centroids


def rgb_to_robot_coords(rgb_coords, transmatrix=RGB_TO_ROBOT_TRANSMATRIX):
    # add vector of 1s as feature to the pc_coords.
    assert len(rgb_coords.shape) == 2
    poly = PolynomialFeatures(2)
    rgb_coords = poly.fit_transform(rgb_coords)

    robot_coords = rgb_coords @ transmatrix
    return robot_coords
