import numpy as np
import skimage.transform
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')
import time

RAW_IMAGE_HEIGHT = 480
RAW_IMAGE_WIDTH = 640
L_MARGIN = 50
R_MARGIN = (RAW_IMAGE_WIDTH - RAW_IMAGE_HEIGHT) - L_MARGIN

def stream_image(camport=0):
    cap = cv2.VideoCapture(camport)
    assert cap.isOpened(), "/dev/video{} is not opened.".format(camport)
    
    while True:
        ret, frame = cap.read()
        cv2.imshow('video', frame)
#        time.sleep(0.01)
        break


def pull_image(camport=0, image_name=None):
    cap = cv2.VideoCapture(camport)
    assert cap.isOpened(), "/dev/video{} is not opened.".format(camport)
    ret, frame = cap.read()
    if image_name:
        assert image_name[-4:] in [".jpg", ".png"], "Invalid image_name {}".format(image_name)
        cv2.imwrite(image_name, frame)
    return frame

def process_image_rgb(image, desired_h=64, desired_w=64):
    # Currently only supporting downsampling to square, 2**i x 2**i image.
    assert desired_h == desired_w, \
        "desired_h: {} should equal desired_w: {}".format(desired_h, desired_w)
    assert desired_h == int(2 ** np.round(np.log2(desired_h))), "desired_h {} not a power of 2".format(desired_h)
    assert desired_w == int(2 ** np.round(np.log2(desired_w))), "desired_w {} not a power of 2".format(desired_w)

    # flip upside-down (0), then leftside-right (1)
    image = np.flip(image, axis=(0,1))
    h, w, _ = image.shape
    assert h == RAW_IMAGE_HEIGHT and w == RAW_IMAGE_WIDTH, \
        "Dimensions {}, {} do not match expected raw image dimensions {}, {}".format(
            h, RAW_IMAGE_HEIGHT, w, RAW_IMAGE_WIDTH
        )

    # Crop left and right.
    image = image[:,L_MARGIN : RAW_IMAGE_WIDTH - R_MARGIN]

    # Resize square image to a power of 2.
    resize_to = next(
        2 ** i for i in reversed(range(10))
        if 2 ** i < image.shape[0])
    image = skimage.transform.resize(
        image, (resize_to, resize_to), anti_aliasing=True, mode='constant')

    # Downsample 2**i x 2**i dimensioned square image.
    height_factor = image.shape[0] // desired_h
    width_factor = image.shape[1] // desired_w
    image = skimage.transform.downscale_local_mean(
        image, (width_factor, height_factor, 1))
    image = skimage.util.img_as_ubyte(image)

    return image

if __name__ == "__main__":
    count = 0
    while True:
        frame = pull_image(0, 'randompicture_{}.png'.format(count))
        frame = process_image_rgb(frame, 64, 64)
        cv2.imwrite("randompicture_{}_processed.png".format(count), frame)
        print("frame.shape", frame.shape)
        time.sleep(1)
        count += 1
        break
    #stream_image()
    #time.sleep(10)
