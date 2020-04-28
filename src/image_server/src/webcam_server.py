#!/usr/bin/env python
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image as Image_msg

import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')
import numpy as np
from image_server.srv import image, imageResponse


class USBCamera(object):
    def __init__(self, ):
        self._latest_image = None
        rospy.Subscriber("/usb_camera/image_raw/", Image_msg,
                         self.store_latest_image)
        rospy.init_node('usb_camera_node')

    def store_latest_image(self, image_data, bgr2rgb=True):
        image = CvBridge().imgmsg_to_cv2(image_data)

        # convert BGR to RGB
        image = image.transpose((-1, 0, 1))
        image = image[::-1]
        image = image.transpose(((1, -1, 0)))

        self._latest_image = image

    @property
    def latest_image(self):
        return self._latest_image


def get_image(image_msg):
    image_height = image_msg.image_height
    image_width = image_msg.image_width
    image = np.asarray(usb.latest_image)

    # fit image into square
    h, w, _c = image.shape
    if h < w:
        center_image = np.zeros((w, w, 3))
        sh = int(0.5 * (w - h))
        center_image[sh:sh + h] = image
    else:
        center_image = np.zeros((h, h, 3))
        sw = int(0.5 * (h - w))
        center_image[:, sw:sw + w] = image
    image = cv2.resize(center_image, (image_height, image_width))

    image = image.flatten().tolist()
    return imageResponse(image)


def main():
    s = rospy.Service('images_usb', image, get_image)
    rospy.spin()


if __name__ == "__main__":
    global usb
    usb = USBCamera()
    main()
