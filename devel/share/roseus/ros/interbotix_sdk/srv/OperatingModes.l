;; Auto-generated. Do not edit!


(when (boundp 'interbotix_sdk::OperatingModes)
  (if (not (find-package "INTERBOTIX_SDK"))
    (make-package "INTERBOTIX_SDK"))
  (shadow 'OperatingModes (find-package "INTERBOTIX_SDK")))
(unless (find-package "INTERBOTIX_SDK::OPERATINGMODES")
  (make-package "INTERBOTIX_SDK::OPERATINGMODES"))
(unless (find-package "INTERBOTIX_SDK::OPERATINGMODESREQUEST")
  (make-package "INTERBOTIX_SDK::OPERATINGMODESREQUEST"))
(unless (find-package "INTERBOTIX_SDK::OPERATINGMODESRESPONSE")
  (make-package "INTERBOTIX_SDK::OPERATINGMODESRESPONSE"))

(in-package "ROS")





(intern "*ARM_JOINTS_AND_GRIPPER*" (find-package "INTERBOTIX_SDK::OPERATINGMODESREQUEST"))
(shadow '*ARM_JOINTS_AND_GRIPPER* (find-package "INTERBOTIX_SDK::OPERATINGMODESREQUEST"))
(defconstant interbotix_sdk::OperatingModesRequest::*ARM_JOINTS_AND_GRIPPER* 1)
(intern "*ARM_JOINTS*" (find-package "INTERBOTIX_SDK::OPERATINGMODESREQUEST"))
(shadow '*ARM_JOINTS* (find-package "INTERBOTIX_SDK::OPERATINGMODESREQUEST"))
(defconstant interbotix_sdk::OperatingModesRequest::*ARM_JOINTS* 2)
(intern "*GRIPPER*" (find-package "INTERBOTIX_SDK::OPERATINGMODESREQUEST"))
(shadow '*GRIPPER* (find-package "INTERBOTIX_SDK::OPERATINGMODESREQUEST"))
(defconstant interbotix_sdk::OperatingModesRequest::*GRIPPER* 3)
(intern "*SINGLE_JOINT*" (find-package "INTERBOTIX_SDK::OPERATINGMODESREQUEST"))
(shadow '*SINGLE_JOINT* (find-package "INTERBOTIX_SDK::OPERATINGMODESREQUEST"))
(defconstant interbotix_sdk::OperatingModesRequest::*SINGLE_JOINT* 4)
(defclass interbotix_sdk::OperatingModesRequest
  :super ros::object
  :slots (_cmd _mode _joint_name _use_custom_profiles _profile_velocity _profile_acceleration ))

(defmethod interbotix_sdk::OperatingModesRequest
  (:init
   (&key
    ((:cmd __cmd) 0)
    ((:mode __mode) "")
    ((:joint_name __joint_name) "")
    ((:use_custom_profiles __use_custom_profiles) nil)
    ((:profile_velocity __profile_velocity) 0)
    ((:profile_acceleration __profile_acceleration) 0)
    )
   (send-super :init)
   (setq _cmd (round __cmd))
   (setq _mode (string __mode))
   (setq _joint_name (string __joint_name))
   (setq _use_custom_profiles __use_custom_profiles)
   (setq _profile_velocity (round __profile_velocity))
   (setq _profile_acceleration (round __profile_acceleration))
   self)
  (:cmd
   (&optional __cmd)
   (if __cmd (setq _cmd __cmd)) _cmd)
  (:mode
   (&optional __mode)
   (if __mode (setq _mode __mode)) _mode)
  (:joint_name
   (&optional __joint_name)
   (if __joint_name (setq _joint_name __joint_name)) _joint_name)
  (:use_custom_profiles
   (&optional __use_custom_profiles)
   (if __use_custom_profiles (setq _use_custom_profiles __use_custom_profiles)) _use_custom_profiles)
  (:profile_velocity
   (&optional __profile_velocity)
   (if __profile_velocity (setq _profile_velocity __profile_velocity)) _profile_velocity)
  (:profile_acceleration
   (&optional __profile_acceleration)
   (if __profile_acceleration (setq _profile_acceleration __profile_acceleration)) _profile_acceleration)
  (:serialization-length
   ()
   (+
    ;; int8 _cmd
    1
    ;; string _mode
    4 (length _mode)
    ;; string _joint_name
    4 (length _joint_name)
    ;; bool _use_custom_profiles
    1
    ;; int32 _profile_velocity
    4
    ;; int32 _profile_acceleration
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int8 _cmd
       (write-byte _cmd s)
     ;; string _mode
       (write-long (length _mode) s) (princ _mode s)
     ;; string _joint_name
       (write-long (length _joint_name) s) (princ _joint_name s)
     ;; bool _use_custom_profiles
       (if _use_custom_profiles (write-byte -1 s) (write-byte 0 s))
     ;; int32 _profile_velocity
       (write-long _profile_velocity s)
     ;; int32 _profile_acceleration
       (write-long _profile_acceleration s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int8 _cmd
     (setq _cmd (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _cmd 127) (setq _cmd (- _cmd 256)))
   ;; string _mode
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _mode (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _joint_name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _joint_name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; bool _use_custom_profiles
     (setq _use_custom_profiles (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; int32 _profile_velocity
     (setq _profile_velocity (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _profile_acceleration
     (setq _profile_acceleration (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(defclass interbotix_sdk::OperatingModesResponse
  :super ros::object
  :slots ())

(defmethod interbotix_sdk::OperatingModesResponse
  (:init
   (&key
    )
   (send-super :init)
   self)
  (:serialization-length
   ()
   (+
    0
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;;
   self)
  )

(defclass interbotix_sdk::OperatingModes
  :super ros::object
  :slots ())

(setf (get interbotix_sdk::OperatingModes :md5sum-) "585951edcc6006e2034f68a456aad669")
(setf (get interbotix_sdk::OperatingModes :datatype-) "interbotix_sdk/OperatingModes")
(setf (get interbotix_sdk::OperatingModes :request) interbotix_sdk::OperatingModesRequest)
(setf (get interbotix_sdk::OperatingModes :response) interbotix_sdk::OperatingModesResponse)

(defmethod interbotix_sdk::OperatingModesRequest
  (:response () (instance interbotix_sdk::OperatingModesResponse :init)))

(setf (get interbotix_sdk::OperatingModesRequest :md5sum-) "585951edcc6006e2034f68a456aad669")
(setf (get interbotix_sdk::OperatingModesRequest :datatype-) "interbotix_sdk/OperatingModesRequest")
(setf (get interbotix_sdk::OperatingModesRequest :definition-)
      "
































int8 ARM_JOINTS_AND_GRIPPER = 1
int8 ARM_JOINTS = 2
int8 GRIPPER = 3
int8 SINGLE_JOINT = 4

int8 cmd
string mode
string joint_name
bool use_custom_profiles
int32 profile_velocity
int32 profile_acceleration
---

")

(setf (get interbotix_sdk::OperatingModesResponse :md5sum-) "585951edcc6006e2034f68a456aad669")
(setf (get interbotix_sdk::OperatingModesResponse :datatype-) "interbotix_sdk/OperatingModesResponse")
(setf (get interbotix_sdk::OperatingModesResponse :definition-)
      "
































int8 ARM_JOINTS_AND_GRIPPER = 1
int8 ARM_JOINTS = 2
int8 GRIPPER = 3
int8 SINGLE_JOINT = 4

int8 cmd
string mode
string joint_name
bool use_custom_profiles
int32 profile_velocity
int32 profile_acceleration
---

")



(provide :interbotix_sdk/OperatingModes "585951edcc6006e2034f68a456aad669")


