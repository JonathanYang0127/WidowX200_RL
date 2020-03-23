; Auto-generated. Do not edit!


(cl:in-package interbotix_joy_control-msg)


;//! \htmlinclude ArmJoyControl.msg.html

(cl:defclass <ArmJoyControl> (roslisp-msg-protocol:ros-message)
  ((ee_x_cmd
    :reader ee_x_cmd
    :initarg :ee_x_cmd
    :type cl:fixnum
    :initform 0)
   (ee_y_cmd
    :reader ee_y_cmd
    :initarg :ee_y_cmd
    :type cl:fixnum
    :initform 0)
   (ee_z_cmd
    :reader ee_z_cmd
    :initarg :ee_z_cmd
    :type cl:fixnum
    :initform 0)
   (ee_roll_cmd
    :reader ee_roll_cmd
    :initarg :ee_roll_cmd
    :type cl:fixnum
    :initform 0)
   (ee_pitch_cmd
    :reader ee_pitch_cmd
    :initarg :ee_pitch_cmd
    :type cl:fixnum
    :initform 0)
   (waist_cmd
    :reader waist_cmd
    :initarg :waist_cmd
    :type cl:fixnum
    :initform 0)
   (gripper_cmd
    :reader gripper_cmd
    :initarg :gripper_cmd
    :type cl:fixnum
    :initform 0)
   (robot_pose
    :reader robot_pose
    :initarg :robot_pose
    :type cl:fixnum
    :initform 0)
   (speed_cmd
    :reader speed_cmd
    :initarg :speed_cmd
    :type cl:fixnum
    :initform 0)
   (toggle_speed_cmd
    :reader toggle_speed_cmd
    :initarg :toggle_speed_cmd
    :type cl:fixnum
    :initform 0)
   (gripper_pwm_cmd
    :reader gripper_pwm_cmd
    :initarg :gripper_pwm_cmd
    :type cl:fixnum
    :initform 0))
)

(cl:defclass ArmJoyControl (<ArmJoyControl>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ArmJoyControl>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ArmJoyControl)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name interbotix_joy_control-msg:<ArmJoyControl> is deprecated: use interbotix_joy_control-msg:ArmJoyControl instead.")))

(cl:ensure-generic-function 'ee_x_cmd-val :lambda-list '(m))
(cl:defmethod ee_x_cmd-val ((m <ArmJoyControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_joy_control-msg:ee_x_cmd-val is deprecated.  Use interbotix_joy_control-msg:ee_x_cmd instead.")
  (ee_x_cmd m))

(cl:ensure-generic-function 'ee_y_cmd-val :lambda-list '(m))
(cl:defmethod ee_y_cmd-val ((m <ArmJoyControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_joy_control-msg:ee_y_cmd-val is deprecated.  Use interbotix_joy_control-msg:ee_y_cmd instead.")
  (ee_y_cmd m))

(cl:ensure-generic-function 'ee_z_cmd-val :lambda-list '(m))
(cl:defmethod ee_z_cmd-val ((m <ArmJoyControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_joy_control-msg:ee_z_cmd-val is deprecated.  Use interbotix_joy_control-msg:ee_z_cmd instead.")
  (ee_z_cmd m))

(cl:ensure-generic-function 'ee_roll_cmd-val :lambda-list '(m))
(cl:defmethod ee_roll_cmd-val ((m <ArmJoyControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_joy_control-msg:ee_roll_cmd-val is deprecated.  Use interbotix_joy_control-msg:ee_roll_cmd instead.")
  (ee_roll_cmd m))

(cl:ensure-generic-function 'ee_pitch_cmd-val :lambda-list '(m))
(cl:defmethod ee_pitch_cmd-val ((m <ArmJoyControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_joy_control-msg:ee_pitch_cmd-val is deprecated.  Use interbotix_joy_control-msg:ee_pitch_cmd instead.")
  (ee_pitch_cmd m))

(cl:ensure-generic-function 'waist_cmd-val :lambda-list '(m))
(cl:defmethod waist_cmd-val ((m <ArmJoyControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_joy_control-msg:waist_cmd-val is deprecated.  Use interbotix_joy_control-msg:waist_cmd instead.")
  (waist_cmd m))

(cl:ensure-generic-function 'gripper_cmd-val :lambda-list '(m))
(cl:defmethod gripper_cmd-val ((m <ArmJoyControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_joy_control-msg:gripper_cmd-val is deprecated.  Use interbotix_joy_control-msg:gripper_cmd instead.")
  (gripper_cmd m))

(cl:ensure-generic-function 'robot_pose-val :lambda-list '(m))
(cl:defmethod robot_pose-val ((m <ArmJoyControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_joy_control-msg:robot_pose-val is deprecated.  Use interbotix_joy_control-msg:robot_pose instead.")
  (robot_pose m))

(cl:ensure-generic-function 'speed_cmd-val :lambda-list '(m))
(cl:defmethod speed_cmd-val ((m <ArmJoyControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_joy_control-msg:speed_cmd-val is deprecated.  Use interbotix_joy_control-msg:speed_cmd instead.")
  (speed_cmd m))

(cl:ensure-generic-function 'toggle_speed_cmd-val :lambda-list '(m))
(cl:defmethod toggle_speed_cmd-val ((m <ArmJoyControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_joy_control-msg:toggle_speed_cmd-val is deprecated.  Use interbotix_joy_control-msg:toggle_speed_cmd instead.")
  (toggle_speed_cmd m))

(cl:ensure-generic-function 'gripper_pwm_cmd-val :lambda-list '(m))
(cl:defmethod gripper_pwm_cmd-val ((m <ArmJoyControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_joy_control-msg:gripper_pwm_cmd-val is deprecated.  Use interbotix_joy_control-msg:gripper_pwm_cmd instead.")
  (gripper_pwm_cmd m))
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql '<ArmJoyControl>)))
    "Constants for message type '<ArmJoyControl>"
  '((:EE_X_INC . 1)
    (:EE_X_DEC . 2)
    (:EE_Y_INC . 3)
    (:EE_Y_DEC . 4)
    (:EE_Z_INC . 5)
    (:EE_Z_DEC . 6)
    (:EE_ROLL_CCW . 7)
    (:EE_ROLL_CW . 8)
    (:EE_PITCH_UP . 9)
    (:EE_PITCH_DOWN . 10)
    (:WAIST_CCW . 11)
    (:WAIST_CW . 12)
    (:GRIPPER_OPEN . 13)
    (:GRIPPER_CLOSE . 14)
    (:HOME_POSE . 15)
    (:SLEEP_POSE . 16)
    (:SPEED_INC . 17)
    (:SPEED_DEC . 18)
    (:SPEED_COURSE . 19)
    (:SPEED_FINE . 20)
    (:GRIPPER_PWM_INC . 21)
    (:GRIPPER_PWM_DEC . 22))
)
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql 'ArmJoyControl)))
    "Constants for message type 'ArmJoyControl"
  '((:EE_X_INC . 1)
    (:EE_X_DEC . 2)
    (:EE_Y_INC . 3)
    (:EE_Y_DEC . 4)
    (:EE_Z_INC . 5)
    (:EE_Z_DEC . 6)
    (:EE_ROLL_CCW . 7)
    (:EE_ROLL_CW . 8)
    (:EE_PITCH_UP . 9)
    (:EE_PITCH_DOWN . 10)
    (:WAIST_CCW . 11)
    (:WAIST_CW . 12)
    (:GRIPPER_OPEN . 13)
    (:GRIPPER_CLOSE . 14)
    (:HOME_POSE . 15)
    (:SLEEP_POSE . 16)
    (:SPEED_INC . 17)
    (:SPEED_DEC . 18)
    (:SPEED_COURSE . 19)
    (:SPEED_FINE . 20)
    (:GRIPPER_PWM_INC . 21)
    (:GRIPPER_PWM_DEC . 22))
)
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ArmJoyControl>) ostream)
  "Serializes a message object of type '<ArmJoyControl>"
  (cl:let* ((signed (cl:slot-value msg 'ee_x_cmd)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'ee_y_cmd)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'ee_z_cmd)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'ee_roll_cmd)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'ee_pitch_cmd)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'waist_cmd)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'gripper_cmd)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'robot_pose)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'speed_cmd)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'toggle_speed_cmd)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'gripper_pwm_cmd)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ArmJoyControl>) istream)
  "Deserializes a message object of type '<ArmJoyControl>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'ee_x_cmd) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'ee_y_cmd) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'ee_z_cmd) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'ee_roll_cmd) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'ee_pitch_cmd) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'waist_cmd) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'gripper_cmd) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'robot_pose) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'speed_cmd) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'toggle_speed_cmd) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'gripper_pwm_cmd) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ArmJoyControl>)))
  "Returns string type for a message object of type '<ArmJoyControl>"
  "interbotix_joy_control/ArmJoyControl")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ArmJoyControl)))
  "Returns string type for a message object of type 'ArmJoyControl"
  "interbotix_joy_control/ArmJoyControl")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ArmJoyControl>)))
  "Returns md5sum for a message object of type '<ArmJoyControl>"
  "74891567b0665aa1963bdc439b948bf5")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ArmJoyControl)))
  "Returns md5sum for a message object of type 'ArmJoyControl"
  "74891567b0665aa1963bdc439b948bf5")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ArmJoyControl>)))
  "Returns full string definition for message of type '<ArmJoyControl>"
  (cl:format cl:nil "# Send commands from the joy_control node to the joy_robot_control node~%~%# enum values that define the joystick controls for the robot~%~%#########################################################################################################~%~%# Control the motion of the virtual 'ee_gripper_link' or end effector using the modern_robotics_ik engine~%# Position Control~%int8 EE_X_INC = 1~%int8 EE_X_DEC = 2~%int8 EE_Y_INC = 3~%int8 EE_Y_DEC = 4~%int8 EE_Z_INC = 5~%int8 EE_Z_DEC = 6~%~%# Orientation Control~%int8 EE_ROLL_CCW = 7~%int8 EE_ROLL_CW = 8~%int8 EE_PITCH_UP = 9~%int8 EE_PITCH_DOWN = 10~%~%#########################################################################################################~%~%# Control the motion of independent joints on the Arm or send predefined robot poses~%# Waist Joint Control~%int8 WAIST_CCW = 11~%int8 WAIST_CW = 12~%~%# Gripper Control~%int8 GRIPPER_OPEN = 13~%int8 GRIPPER_CLOSE = 14~%~%# Pose Control~%int8 HOME_POSE = 15~%int8 SLEEP_POSE = 16~%~%#########################################################################################################~%~%# Customize configurations for the Interbotix Arm~%# Inc/Dec Joint speed~%int8 SPEED_INC = 17~%int8 SPEED_DEC = 18~%~%# Quickly toggle between a fast and slow speed setting~%int8 SPEED_COURSE = 19~%int8 SPEED_FINE = 20~%~%# Inc/Dec Gripper pressure~%int8 GRIPPER_PWM_INC = 21~%int8 GRIPPER_PWM_DEC = 22~%~%#########################################################################################################~%~%# Control the motion of the Interbotix Arm~%int8 ee_x_cmd~%int8 ee_y_cmd~%int8 ee_z_cmd~%int8 ee_roll_cmd~%int8 ee_pitch_cmd~%~%# Independent Joint/Pose Control~%int8 waist_cmd~%int8 gripper_cmd~%int8 robot_pose~%~%# Speed Configs~%int8 speed_cmd~%int8 toggle_speed_cmd~%int8 gripper_pwm_cmd~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ArmJoyControl)))
  "Returns full string definition for message of type 'ArmJoyControl"
  (cl:format cl:nil "# Send commands from the joy_control node to the joy_robot_control node~%~%# enum values that define the joystick controls for the robot~%~%#########################################################################################################~%~%# Control the motion of the virtual 'ee_gripper_link' or end effector using the modern_robotics_ik engine~%# Position Control~%int8 EE_X_INC = 1~%int8 EE_X_DEC = 2~%int8 EE_Y_INC = 3~%int8 EE_Y_DEC = 4~%int8 EE_Z_INC = 5~%int8 EE_Z_DEC = 6~%~%# Orientation Control~%int8 EE_ROLL_CCW = 7~%int8 EE_ROLL_CW = 8~%int8 EE_PITCH_UP = 9~%int8 EE_PITCH_DOWN = 10~%~%#########################################################################################################~%~%# Control the motion of independent joints on the Arm or send predefined robot poses~%# Waist Joint Control~%int8 WAIST_CCW = 11~%int8 WAIST_CW = 12~%~%# Gripper Control~%int8 GRIPPER_OPEN = 13~%int8 GRIPPER_CLOSE = 14~%~%# Pose Control~%int8 HOME_POSE = 15~%int8 SLEEP_POSE = 16~%~%#########################################################################################################~%~%# Customize configurations for the Interbotix Arm~%# Inc/Dec Joint speed~%int8 SPEED_INC = 17~%int8 SPEED_DEC = 18~%~%# Quickly toggle between a fast and slow speed setting~%int8 SPEED_COURSE = 19~%int8 SPEED_FINE = 20~%~%# Inc/Dec Gripper pressure~%int8 GRIPPER_PWM_INC = 21~%int8 GRIPPER_PWM_DEC = 22~%~%#########################################################################################################~%~%# Control the motion of the Interbotix Arm~%int8 ee_x_cmd~%int8 ee_y_cmd~%int8 ee_z_cmd~%int8 ee_roll_cmd~%int8 ee_pitch_cmd~%~%# Independent Joint/Pose Control~%int8 waist_cmd~%int8 gripper_cmd~%int8 robot_pose~%~%# Speed Configs~%int8 speed_cmd~%int8 toggle_speed_cmd~%int8 gripper_pwm_cmd~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ArmJoyControl>))
  (cl:+ 0
     1
     1
     1
     1
     1
     1
     1
     1
     1
     1
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ArmJoyControl>))
  "Converts a ROS message object to a list"
  (cl:list 'ArmJoyControl
    (cl:cons ':ee_x_cmd (ee_x_cmd msg))
    (cl:cons ':ee_y_cmd (ee_y_cmd msg))
    (cl:cons ':ee_z_cmd (ee_z_cmd msg))
    (cl:cons ':ee_roll_cmd (ee_roll_cmd msg))
    (cl:cons ':ee_pitch_cmd (ee_pitch_cmd msg))
    (cl:cons ':waist_cmd (waist_cmd msg))
    (cl:cons ':gripper_cmd (gripper_cmd msg))
    (cl:cons ':robot_pose (robot_pose msg))
    (cl:cons ':speed_cmd (speed_cmd msg))
    (cl:cons ':toggle_speed_cmd (toggle_speed_cmd msg))
    (cl:cons ':gripper_pwm_cmd (gripper_pwm_cmd msg))
))
