import gym_replab
import numpy as np
import rospy
from scipy import ndimage
import os
ros_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'
if ros_path in os.sys.path:
    os.sys.path.remove(ros_path)
import cv2
os.sys.path.append(ros_path)

MASK_DIFF_THRESH = 15
MIN_PIXEL_DIFF_THRESH = 0.0065 # for far-away objects. Will be scaled up for closer objects.
CANVAS_DIFF_THRESH = 200 # some value between [0, 255]
MAX_BYTE_VAL = 255
# This threshold is scaled up depending on
# how close the object is to the camera.
# % change in canvas grayscale pixel difference
# from a black canvas after normalizing

def get_curr_image(rgb_image_service):
    return gym_replab.utils.get_rgb_image(rgb_image_service)

def background_subtraction(image0, image1, save_image=False):
    cv2.imwrite("image0.png", image0)
    cv2.imwrite("image1.png", image1)
    diff = cv2.absdiff(image1, image0)
    print(diff.shape)
    mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    print("mask.shape", mask.shape)
    imask = mask > MASK_DIFF_THRESH

    canvas = np.zeros_like(image1, np.uint8)
    canvas[imask] = image1[imask]
    canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    # Canvas is grayscale. Convert to black (0) and white (255) values only.
    canvas = MAX_BYTE_VAL * (canvas > CANVAS_DIFF_THRESH)
    print("canvas", canvas)

    if save_image:
        cv2.imwrite("rgbdiff.png", diff)
        cv2.imwrite("diff.png", canvas)
    return diff, canvas

def is_object_missing(canvas):
    image_area = canvas.shape[0] * canvas.shape[1]
    change_in_canvas = np.sum(canvas) / (image_area * MAX_BYTE_VAL)
    print("change_in_canvas", change_in_canvas)

    if change_in_canvas == 0:
        return False

    # Do rescaling here. Detect object midpoint.
    x_cm, y_cm = ndimage.measurements.center_of_mass(canvas)
    # x_cm, y_cm are the center of mass coordinates on the canvas.canvas
    # x_cm is the "y"-coordinate on the image.
    # x_cm is higher for lower position on the image (closer to the camera)
    # x_cm ranges from 30 (far) to 190 (close).
    # We will use a normalized range of 0 (far) to 1 (close).
    x_cm_norm = x_cm / canvas.shape[0] # force center of mass between 0 and 1
    print("x_cm_norm", x_cm_norm)
    adjusted_pixel_diff_thresh = MIN_PIXEL_DIFF_THRESH * (1 + x_cm_norm)
    print("adjusted_pixel_diff_thresh", adjusted_pixel_diff_thresh)
    # If midpoint is high, lower PIXEL_DIFF_THRESH.
    return change_in_canvas > adjusted_pixel_diff_thresh


def apply_blob_detection(img, save_image = False):
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
    if save_image:
        img_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imwrite("keypoints.png", img_with_keypoints)
    if len(keypoints) == 1 and keypoints[0].size < 10:
        return False
    return len(keypoints) == 1


def grasp_success_blob_detector(image0, image1, save_image=False):
    diff, canvas = background_subtraction(image0, image1, save_image)
    return apply_blob_detection(diff, save_image)


def grasp_success(image0, image1, save_image=False):
    diff, canvas = background_subtraction(image0, image1, save_image)
    return is_object_missing(canvas)

if __name__ == "__main__":
    rospy.init_node('images_service', anonymous=True)
    rgb_image_service = gym_replab.utils.KinectImageService("rgb", 256)
    i0 = get_curr_image(rgb_image_service)
    input("Press Enter to continue...")
    i1 = get_curr_image(rgb_image_service)
    print("Was it a Picking Success?", grasp_success(i0, i1))
