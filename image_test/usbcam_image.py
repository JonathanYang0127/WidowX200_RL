import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')
import time


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


if __name__ == "__main__":
    count = 0
    while True:
        pull_image(0, 'randompicture_{}.png'.format(count))
        time.sleep(1)
        count += 1
    #stream_image()
    #time.sleep(10)
