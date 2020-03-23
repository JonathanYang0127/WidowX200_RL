; Auto-generated. Do not edit!


(cl:in-package interbotix_sdk-srv)


;//! \htmlinclude OperatingModes-request.msg.html

(cl:defclass <OperatingModes-request> (roslisp-msg-protocol:ros-message)
  ((cmd
    :reader cmd
    :initarg :cmd
    :type cl:fixnum
    :initform 0)
   (mode
    :reader mode
    :initarg :mode
    :type cl:string
    :initform "")
   (joint_name
    :reader joint_name
    :initarg :joint_name
    :type cl:string
    :initform "")
   (use_custom_profiles
    :reader use_custom_profiles
    :initarg :use_custom_profiles
    :type cl:boolean
    :initform cl:nil)
   (profile_velocity
    :reader profile_velocity
    :initarg :profile_velocity
    :type cl:integer
    :initform 0)
   (profile_acceleration
    :reader profile_acceleration
    :initarg :profile_acceleration
    :type cl:integer
    :initform 0))
)

(cl:defclass OperatingModes-request (<OperatingModes-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <OperatingModes-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'OperatingModes-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name interbotix_sdk-srv:<OperatingModes-request> is deprecated: use interbotix_sdk-srv:OperatingModes-request instead.")))

(cl:ensure-generic-function 'cmd-val :lambda-list '(m))
(cl:defmethod cmd-val ((m <OperatingModes-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_sdk-srv:cmd-val is deprecated.  Use interbotix_sdk-srv:cmd instead.")
  (cmd m))

(cl:ensure-generic-function 'mode-val :lambda-list '(m))
(cl:defmethod mode-val ((m <OperatingModes-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_sdk-srv:mode-val is deprecated.  Use interbotix_sdk-srv:mode instead.")
  (mode m))

(cl:ensure-generic-function 'joint_name-val :lambda-list '(m))
(cl:defmethod joint_name-val ((m <OperatingModes-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_sdk-srv:joint_name-val is deprecated.  Use interbotix_sdk-srv:joint_name instead.")
  (joint_name m))

(cl:ensure-generic-function 'use_custom_profiles-val :lambda-list '(m))
(cl:defmethod use_custom_profiles-val ((m <OperatingModes-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_sdk-srv:use_custom_profiles-val is deprecated.  Use interbotix_sdk-srv:use_custom_profiles instead.")
  (use_custom_profiles m))

(cl:ensure-generic-function 'profile_velocity-val :lambda-list '(m))
(cl:defmethod profile_velocity-val ((m <OperatingModes-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_sdk-srv:profile_velocity-val is deprecated.  Use interbotix_sdk-srv:profile_velocity instead.")
  (profile_velocity m))

(cl:ensure-generic-function 'profile_acceleration-val :lambda-list '(m))
(cl:defmethod profile_acceleration-val ((m <OperatingModes-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interbotix_sdk-srv:profile_acceleration-val is deprecated.  Use interbotix_sdk-srv:profile_acceleration instead.")
  (profile_acceleration m))
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql '<OperatingModes-request>)))
    "Constants for message type '<OperatingModes-request>"
  '((:ARM_JOINTS_AND_GRIPPER . 1)
    (:ARM_JOINTS . 2)
    (:GRIPPER . 3)
    (:SINGLE_JOINT . 4))
)
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql 'OperatingModes-request)))
    "Constants for message type 'OperatingModes-request"
  '((:ARM_JOINTS_AND_GRIPPER . 1)
    (:ARM_JOINTS . 2)
    (:GRIPPER . 3)
    (:SINGLE_JOINT . 4))
)
(cl:defmethod roslisp-msg-protocol:serialize ((msg <OperatingModes-request>) ostream)
  "Serializes a message object of type '<OperatingModes-request>"
  (cl:let* ((signed (cl:slot-value msg 'cmd)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'mode))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'mode))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'joint_name))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'joint_name))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'use_custom_profiles) 1 0)) ostream)
  (cl:let* ((signed (cl:slot-value msg 'profile_velocity)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'profile_acceleration)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <OperatingModes-request>) istream)
  "Deserializes a message object of type '<OperatingModes-request>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'cmd) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'mode) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'mode) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'joint_name) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'joint_name) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:setf (cl:slot-value msg 'use_custom_profiles) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'profile_velocity) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'profile_acceleration) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<OperatingModes-request>)))
  "Returns string type for a service object of type '<OperatingModes-request>"
  "interbotix_sdk/OperatingModesRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'OperatingModes-request)))
  "Returns string type for a service object of type 'OperatingModes-request"
  "interbotix_sdk/OperatingModesRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<OperatingModes-request>)))
  "Returns md5sum for a message object of type '<OperatingModes-request>"
  "585951edcc6006e2034f68a456aad669")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'OperatingModes-request)))
  "Returns md5sum for a message object of type 'OperatingModes-request"
  "585951edcc6006e2034f68a456aad669")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<OperatingModes-request>)))
  "Returns full string definition for message of type '<OperatingModes-request>"
  (cl:format cl:nil "~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%int8 ARM_JOINTS_AND_GRIPPER = 1~%int8 ARM_JOINTS = 2~%int8 GRIPPER = 3~%int8 SINGLE_JOINT = 4~%~%int8 cmd~%string mode~%string joint_name~%bool use_custom_profiles~%int32 profile_velocity~%int32 profile_acceleration~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'OperatingModes-request)))
  "Returns full string definition for message of type 'OperatingModes-request"
  (cl:format cl:nil "~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%~%int8 ARM_JOINTS_AND_GRIPPER = 1~%int8 ARM_JOINTS = 2~%int8 GRIPPER = 3~%int8 SINGLE_JOINT = 4~%~%int8 cmd~%string mode~%string joint_name~%bool use_custom_profiles~%int32 profile_velocity~%int32 profile_acceleration~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <OperatingModes-request>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'mode))
     4 (cl:length (cl:slot-value msg 'joint_name))
     1
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <OperatingModes-request>))
  "Converts a ROS message object to a list"
  (cl:list 'OperatingModes-request
    (cl:cons ':cmd (cmd msg))
    (cl:cons ':mode (mode msg))
    (cl:cons ':joint_name (joint_name msg))
    (cl:cons ':use_custom_profiles (use_custom_profiles msg))
    (cl:cons ':profile_velocity (profile_velocity msg))
    (cl:cons ':profile_acceleration (profile_acceleration msg))
))
;//! \htmlinclude OperatingModes-response.msg.html

(cl:defclass <OperatingModes-response> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass OperatingModes-response (<OperatingModes-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <OperatingModes-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'OperatingModes-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name interbotix_sdk-srv:<OperatingModes-response> is deprecated: use interbotix_sdk-srv:OperatingModes-response instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <OperatingModes-response>) ostream)
  "Serializes a message object of type '<OperatingModes-response>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <OperatingModes-response>) istream)
  "Deserializes a message object of type '<OperatingModes-response>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<OperatingModes-response>)))
  "Returns string type for a service object of type '<OperatingModes-response>"
  "interbotix_sdk/OperatingModesResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'OperatingModes-response)))
  "Returns string type for a service object of type 'OperatingModes-response"
  "interbotix_sdk/OperatingModesResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<OperatingModes-response>)))
  "Returns md5sum for a message object of type '<OperatingModes-response>"
  "585951edcc6006e2034f68a456aad669")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'OperatingModes-response)))
  "Returns md5sum for a message object of type 'OperatingModes-response"
  "585951edcc6006e2034f68a456aad669")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<OperatingModes-response>)))
  "Returns full string definition for message of type '<OperatingModes-response>"
  (cl:format cl:nil "~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'OperatingModes-response)))
  "Returns full string definition for message of type 'OperatingModes-response"
  (cl:format cl:nil "~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <OperatingModes-response>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <OperatingModes-response>))
  "Converts a ROS message object to a list"
  (cl:list 'OperatingModes-response
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'OperatingModes)))
  'OperatingModes-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'OperatingModes)))
  'OperatingModes-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'OperatingModes)))
  "Returns string type for a service object of type '<OperatingModes>"
  "interbotix_sdk/OperatingModes")