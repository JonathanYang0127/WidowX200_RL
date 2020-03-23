; Auto-generated. Do not edit!


(cl:in-package interbotix_sdk-msg)


;//! \htmlinclude SingleCommand.msg.html

(cl:defclass <SingleCommand> (roslisp-msg-protocol:ros-message)
  ((joint_name
    :reader joint_name
    :initarg :joint_name
    :type cl:string
    :initform "")
   (cmd
    :reader cmd
    :initarg :cmd
    :type cl:float
    :initform 0.0))
)

(cl:defclass SingleCommand (<SingleCommand>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SingleCommand>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SingleCommand)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name interbotix_sdk-msg:<SingleCommand> is deprecated: use interbotix_sdk-msg:SingleCommand instead.")))

(cl:ensure-generic-function 'joint_name-val :lambda-list '(m))
(cl:defmethod joint_name-val ((m <SingleCommand>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_sdk-msg:joint_name-val is deprecated.  Use interbotix_sdk-msg:joint_name instead.")
  (joint_name m))

(cl:ensure-generic-function 'cmd-val :lambda-list '(m))
(cl:defmethod cmd-val ((m <SingleCommand>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_sdk-msg:cmd-val is deprecated.  Use interbotix_sdk-msg:cmd instead.")
  (cmd m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SingleCommand>) ostream)
  "Serializes a message object of type '<SingleCommand>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'joint_name))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'joint_name))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'cmd))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SingleCommand>) istream)
  "Deserializes a message object of type '<SingleCommand>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'joint_name) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'joint_name) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'cmd) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SingleCommand>)))
  "Returns string type for a message object of type '<SingleCommand>"
  "interbotix_sdk/SingleCommand")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SingleCommand)))
  "Returns string type for a message object of type 'SingleCommand"
  "interbotix_sdk/SingleCommand")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SingleCommand>)))
  "Returns md5sum for a message object of type '<SingleCommand>"
  "6d45868a3dac16da3c97708e8cdbf2c6")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SingleCommand)))
  "Returns md5sum for a message object of type 'SingleCommand"
  "6d45868a3dac16da3c97708e8cdbf2c6")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SingleCommand>)))
  "Returns full string definition for message of type '<SingleCommand>"
  (cl:format cl:nil "# Send a command to the specified joint~%#~%# 'joint_name' is the name of the joint to control (any of the motor names listed~%# in the 'order' or 'singles' lists located in a motor config file - except for shadow motors)~%# 'cmd' can be a position [rad], velocity [rad/s], current [mA], or pwm depending on what operating~%# mode the joint is currently set at.~%#~%# Note that the gripper can be controlled by publishing this type of message to the~%# /<robot_name>/single_joint/command topic as well. There are two main differences between using~%# this topic and the /<robot_name>/gripper/command topic for controlling the gripper:~%#   1) By publishing to the /<robot_name>/gripper/command topic, you do not have to specify that you~%#      are commanding the gripper - it's automatically understood.~%#   2) When the gripper is in \"position\" control, using the /<robot_name>/gripper/command topic specifies a~%#      linear distance in meters between the gripper fingers. However, using the /<robot_name>/single_joint/command~%#      topic specifies an angular distance in radians.~%~%string joint_name~%float64 cmd~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SingleCommand)))
  "Returns full string definition for message of type 'SingleCommand"
  (cl:format cl:nil "# Send a command to the specified joint~%#~%# 'joint_name' is the name of the joint to control (any of the motor names listed~%# in the 'order' or 'singles' lists located in a motor config file - except for shadow motors)~%# 'cmd' can be a position [rad], velocity [rad/s], current [mA], or pwm depending on what operating~%# mode the joint is currently set at.~%#~%# Note that the gripper can be controlled by publishing this type of message to the~%# /<robot_name>/single_joint/command topic as well. There are two main differences between using~%# this topic and the /<robot_name>/gripper/command topic for controlling the gripper:~%#   1) By publishing to the /<robot_name>/gripper/command topic, you do not have to specify that you~%#      are commanding the gripper - it's automatically understood.~%#   2) When the gripper is in \"position\" control, using the /<robot_name>/gripper/command topic specifies a~%#      linear distance in meters between the gripper fingers. However, using the /<robot_name>/single_joint/command~%#      topic specifies an angular distance in radians.~%~%string joint_name~%float64 cmd~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SingleCommand>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'joint_name))
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SingleCommand>))
  "Converts a ROS message object to a list"
  (cl:list 'SingleCommand
    (cl:cons ':joint_name (joint_name msg))
    (cl:cons ':cmd (cmd msg))
))
