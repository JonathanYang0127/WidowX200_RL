;; Auto-generated. Do not edit!


(when (boundp 'interbotix_sdk::SingleCommand)
  (if (not (find-package "INTERBOTIX_SDK"))
    (make-package "INTERBOTIX_SDK"))
  (shadow 'SingleCommand (find-package "INTERBOTIX_SDK")))
(unless (find-package "INTERBOTIX_SDK::SINGLECOMMAND")
  (make-package "INTERBOTIX_SDK::SINGLECOMMAND"))

(in-package "ROS")
;;//! \htmlinclude SingleCommand.msg.html


(defclass interbotix_sdk::SingleCommand
  :super ros::object
  :slots (_joint_name _cmd ))

(defmethod interbotix_sdk::SingleCommand
  (:init
   (&key
    ((:joint_name __joint_name) "")
    ((:cmd __cmd) 0.0)
    )
   (send-super :init)
   (setq _joint_name (string __joint_name))
   (setq _cmd (float __cmd))
   self)
  (:joint_name
   (&optional __joint_name)
   (if __joint_name (setq _joint_name __joint_name)) _joint_name)
  (:cmd
   (&optional __cmd)
   (if __cmd (setq _cmd __cmd)) _cmd)
  (:serialization-length
   ()
   (+
    ;; string _joint_name
    4 (length _joint_name)
    ;; float64 _cmd
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _joint_name
       (write-long (length _joint_name) s) (princ _joint_name s)
     ;; float64 _cmd
       (sys::poke _cmd (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _joint_name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _joint_name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; float64 _cmd
     (setq _cmd (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get interbotix_sdk::SingleCommand :md5sum-) "6d45868a3dac16da3c97708e8cdbf2c6")
(setf (get interbotix_sdk::SingleCommand :datatype-) "interbotix_sdk/SingleCommand")
(setf (get interbotix_sdk::SingleCommand :definition-)
      "# Send a command to the specified joint
#
# 'joint_name' is the name of the joint to control (any of the motor names listed
# in the 'order' or 'singles' lists located in a motor config file - except for shadow motors)
# 'cmd' can be a position [rad], velocity [rad/s], current [mA], or pwm depending on what operating
# mode the joint is currently set at.
#
# Note that the gripper can be controlled by publishing this type of message to the
# /<robot_name>/single_joint/command topic as well. There are two main differences between using
# this topic and the /<robot_name>/gripper/command topic for controlling the gripper:
#   1) By publishing to the /<robot_name>/gripper/command topic, you do not have to specify that you
#      are commanding the gripper - it's automatically understood.
#   2) When the gripper is in \"position\" control, using the /<robot_name>/gripper/command topic specifies a
#      linear distance in meters between the gripper fingers. However, using the /<robot_name>/single_joint/command
#      topic specifies an angular distance in radians.

string joint_name
float64 cmd

")



(provide :interbotix_sdk/SingleCommand "6d45868a3dac16da3c97708e8cdbf2c6")


