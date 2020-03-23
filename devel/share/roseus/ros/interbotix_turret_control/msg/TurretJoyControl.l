;; Auto-generated. Do not edit!


(when (boundp 'interbotix_turret_control::TurretJoyControl)
  (if (not (find-package "INTERBOTIX_TURRET_CONTROL"))
    (make-package "INTERBOTIX_TURRET_CONTROL"))
  (shadow 'TurretJoyControl (find-package "INTERBOTIX_TURRET_CONTROL")))
(unless (find-package "INTERBOTIX_TURRET_CONTROL::TURRETJOYCONTROL")
  (make-package "INTERBOTIX_TURRET_CONTROL::TURRETJOYCONTROL"))

(in-package "ROS")
;;//! \htmlinclude TurretJoyControl.msg.html


(intern "*PAN_CCW*" (find-package "INTERBOTIX_TURRET_CONTROL::TURRETJOYCONTROL"))
(shadow '*PAN_CCW* (find-package "INTERBOTIX_TURRET_CONTROL::TURRETJOYCONTROL"))
(defconstant interbotix_turret_control::TurretJoyControl::*PAN_CCW* 1)
(intern "*PAN_CW*" (find-package "INTERBOTIX_TURRET_CONTROL::TURRETJOYCONTROL"))
(shadow '*PAN_CW* (find-package "INTERBOTIX_TURRET_CONTROL::TURRETJOYCONTROL"))
(defconstant interbotix_turret_control::TurretJoyControl::*PAN_CW* 2)
(intern "*TILT_UP*" (find-package "INTERBOTIX_TURRET_CONTROL::TURRETJOYCONTROL"))
(shadow '*TILT_UP* (find-package "INTERBOTIX_TURRET_CONTROL::TURRETJOYCONTROL"))
(defconstant interbotix_turret_control::TurretJoyControl::*TILT_UP* 3)
(intern "*TILT_DOWN*" (find-package "INTERBOTIX_TURRET_CONTROL::TURRETJOYCONTROL"))
(shadow '*TILT_DOWN* (find-package "INTERBOTIX_TURRET_CONTROL::TURRETJOYCONTROL"))
(defconstant interbotix_turret_control::TurretJoyControl::*TILT_DOWN* 4)
(intern "*PAN_TILT_HOME*" (find-package "INTERBOTIX_TURRET_CONTROL::TURRETJOYCONTROL"))
(shadow '*PAN_TILT_HOME* (find-package "INTERBOTIX_TURRET_CONTROL::TURRETJOYCONTROL"))
(defconstant interbotix_turret_control::TurretJoyControl::*PAN_TILT_HOME* 5)
(intern "*SPEED_INC*" (find-package "INTERBOTIX_TURRET_CONTROL::TURRETJOYCONTROL"))
(shadow '*SPEED_INC* (find-package "INTERBOTIX_TURRET_CONTROL::TURRETJOYCONTROL"))
(defconstant interbotix_turret_control::TurretJoyControl::*SPEED_INC* 6)
(intern "*SPEED_DEC*" (find-package "INTERBOTIX_TURRET_CONTROL::TURRETJOYCONTROL"))
(shadow '*SPEED_DEC* (find-package "INTERBOTIX_TURRET_CONTROL::TURRETJOYCONTROL"))
(defconstant interbotix_turret_control::TurretJoyControl::*SPEED_DEC* 7)
(intern "*SPEED_COURSE*" (find-package "INTERBOTIX_TURRET_CONTROL::TURRETJOYCONTROL"))
(shadow '*SPEED_COURSE* (find-package "INTERBOTIX_TURRET_CONTROL::TURRETJOYCONTROL"))
(defconstant interbotix_turret_control::TurretJoyControl::*SPEED_COURSE* 8)
(intern "*SPEED_FINE*" (find-package "INTERBOTIX_TURRET_CONTROL::TURRETJOYCONTROL"))
(shadow '*SPEED_FINE* (find-package "INTERBOTIX_TURRET_CONTROL::TURRETJOYCONTROL"))
(defconstant interbotix_turret_control::TurretJoyControl::*SPEED_FINE* 9)
(defclass interbotix_turret_control::TurretJoyControl
  :super ros::object
  :slots (_pan_cmd _tilt_cmd _speed_cmd _toggle_speed_cmd ))

(defmethod interbotix_turret_control::TurretJoyControl
  (:init
   (&key
    ((:pan_cmd __pan_cmd) 0)
    ((:tilt_cmd __tilt_cmd) 0)
    ((:speed_cmd __speed_cmd) 0)
    ((:toggle_speed_cmd __toggle_speed_cmd) 0)
    )
   (send-super :init)
   (setq _pan_cmd (round __pan_cmd))
   (setq _tilt_cmd (round __tilt_cmd))
   (setq _speed_cmd (round __speed_cmd))
   (setq _toggle_speed_cmd (round __toggle_speed_cmd))
   self)
  (:pan_cmd
   (&optional __pan_cmd)
   (if __pan_cmd (setq _pan_cmd __pan_cmd)) _pan_cmd)
  (:tilt_cmd
   (&optional __tilt_cmd)
   (if __tilt_cmd (setq _tilt_cmd __tilt_cmd)) _tilt_cmd)
  (:speed_cmd
   (&optional __speed_cmd)
   (if __speed_cmd (setq _speed_cmd __speed_cmd)) _speed_cmd)
  (:toggle_speed_cmd
   (&optional __toggle_speed_cmd)
   (if __toggle_speed_cmd (setq _toggle_speed_cmd __toggle_speed_cmd)) _toggle_speed_cmd)
  (:serialization-length
   ()
   (+
    ;; int8 _pan_cmd
    1
    ;; int8 _tilt_cmd
    1
    ;; int8 _speed_cmd
    1
    ;; int8 _toggle_speed_cmd
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int8 _pan_cmd
       (write-byte _pan_cmd s)
     ;; int8 _tilt_cmd
       (write-byte _tilt_cmd s)
     ;; int8 _speed_cmd
       (write-byte _speed_cmd s)
     ;; int8 _toggle_speed_cmd
       (write-byte _toggle_speed_cmd s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int8 _pan_cmd
     (setq _pan_cmd (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _pan_cmd 127) (setq _pan_cmd (- _pan_cmd 256)))
   ;; int8 _tilt_cmd
     (setq _tilt_cmd (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _tilt_cmd 127) (setq _tilt_cmd (- _tilt_cmd 256)))
   ;; int8 _speed_cmd
     (setq _speed_cmd (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _speed_cmd 127) (setq _speed_cmd (- _speed_cmd 256)))
   ;; int8 _toggle_speed_cmd
     (setq _toggle_speed_cmd (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _toggle_speed_cmd 127) (setq _toggle_speed_cmd (- _toggle_speed_cmd 256)))
   ;;
   self)
  )

(setf (get interbotix_turret_control::TurretJoyControl :md5sum-) "f699b95ec0a0298bd77c4a4d7f52404f")
(setf (get interbotix_turret_control::TurretJoyControl :datatype-) "interbotix_turret_control/TurretJoyControl")
(setf (get interbotix_turret_control::TurretJoyControl :definition-)
      "# Send commands from the joy_node to the turret_control node

# enum values that define the joystick controls for the robot

#########################################################################################################

# Control the pan-and-tilt mechanism
int8 PAN_CCW = 1
int8 PAN_CW = 2
int8 TILT_UP = 3
int8 TILT_DOWN = 4
int8 PAN_TILT_HOME = 5

#########################################################################################################

# Customize configurations for the Interbotix Turret
# Inc/Dec Joint speed
int8 SPEED_INC = 6
int8 SPEED_DEC = 7

# Quickly toggle between a fast and slow speed setting
int8 SPEED_COURSE = 8
int8 SPEED_FINE = 9

#########################################################################################################

# Control the motion of the pan-and-tilt mechanism
int8 pan_cmd
int8 tilt_cmd

# Speed Configs
int8 speed_cmd
int8 toggle_speed_cmd

")



(provide :interbotix_turret_control/TurretJoyControl "f699b95ec0a0298bd77c4a4d7f52404f")


