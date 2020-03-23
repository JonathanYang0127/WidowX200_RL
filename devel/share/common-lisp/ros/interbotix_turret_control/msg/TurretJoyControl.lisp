; Auto-generated. Do not edit!


(cl:in-package interbotix_turret_control-msg)


;//! \htmlinclude TurretJoyControl.msg.html

(cl:defclass <TurretJoyControl> (roslisp-msg-protocol:ros-message)
  ((pan_cmd
    :reader pan_cmd
    :initarg :pan_cmd
    :type cl:fixnum
    :initform 0)
   (tilt_cmd
    :reader tilt_cmd
    :initarg :tilt_cmd
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
    :initform 0))
)

(cl:defclass TurretJoyControl (<TurretJoyControl>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <TurretJoyControl>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'TurretJoyControl)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name interbotix_turret_control-msg:<TurretJoyControl> is deprecated: use interbotix_turret_control-msg:TurretJoyControl instead.")))

(cl:ensure-generic-function 'pan_cmd-val :lambda-list '(m))
(cl:defmethod pan_cmd-val ((m <TurretJoyControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_turret_control-msg:pan_cmd-val is deprecated.  Use interbotix_turret_control-msg:pan_cmd instead.")
  (pan_cmd m))

(cl:ensure-generic-function 'tilt_cmd-val :lambda-list '(m))
(cl:defmethod tilt_cmd-val ((m <TurretJoyControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_turret_control-msg:tilt_cmd-val is deprecated.  Use interbotix_turret_control-msg:tilt_cmd instead.")
  (tilt_cmd m))

(cl:ensure-generic-function 'speed_cmd-val :lambda-list '(m))
(cl:defmethod speed_cmd-val ((m <TurretJoyControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_turret_control-msg:speed_cmd-val is deprecated.  Use interbotix_turret_control-msg:speed_cmd instead.")
  (speed_cmd m))

(cl:ensure-generic-function 'toggle_speed_cmd-val :lambda-list '(m))
(cl:defmethod toggle_speed_cmd-val ((m <TurretJoyControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_turret_control-msg:toggle_speed_cmd-val is deprecated.  Use interbotix_turret_control-msg:toggle_speed_cmd instead.")
  (toggle_speed_cmd m))
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql '<TurretJoyControl>)))
    "Constants for message type '<TurretJoyControl>"
  '((:PAN_CCW . 1)
    (:PAN_CW . 2)
    (:TILT_UP . 3)
    (:TILT_DOWN . 4)
    (:PAN_TILT_HOME . 5)
    (:SPEED_INC . 6)
    (:SPEED_DEC . 7)
    (:SPEED_COURSE . 8)
    (:SPEED_FINE . 9))
)
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql 'TurretJoyControl)))
    "Constants for message type 'TurretJoyControl"
  '((:PAN_CCW . 1)
    (:PAN_CW . 2)
    (:TILT_UP . 3)
    (:TILT_DOWN . 4)
    (:PAN_TILT_HOME . 5)
    (:SPEED_INC . 6)
    (:SPEED_DEC . 7)
    (:SPEED_COURSE . 8)
    (:SPEED_FINE . 9))
)
(cl:defmethod roslisp-msg-protocol:serialize ((msg <TurretJoyControl>) ostream)
  "Serializes a message object of type '<TurretJoyControl>"
  (cl:let* ((signed (cl:slot-value msg 'pan_cmd)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'tilt_cmd)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'speed_cmd)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'toggle_speed_cmd)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <TurretJoyControl>) istream)
  "Deserializes a message object of type '<TurretJoyControl>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'pan_cmd) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'tilt_cmd) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'speed_cmd) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'toggle_speed_cmd) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<TurretJoyControl>)))
  "Returns string type for a message object of type '<TurretJoyControl>"
  "interbotix_turret_control/TurretJoyControl")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'TurretJoyControl)))
  "Returns string type for a message object of type 'TurretJoyControl"
  "interbotix_turret_control/TurretJoyControl")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<TurretJoyControl>)))
  "Returns md5sum for a message object of type '<TurretJoyControl>"
  "f699b95ec0a0298bd77c4a4d7f52404f")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'TurretJoyControl)))
  "Returns md5sum for a message object of type 'TurretJoyControl"
  "f699b95ec0a0298bd77c4a4d7f52404f")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<TurretJoyControl>)))
  "Returns full string definition for message of type '<TurretJoyControl>"
  (cl:format cl:nil "# Send commands from the joy_node to the turret_control node~%~%# enum values that define the joystick controls for the robot~%~%#########################################################################################################~%~%# Control the pan-and-tilt mechanism~%int8 PAN_CCW = 1~%int8 PAN_CW = 2~%int8 TILT_UP = 3~%int8 TILT_DOWN = 4~%int8 PAN_TILT_HOME = 5~%~%#########################################################################################################~%~%# Customize configurations for the Interbotix Turret~%# Inc/Dec Joint speed~%int8 SPEED_INC = 6~%int8 SPEED_DEC = 7~%~%# Quickly toggle between a fast and slow speed setting~%int8 SPEED_COURSE = 8~%int8 SPEED_FINE = 9~%~%#########################################################################################################~%~%# Control the motion of the pan-and-tilt mechanism~%int8 pan_cmd~%int8 tilt_cmd~%~%# Speed Configs~%int8 speed_cmd~%int8 toggle_speed_cmd~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'TurretJoyControl)))
  "Returns full string definition for message of type 'TurretJoyControl"
  (cl:format cl:nil "# Send commands from the joy_node to the turret_control node~%~%# enum values that define the joystick controls for the robot~%~%#########################################################################################################~%~%# Control the pan-and-tilt mechanism~%int8 PAN_CCW = 1~%int8 PAN_CW = 2~%int8 TILT_UP = 3~%int8 TILT_DOWN = 4~%int8 PAN_TILT_HOME = 5~%~%#########################################################################################################~%~%# Customize configurations for the Interbotix Turret~%# Inc/Dec Joint speed~%int8 SPEED_INC = 6~%int8 SPEED_DEC = 7~%~%# Quickly toggle between a fast and slow speed setting~%int8 SPEED_COURSE = 8~%int8 SPEED_FINE = 9~%~%#########################################################################################################~%~%# Control the motion of the pan-and-tilt mechanism~%int8 pan_cmd~%int8 tilt_cmd~%~%# Speed Configs~%int8 speed_cmd~%int8 toggle_speed_cmd~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <TurretJoyControl>))
  (cl:+ 0
     1
     1
     1
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <TurretJoyControl>))
  "Converts a ROS message object to a list"
  (cl:list 'TurretJoyControl
    (cl:cons ':pan_cmd (pan_cmd msg))
    (cl:cons ':tilt_cmd (tilt_cmd msg))
    (cl:cons ':speed_cmd (speed_cmd msg))
    (cl:cons ':toggle_speed_cmd (toggle_speed_cmd msg))
))
