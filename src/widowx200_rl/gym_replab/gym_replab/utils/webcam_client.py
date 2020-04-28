import argparse

import rospy
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')
import numpy as np
from image_server.srv import image as Image


def get_image(height, width):
    rospy.wait_for_service('images_usb')
    try:
        request_image = rospy.ServiceProxy(
            'images_usb', Image, persistent=True)
        response = request_image(height, width)
        image = response.image
        image = np.asarray(image).reshape((height, width, 3)).astype('uint8')
        return image
    except rospy.ServiceException as e:
        print(e)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--height', type=int, default=84)
    parser.add_argument('--width', type=int, default=84)
    return parser.parse_args()


def main(args):
    image = get_image(args.height, args.width)
    print('image shape: {}'.format(image.shape))
    print('maximum value: {}'.format(np.max(image)))
    print('minimum value: {}'.format(np.min(image)))
    cv2.imwrite('picture0.png', image)


if __name__ == '__main__':
    main(parse_args())
