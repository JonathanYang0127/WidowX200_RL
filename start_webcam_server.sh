roslaunch video_stream_opencv camera.launch video_stream_provider:=0 camera_name:=usb_camera visualize:=False fps:=60 &
rosrun image_server webcam_server.py

