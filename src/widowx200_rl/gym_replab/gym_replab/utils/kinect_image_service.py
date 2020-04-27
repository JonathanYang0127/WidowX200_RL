from sensor_msgs.msg import Image as Image_msg, PointCloud2 as PointCloud2_msg
import sensor_msgs.point_cloud2 as pc2
import rospy
import numpy as np
import skimage
import matplotlib as mpl
mpl.use('Agg') # Stop Matplotlib from expecting DISPLAY
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import Axes3D
from cv_bridge import CvBridge, CvBridgeError
import pcl
import os

import warnings
from sklearn.exceptions import DataConversionWarning

warnings.filterwarnings(action='ignore', category=DataConversionWarning)

rgb_topic = "/kinect2/qhd/image_color"
sd_img_d_topic = "/kinect2/sd/image_depth"
hd_img_dr_topic = "/kinect2/hd/image_depth_rect"
hd_img_drc_topic = "/kinect2/hd/image_depth_rect/compressed"
qhd_img_dr_topic = "/kinect2/qhd/image_depth_rect"
qhd_img_drc_topic = "/kinect2/qhd/image_depth_rect/compressed"
qhd_pts_topic = "/kinect2/qhd/points"
sd_img_dc_topic = "/kinect2/sd/image_depth/compressed"
sd_img_dr_topic = "/kinect2/sd/image_depth_rect"
sd_img_drc_topic = "/kinect2/sd/image_depth_rect/compressed"
sd_img_ir_topic = "/kinect2/sd/image_ir"
sd_img_irc_topic = "/kinect2/sd/image_ir/compressed"
sd_img_ir_r_topic = "/kinect2/sd/image_ir_rect"
sd_img_ir_rc_topic = "/kinect2/sd/image_ir_rect/compressed"
sd_pts_topic = "/kinect2/sd/points"

class KinectImageService(object):
    def __init__(self, image_type="rgb", rgb_image_dim=64):
        self.image_type = image_type
        if self.image_type == "rgb":
            self.image_width = rgb_image_dim
            self.image_height = rgb_image_dim
            self.stream_data_width = 960
            self.stream_data_height = 540
            rostopic = rgb_topic
        elif self.image_type == "depth_qhd_dr":
            self.image_width = 256
            self.image_height = 256
            self.stream_data_width = 960
            self.stream_data_height = 540
            rostopic = qhd_img_dr_topic
        elif self.image_type == "depth_sd_d":
            self.image_width = 256
            self.image_height = 256
            self.stream_data_width = 512
            self.stream_data_height = 424
            rostopic = sd_img_d_topic
        elif self.image_type == "sd_pts":
            rostopic = sd_pts_topic
        else:
            raise NotImplementedError("{} imagetype not supported".format(self.image_type))

        if self.image_type == "rgb":
            image_shape=(self.image_width, self.image_height, 3)
        elif self.image_type in ["depth_qhd_dr", "depth_sd_d"]:
            image_shape=(self.image_width, self.image_height, 2)

        if self.image_type in ["rgb", "depth_qhd_dr", "depth_sd_d"]:
            self.image_shape = image_shape
            self.image = None
        elif self.image_type == "sd_pts":
            self.pc_array = None # np.array
            self.pc = None # pcl.PointCloud_PointXYZRGB

        if self.image_type in ["rgb", "depth_qhd_dr", "depth_sd_d"]:
            msg_type = Image_msg
            store_func = self.store_image
        elif self.image_type == "sd_pts":
            msg_type = PointCloud2_msg
            store_func = self.store_pc
        rospy.Subscriber(
            rostopic,
            msg_type,
            store_func,
            queue_size=1,
            buff_size=2**24,
            tcp_nodelay=True
        )

        connection_attempts = 5
        for i in range(connection_attempts):
            if ((self.image_type in ["rgb", "depth_qhd_dr", "depth_sd_d"] and self.image is not None)
                or (self.image_type == "sd_pts" and self.pc is not None)):
                break
            print("No image found yet.")
            rospy.sleep(1)

        if i == (connection_attempts - 1):
            raise ValueError

    def process_image_rgb(self, image):
        # image = np.flip(image.reshape((1080, 1920, 3)), axis=2)
        # image = image[50:950, 500:1400]

        image = np.flip(image.reshape((self.stream_data_height, self.stream_data_width, 3)), axis=2)
        w = 380
        v_margin = 302
        h = 320
        h_margin = 145
        image = image[h_margin:h_margin + h:, v_margin:v_margin + w]

        # image = image[280:280+260, 400:400+260]

        # image = np.flip(image.reshape((424, 512, 3)), axis=2)
        # image = image[:, 44:-44]

        resize_to = next(
            2 ** i for i in reversed(range(10))
            if 2 ** i < image.shape[0])
        image = skimage.transform.resize(
            image, (resize_to, resize_to), anti_aliasing=True, mode='constant')
        width = image.shape[0] // self.image_shape[0]
        height = image.shape[1] // self.image_shape[1]
        image = skimage.transform.downscale_local_mean(
            image, (width, height, 1))
        image = skimage.util.img_as_ubyte(image)

        return image

    def process_image_d(self, image):
        print("image.dtype in process_image_d", image.dtype)
        assert self.stream_data_width > self.stream_data_height, (
            "stream width: {} is not > height: {}".format(self.stream_data_width, self.stream_data_height))
        image = np.flip(image.reshape((self.stream_data_height, self.stream_data_width, 2)), axis=-1)
        image = np.array(image, dtype=np.uint16) # Convert to uint16 np array so we can slide by 8 bits later.
        image0 = image[:, :, 0] # The "tens place" (more significant bits in the distance).
        image1 = image[:, :, 1] # The "ones place" (less significant bits in the distance)
        image = (image0 << 8) + image1 # The 0th image is the "tens place,"
        # so we slide it over by 8 bits (image is a uint_8). The 1th image is the "ones place."
        image = np.clip(image, 256*2, 256*3.5) # Cleanse image of outliers
        # edge_width_trim = (self.stream_data_width - self.stream_data_height) // 2
        # image = image[:, edge_width_trim : edge_width_trim + self.stream_data_height] # trim width st width == height
        resize_to = next(
            2 ** i for i in reversed(range(10))
            if 2 ** i < image.shape[0])
        # image = skimage.transform.resize(
        #     image, (resize_to, resize_to), anti_aliasing=True, mode='constant')
        # width = image.shape[0] // self.image_shape[0]
        # height = image.shape[1] // self.image_shape[1]
        # image = skimage.transform.downscale_local_mean(
        #     image, (width, height, 1)) ## (width, height, 1))
        # image = skimage.util.img_as_ubyte(image)
        print("process_image_d, image.shape", image.shape)
        return image

    def store_image(self, data):
        # start = rospy.Time.now()

        image = np.frombuffer(data.data, dtype=np.uint8)
        if self.image_type == "rgb":
            image = self.process_image_rgb(image.copy())
        elif self.image_type in ["depth_qhd_dr", "depth_sd_d"]:
            image = self.process_image_d(image.copy())
        self.image = image

        # end = rospy.Time.now()

        # transport_delay = (start - data.header.stamp).to_sec()
        # process_delay = (end - start).to_sec()
        # total_delay = transport_delay + process_delay

        # print(f"Processing frame"
        #       f" | Transport delay:{transport_delay:6.3f}"
        #       f" | Process delay: {process_delay:6.3f}"
        #       f" | Total delay: {total_delay:6.3f}")

    def store_pc(self, data):
        self.pc = pc2.read_points(data, skip_nans=True)

    def get_image(self, *args, **kwargs):
        width = self.image_width
        height = self.image_height
        print("width, height", width, height)
        print("self.image.shape", self.image.shape)
        # if self.image.shape[:2] != (width, height):
        #     old_width, old_height = self.image.shape[:2]
        #     assert old_width >= width and old_height >= height, (
        #         f'{(old_width, old_height)} needs to be >= {(width, height)}')
        #     old_image = self.image.copy()
        #     # skimage requires the image be converted to float first
        #     float_img = skimage.util.img_as_float(old_image)
        #     # print("old_width, old_height", old_width, old_height)
        #     # print("width, height", width, height)
        #     # assert old_width % width == 0 and old_height % height == 0, (
        #     #     "image width and height ({}, {}) should be factors of ({}, {})".format(
        #     #         width, height, old_width, old_height
        #     #     )
        #     # )
        #     width_factor = old_width // width
        #     height_factor = old_height // height
        #     if self.image_type == "rgb":
        #         downsampled = skimage.transform.downscale_local_mean(
        #             float_img, (width_factor, height_factor, 1))
        #     elif self.image_type in ["depth_qhd_dr", "depth_sd_d"]:
        #         downsampled = skimage.transform.downscale_local_mean(
        #             float_img, (width_factor, height_factor))
        #     # Convert back to uint8
        #     downsampled = skimage.util.img_as_ubyte(downsampled)
        #     return downsampled

        # # old_image = self.image.copy()

        # # same_frame = np.all(old_image == self._image)
        # # if same_frame:
        # #     self._same_frame_count += 1
        # # else:
        # #     self._same_frame_count = 0

        # # if self._same_frame_count > 100:
        # assert self.image.shape[:2] == (width, height)
        return self.image

    def get_pc(self, *args, **kwargs):
        pc_iter = self.pc # generator object (iterator)
        self.pc_array = np.array(list(pc_iter), dtype=np.float32)
        self.pc = pcl.PointCloud_PointXYZRGB(self.pc_array)
        return self.pc

    def pull_image(self, i=0, save_images=False):
        if self.image_type in ["rgb", "depth_qhd_dr", "depth_sd_d"]:
            image = self.get_image()
            if image is None:
                print("No pixels received yet")
            else:
                print(image.dtype, image.shape)

            if save_images:
                # print("image[:,450]", image[:,450])
                plt.imsave("image{}.png".format(i), image.copy())
            return image
        elif self.image_type == "sd_pts":
            pc = self.get_pc()
            pc_array = self.pc_array
            if pc is None:
                print("No points received yet")
            else:
                print(pc_array.dtype, pc_array.shape)
            pcl.save_XYZRGBA(pc, "pc{}.pcd".format(i))
            print("pc{}.pcd saved in".format(i), os.path.abspath(os.getcwd()))
            return pc

if __name__ == '__main__':
    rospy.init_node('images_service', anonymous=True)
    try:
        image_service = KinectImageService("sd_pts") # "rgb" or "sd_pts"
        image_service.pull_image()
    except rospy.ROSInterruptException:
        pass
