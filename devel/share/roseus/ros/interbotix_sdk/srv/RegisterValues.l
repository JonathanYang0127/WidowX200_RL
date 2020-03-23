;; Auto-generated. Do not edit!


(when (boundp 'interbotix_sdk::RegisterValues)
  (if (not (find-package "INTERBOTIX_SDK"))
    (make-package "INTERBOTIX_SDK"))
  (shadow 'RegisterValues (find-package "INTERBOTIX_SDK")))
(unless (find-package "INTERBOTIX_SDK::REGISTERVALUES")
  (make-package "INTERBOTIX_SDK::REGISTERVALUES"))
(unless (find-package "INTERBOTIX_SDK::REGISTERVALUESREQUEST")
  (make-package "INTERBOTIX_SDK::REGISTERVALUESREQUEST"))
(unless (find-package "INTERBOTIX_SDK::REGISTERVALUESRESPONSE")
  (make-package "INTERBOTIX_SDK::REGISTERVALUESRESPONSE"))

(in-package "ROS")





(intern "*ARM_JOINTS_AND_GRIPPER*" (find-package "INTERBOTIX_SDK::REGISTERVALUESREQUEST"))
(shadow '*ARM_JOINTS_AND_GRIPPER* (find-package "INTERBOTIX_SDK::REGISTERVALUESREQUEST"))
(defconstant interbotix_sdk::RegisterValuesRequest::*ARM_JOINTS_AND_GRIPPER* 1)
(intern "*ARM_JOINTS*" (find-package "INTERBOTIX_SDK::REGISTERVALUESREQUEST"))
(shadow '*ARM_JOINTS* (find-package "INTERBOTIX_SDK::REGISTERVALUESREQUEST"))
(defconstant interbotix_sdk::RegisterValuesRequest::*ARM_JOINTS* 2)
(intern "*GRIPPER*" (find-package "INTERBOTIX_SDK::REGISTERVALUESREQUEST"))
(shadow '*GRIPPER* (find-package "INTERBOTIX_SDK::REGISTERVALUESREQUEST"))
(defconstant interbotix_sdk::RegisterValuesRequest::*GRIPPER* 3)
(intern "*SINGLE_MOTOR*" (find-package "INTERBOTIX_SDK::REGISTERVALUESREQUEST"))
(shadow '*SINGLE_MOTOR* (find-package "INTERBOTIX_SDK::REGISTERVALUESREQUEST"))
(defconstant interbotix_sdk::RegisterValuesRequest::*SINGLE_MOTOR* 4)
(defclass interbotix_sdk::RegisterValuesRequest
  :super ros::object
  :slots (_cmd _motor_name _addr_name _value ))

(defmethod interbotix_sdk::RegisterValuesRequest
  (:init
   (&key
    ((:cmd __cmd) 0)
    ((:motor_name __motor_name) "")
    ((:addr_name __addr_name) "")
    ((:value __value) 0)
    )
   (send-super :init)
   (setq _cmd (round __cmd))
   (setq _motor_name (string __motor_name))
   (setq _addr_name (string __addr_name))
   (setq _value (round __value))
   self)
  (:cmd
   (&optional __cmd)
   (if __cmd (setq _cmd __cmd)) _cmd)
  (:motor_name
   (&optional __motor_name)
   (if __motor_name (setq _motor_name __motor_name)) _motor_name)
  (:addr_name
   (&optional __addr_name)
   (if __addr_name (setq _addr_name __addr_name)) _addr_name)
  (:value
   (&optional __value)
   (if __value (setq _value __value)) _value)
  (:serialization-length
   ()
   (+
    ;; int8 _cmd
    1
    ;; string _motor_name
    4 (length _motor_name)
    ;; string _addr_name
    4 (length _addr_name)
    ;; int32 _value
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int8 _cmd
       (write-byte _cmd s)
     ;; string _motor_name
       (write-long (length _motor_name) s) (princ _motor_name s)
     ;; string _addr_name
       (write-long (length _addr_name) s) (princ _addr_name s)
     ;; int32 _value
       (write-long _value s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int8 _cmd
     (setq _cmd (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _cmd 127) (setq _cmd (- _cmd 256)))
   ;; string _motor_name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _motor_name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _addr_name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _addr_name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; int32 _value
     (setq _value (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(defclass interbotix_sdk::RegisterValuesResponse
  :super ros::object
  :slots (_values ))

(defmethod interbotix_sdk::RegisterValuesResponse
  (:init
   (&key
    ((:values __values) (make-array 0 :initial-element 0 :element-type :integer))
    )
   (send-super :init)
   (setq _values __values)
   self)
  (:values
   (&optional __values)
   (if __values (setq _values __values)) _values)
  (:serialization-length
   ()
   (+
    ;; int32[] _values
    (* 4    (length _values)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32[] _values
     (write-long (length _values) s)
     (dotimes (i (length _values))
       (write-long (elt _values i) s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32[] _values
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _values (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _values i) (sys::peek buf ptr- :integer)) (incf ptr- 4)
     ))
   ;;
   self)
  )

(defclass interbotix_sdk::RegisterValues
  :super ros::object
  :slots ())

(setf (get interbotix_sdk::RegisterValues :md5sum-) "c4b094ee6f4751519e444f39591c55e1")
(setf (get interbotix_sdk::RegisterValues :datatype-) "interbotix_sdk/RegisterValues")
(setf (get interbotix_sdk::RegisterValues :request) interbotix_sdk::RegisterValuesRequest)
(setf (get interbotix_sdk::RegisterValues :response) interbotix_sdk::RegisterValuesResponse)

(defmethod interbotix_sdk::RegisterValuesRequest
  (:response () (instance interbotix_sdk::RegisterValuesResponse :init)))

(setf (get interbotix_sdk::RegisterValuesRequest :md5sum-) "c4b094ee6f4751519e444f39591c55e1")
(setf (get interbotix_sdk::RegisterValuesRequest :datatype-) "interbotix_sdk/RegisterValuesRequest")
(setf (get interbotix_sdk::RegisterValuesRequest :definition-)
      "





























int8 ARM_JOINTS_AND_GRIPPER = 1
int8 ARM_JOINTS = 2
int8 GRIPPER = 3
int8 SINGLE_MOTOR = 4

int8 cmd
string motor_name
string addr_name
int32 value
---
int32[] values

")

(setf (get interbotix_sdk::RegisterValuesResponse :md5sum-) "c4b094ee6f4751519e444f39591c55e1")
(setf (get interbotix_sdk::RegisterValuesResponse :datatype-) "interbotix_sdk/RegisterValuesResponse")
(setf (get interbotix_sdk::RegisterValuesResponse :definition-)
      "





























int8 ARM_JOINTS_AND_GRIPPER = 1
int8 ARM_JOINTS = 2
int8 GRIPPER = 3
int8 SINGLE_MOTOR = 4

int8 cmd
string motor_name
string addr_name
int32 value
---
int32[] values

")



(provide :interbotix_sdk/RegisterValues "c4b094ee6f4751519e444f39591c55e1")


