;; Auto-generated. Do not edit!


(when (boundp 'interbotix_sdk::RobotInfo)
  (if (not (find-package "INTERBOTIX_SDK"))
    (make-package "INTERBOTIX_SDK"))
  (shadow 'RobotInfo (find-package "INTERBOTIX_SDK")))
(unless (find-package "INTERBOTIX_SDK::ROBOTINFO")
  (make-package "INTERBOTIX_SDK::ROBOTINFO"))
(unless (find-package "INTERBOTIX_SDK::ROBOTINFOREQUEST")
  (make-package "INTERBOTIX_SDK::ROBOTINFOREQUEST"))
(unless (find-package "INTERBOTIX_SDK::ROBOTINFORESPONSE")
  (make-package "INTERBOTIX_SDK::ROBOTINFORESPONSE"))

(in-package "ROS")





(defclass interbotix_sdk::RobotInfoRequest
  :super ros::object
  :slots ())

(defmethod interbotix_sdk::RobotInfoRequest
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

(defclass interbotix_sdk::RobotInfoResponse
  :super ros::object
  :slots (_joint_names _joint_ids _lower_joint_limits _upper_joint_limits _velocity_limits _lower_gripper_limit _upper_gripper_limit _use_gripper _home_pos _sleep_pos _num_joints _num_single_joints ))

(defmethod interbotix_sdk::RobotInfoResponse
  (:init
   (&key
    ((:joint_names __joint_names) (let (r) (dotimes (i 0) (push "" r)) r))
    ((:joint_ids __joint_ids) (make-array 0 :initial-element 0 :element-type :integer))
    ((:lower_joint_limits __lower_joint_limits) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:upper_joint_limits __upper_joint_limits) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:velocity_limits __velocity_limits) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:lower_gripper_limit __lower_gripper_limit) 0.0)
    ((:upper_gripper_limit __upper_gripper_limit) 0.0)
    ((:use_gripper __use_gripper) nil)
    ((:home_pos __home_pos) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:sleep_pos __sleep_pos) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:num_joints __num_joints) 0)
    ((:num_single_joints __num_single_joints) 0)
    )
   (send-super :init)
   (setq _joint_names __joint_names)
   (setq _joint_ids __joint_ids)
   (setq _lower_joint_limits __lower_joint_limits)
   (setq _upper_joint_limits __upper_joint_limits)
   (setq _velocity_limits __velocity_limits)
   (setq _lower_gripper_limit (float __lower_gripper_limit))
   (setq _upper_gripper_limit (float __upper_gripper_limit))
   (setq _use_gripper __use_gripper)
   (setq _home_pos __home_pos)
   (setq _sleep_pos __sleep_pos)
   (setq _num_joints (round __num_joints))
   (setq _num_single_joints (round __num_single_joints))
   self)
  (:joint_names
   (&optional __joint_names)
   (if __joint_names (setq _joint_names __joint_names)) _joint_names)
  (:joint_ids
   (&optional __joint_ids)
   (if __joint_ids (setq _joint_ids __joint_ids)) _joint_ids)
  (:lower_joint_limits
   (&optional __lower_joint_limits)
   (if __lower_joint_limits (setq _lower_joint_limits __lower_joint_limits)) _lower_joint_limits)
  (:upper_joint_limits
   (&optional __upper_joint_limits)
   (if __upper_joint_limits (setq _upper_joint_limits __upper_joint_limits)) _upper_joint_limits)
  (:velocity_limits
   (&optional __velocity_limits)
   (if __velocity_limits (setq _velocity_limits __velocity_limits)) _velocity_limits)
  (:lower_gripper_limit
   (&optional __lower_gripper_limit)
   (if __lower_gripper_limit (setq _lower_gripper_limit __lower_gripper_limit)) _lower_gripper_limit)
  (:upper_gripper_limit
   (&optional __upper_gripper_limit)
   (if __upper_gripper_limit (setq _upper_gripper_limit __upper_gripper_limit)) _upper_gripper_limit)
  (:use_gripper
   (&optional __use_gripper)
   (if __use_gripper (setq _use_gripper __use_gripper)) _use_gripper)
  (:home_pos
   (&optional __home_pos)
   (if __home_pos (setq _home_pos __home_pos)) _home_pos)
  (:sleep_pos
   (&optional __sleep_pos)
   (if __sleep_pos (setq _sleep_pos __sleep_pos)) _sleep_pos)
  (:num_joints
   (&optional __num_joints)
   (if __num_joints (setq _num_joints __num_joints)) _num_joints)
  (:num_single_joints
   (&optional __num_single_joints)
   (if __num_single_joints (setq _num_single_joints __num_single_joints)) _num_single_joints)
  (:serialization-length
   ()
   (+
    ;; string[] _joint_names
    (apply #'+ (mapcar #'(lambda (x) (+ 4 (length x))) _joint_names)) 4
    ;; int16[] _joint_ids
    (* 2    (length _joint_ids)) 4
    ;; float64[] _lower_joint_limits
    (* 8    (length _lower_joint_limits)) 4
    ;; float64[] _upper_joint_limits
    (* 8    (length _upper_joint_limits)) 4
    ;; float64[] _velocity_limits
    (* 8    (length _velocity_limits)) 4
    ;; float64 _lower_gripper_limit
    8
    ;; float64 _upper_gripper_limit
    8
    ;; bool _use_gripper
    1
    ;; float64[] _home_pos
    (* 8    (length _home_pos)) 4
    ;; float64[] _sleep_pos
    (* 8    (length _sleep_pos)) 4
    ;; int8 _num_joints
    1
    ;; int8 _num_single_joints
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string[] _joint_names
     (write-long (length _joint_names) s)
     (dolist (elem _joint_names)
       (write-long (length elem) s) (princ elem s)
       )
     ;; int16[] _joint_ids
     (write-long (length _joint_ids) s)
     (dotimes (i (length _joint_ids))
       (write-word (elt _joint_ids i) s)
       )
     ;; float64[] _lower_joint_limits
     (write-long (length _lower_joint_limits) s)
     (dotimes (i (length _lower_joint_limits))
       (sys::poke (elt _lower_joint_limits i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _upper_joint_limits
     (write-long (length _upper_joint_limits) s)
     (dotimes (i (length _upper_joint_limits))
       (sys::poke (elt _upper_joint_limits i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _velocity_limits
     (write-long (length _velocity_limits) s)
     (dotimes (i (length _velocity_limits))
       (sys::poke (elt _velocity_limits i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64 _lower_gripper_limit
       (sys::poke _lower_gripper_limit (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _upper_gripper_limit
       (sys::poke _upper_gripper_limit (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; bool _use_gripper
       (if _use_gripper (write-byte -1 s) (write-byte 0 s))
     ;; float64[] _home_pos
     (write-long (length _home_pos) s)
     (dotimes (i (length _home_pos))
       (sys::poke (elt _home_pos i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _sleep_pos
     (write-long (length _sleep_pos) s)
     (dotimes (i (length _sleep_pos))
       (sys::poke (elt _sleep_pos i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; int8 _num_joints
       (write-byte _num_joints s)
     ;; int8 _num_single_joints
       (write-byte _num_single_joints s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string[] _joint_names
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _joint_names (make-list n))
     (dotimes (i n)
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setf (elt _joint_names i) (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
     ))
   ;; int16[] _joint_ids
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _joint_ids (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _joint_ids i) (sys::peek buf ptr- :short)) (incf ptr- 2)
     ))
   ;; float64[] _lower_joint_limits
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _lower_joint_limits (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _lower_joint_limits i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _upper_joint_limits
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _upper_joint_limits (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _upper_joint_limits i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _velocity_limits
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _velocity_limits (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _velocity_limits i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64 _lower_gripper_limit
     (setq _lower_gripper_limit (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _upper_gripper_limit
     (setq _upper_gripper_limit (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; bool _use_gripper
     (setq _use_gripper (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; float64[] _home_pos
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _home_pos (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _home_pos i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _sleep_pos
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _sleep_pos (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _sleep_pos i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; int8 _num_joints
     (setq _num_joints (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _num_joints 127) (setq _num_joints (- _num_joints 256)))
   ;; int8 _num_single_joints
     (setq _num_single_joints (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _num_single_joints 127) (setq _num_single_joints (- _num_single_joints 256)))
   ;;
   self)
  )

(defclass interbotix_sdk::RobotInfo
  :super ros::object
  :slots ())

(setf (get interbotix_sdk::RobotInfo :md5sum-) "8cbf67af7802be3e000262518104df12")
(setf (get interbotix_sdk::RobotInfo :datatype-) "interbotix_sdk/RobotInfo")
(setf (get interbotix_sdk::RobotInfo :request) interbotix_sdk::RobotInfoRequest)
(setf (get interbotix_sdk::RobotInfo :response) interbotix_sdk::RobotInfoResponse)

(defmethod interbotix_sdk::RobotInfoRequest
  (:response () (instance interbotix_sdk::RobotInfoResponse :init)))

(setf (get interbotix_sdk::RobotInfoRequest :md5sum-) "8cbf67af7802be3e000262518104df12")
(setf (get interbotix_sdk::RobotInfoRequest :datatype-) "interbotix_sdk/RobotInfoRequest")
(setf (get interbotix_sdk::RobotInfoRequest :definition-)
      "























---

string[] joint_names
int16[] joint_ids
float64[] lower_joint_limits
float64[] upper_joint_limits
float64[] velocity_limits
float64 lower_gripper_limit
float64 upper_gripper_limit
bool use_gripper
float64[] home_pos
float64[] sleep_pos
int8 num_joints
int8 num_single_joints

")

(setf (get interbotix_sdk::RobotInfoResponse :md5sum-) "8cbf67af7802be3e000262518104df12")
(setf (get interbotix_sdk::RobotInfoResponse :datatype-) "interbotix_sdk/RobotInfoResponse")
(setf (get interbotix_sdk::RobotInfoResponse :definition-)
      "























---

string[] joint_names
int16[] joint_ids
float64[] lower_joint_limits
float64[] upper_joint_limits
float64[] velocity_limits
float64 lower_gripper_limit
float64 upper_gripper_limit
bool use_gripper
float64[] home_pos
float64[] sleep_pos
int8 num_joints
int8 num_single_joints

")



(provide :interbotix_sdk/RobotInfo "8cbf67af7802be3e000262518104df12")


