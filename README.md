# WidowX200 RL

## Installation
The WidowX200 RL is built on top of IAI Kinect 2, video_stream_opencv, and Interbotix ROS Arms.

###Setting up the Kinect
First install libfreenect2 to by following the instructions in:
https://github.com/OpenKinect/libfreenect2

To test that the Kinect is working try the following commands:
```bash
cd libfreenect2
./build/bin/Protonect
```
If this works, then there should be a GUI with 4 split screens showing different camera readings.
Next, to get the Kinect working with ROS, clone iai_kinect to into src:
https://github.com/code-iai/iai_kinect2

###Setting up the USB camera
Clone the video_stream_opencv repository into WidowX200_RL/src:
https://github.com/ros-drivers/video_stream_opencv

###Setting up the Interbotix Commander
Clone the Interbotix ROS Arms repository into WidowX200_RL/src:
https://github.com/Interbotix/interbotix_ros_arms

After finishing the above steps, run
```bash
catkin_make
```

## Connecting to the WidowX200
To verify that the WidowX200 is running and to debug issues, install Dynamixel Wizard:
https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/

Go to setting and make sure:
1. Protocol 1 and 2 are selected
2. ttyUSB is selected
3. All baud rates are selected

Then, press scan. If this works, then you should see 7 motors connected

## Overview of the Repository
### Packages
In addition to the packages installed above, this repository features three more packages:
1. image_server
This package stores the pictures taken from a USB camera in a server such that they can be made available in real time to the rl environment.
2. widowx200_core
This package holds the controllers for the widowx200 robot. The main controller is in widowx_controller.py
3. widowx200_rl
This package contains the reinforcement learning environments and a joint subscriber which listens for commands given by the environment and relays the information to the robot.


### Running the Robot
Make sure you have at least 5 command prompt panes available. In each pane, run source devel/setup.bash.
Then, run the following commands:
```bash
sh start.sh
roslaunch kinect2_bridge kinect_2 bridge.launch
sh start_webcam_server.sh
rosrun widowx200_rl widowx200_joint_subscriber.py
rosrun widowx200_core gripper_monitor.py
```

### Callibrating the Kinect
Callibrating the Kinect requires fine-tuning gym_replab/utils/color_pc_clusters.py parameters such that the only the objects in the tray are detected. Afterwards, run the script callibrate_camera.py, and place an object down at 9 locations inside the tray to find a linear mapping between the kinect camera coordinates and the robot coordinates
