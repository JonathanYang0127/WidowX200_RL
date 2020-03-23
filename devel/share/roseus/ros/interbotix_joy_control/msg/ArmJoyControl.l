;; Auto-generated. Do not edit!


(when (boundp 'interbotix_joy_control::ArmJoyControl)
  (if (not (find-package "INTERBOTIX_JOY_CONTROL"))
    (make-package "INTERBOTIX_JOY_CONTROL"))
  (shadow 'ArmJoyControl (find-package "INTERBOTIX_JOY_CONTROL")))
(unless (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL")
  (make-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))

(in-package "ROS")
;;//! \htmlinclude ArmJoyControl.msg.html


(intern "*EE_X_INC*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*EE_X_INC* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*EE_X_INC* 1)
(intern "*EE_X_DEC*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*EE_X_DEC* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*EE_X_DEC* 2)
(intern "*EE_Y_INC*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*EE_Y_INC* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*EE_Y_INC* 3)
(intern "*EE_Y_DEC*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*EE_Y_DEC* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*EE_Y_DEC* 4)
(intern "*EE_Z_INC*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*EE_Z_INC* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*EE_Z_INC* 5)
(intern "*EE_Z_DEC*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*EE_Z_DEC* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*EE_Z_DEC* 6)
(intern "*EE_ROLL_CCW*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*EE_ROLL_CCW* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*EE_ROLL_CCW* 7)
(intern "*EE_ROLL_CW*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*EE_ROLL_CW* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*EE_ROLL_CW* 8)
(intern "*EE_PITCH_UP*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*EE_PITCH_UP* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*EE_PITCH_UP* 9)
(intern "*EE_PITCH_DOWN*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*EE_PITCH_DOWN* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*EE_PITCH_DOWN* 10)
(intern "*WAIST_CCW*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*WAIST_CCW* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*WAIST_CCW* 11)
(intern "*WAIST_CW*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*WAIST_CW* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*WAIST_CW* 12)
(intern "*GRIPPER_OPEN*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*GRIPPER_OPEN* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*GRIPPER_OPEN* 13)
(intern "*GRIPPER_CLOSE*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*GRIPPER_CLOSE* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*GRIPPER_CLOSE* 14)
(intern "*HOME_POSE*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*HOME_POSE* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*HOME_POSE* 15)
(intern "*SLEEP_POSE*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*SLEEP_POSE* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*SLEEP_POSE* 16)
(intern "*SPEED_INC*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*SPEED_INC* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*SPEED_INC* 17)
(intern "*SPEED_DEC*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*SPEED_DEC* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*SPEED_DEC* 18)
(intern "*SPEED_COURSE*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*SPEED_COURSE* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*SPEED_COURSE* 19)
(intern "*SPEED_FINE*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*SPEED_FINE* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*SPEED_FINE* 20)
(intern "*GRIPPER_PWM_INC*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*GRIPPER_PWM_INC* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*GRIPPER_PWM_INC* 21)
(intern "*GRIPPER_PWM_DEC*" (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(shadow '*GRIPPER_PWM_DEC* (find-package "INTERBOTIX_JOY_CONTROL::ARMJOYCONTROL"))
(defconstant interbotix_joy_control::ArmJoyControl::*GRIPPER_PWM_DEC* 22)
(defclass interbotix_joy_control::ArmJoyControl
  :super ros::object
  :slots (_ee_x_cmd _ee_y_cmd _ee_z_cmd _ee_roll_cmd _ee_pitch_cmd _waist_cmd _gripper_cmd _robot_pose _speed_cmd _toggle_speed_cmd _gripper_pwm_cmd ))

(defmethod interbotix_joy_control::ArmJoyControl
  (:init
   (&key
    ((:ee_x_cmd __ee_x_cmd) 0)
    ((:ee_y_cmd __ee_y_cmd) 0)
    ((:ee_z_cmd __ee_z_cmd) 0)
    ((:ee_roll_cmd __ee_roll_cmd) 0)
    ((:ee_pitch_cmd __ee_pitch_cmd) 0)
    ((:waist_cmd __waist_cmd) 0)
    ((:gripper_cmd __gripper_cmd) 0)
    ((:robot_pose __robot_pose) 0)
    ((:speed_cmd __speed_cmd) 0)
    ((:toggle_speed_cmd __toggle_speed_cmd) 0)
    ((:gripper_pwm_cmd __gripper_pwm_cmd) 0)
    )
   (send-super :init)
   (setq _ee_x_cmd (round __ee_x_cmd))
   (setq _ee_y_cmd (round __ee_y_cmd))
   (setq _ee_z_cmd (round __ee_z_cmd))
   (setq _ee_roll_cmd (round __ee_roll_cmd))
   (setq _ee_pitch_cmd (round __ee_pitch_cmd))
   (setq _waist_cmd (round __waist_cmd))
   (setq _gripper_cmd (round __gripper_cmd))
   (setq _robot_pose (round __robot_pose))
   (setq _speed_cmd (round __speed_cmd))
   (setq _toggle_speed_cmd (round __toggle_speed_cmd))
   (setq _gripper_pwm_cmd (round __gripper_pwm_cmd))
   self)
  (:ee_x_cmd
   (&optional __ee_x_cmd)
   (if __ee_x_cmd (setq _ee_x_cmd __ee_x_cmd)) _ee_x_cmd)
  (:ee_y_cmd
   (&optional __ee_y_cmd)
   (if __ee_y_cmd (setq _ee_y_cmd __ee_y_cmd)) _ee_y_cmd)
  (:ee_z_cmd
   (&optional __ee_z_cmd)
   (if __ee_z_cmd (setq _ee_z_cmd __ee_z_cmd)) _ee_z_cmd)
  (:ee_roll_cmd
   (&optional __ee_roll_cmd)
   (if __ee_roll_cmd (setq _ee_roll_cmd __ee_roll_cmd)) _ee_roll_cmd)
  (:ee_pitch_cmd
   (&optional __ee_pitch_cmd)
   (if __ee_pitch_cmd (setq _ee_pitch_cmd __ee_pitch_cmd)) _ee_pitch_cmd)
  (:waist_cmd
   (&optional __waist_cmd)
   (if __waist_cmd (setq _waist_cmd __waist_cmd)) _waist_cmd)
  (:gripper_cmd
   (&optional __gripper_cmd)
   (if __gripper_cmd (setq _gripper_cmd __gripper_cmd)) _gripper_cmd)
  (:robot_pose
   (&optional __robot_pose)
   (if __robot_pose (setq _robot_pose __robot_pose)) _robot_pose)
  (:speed_cmd
   (&optional __speed_cmd)
   (if __speed_cmd (setq _speed_cmd __speed_cmd)) _speed_cmd)
  (:toggle_speed_cmd
   (&optional __toggle_speed_cmd)
   (if __toggle_speed_cmd (setq _toggle_speed_cmd __toggle_speed_cmd)) _toggle_speed_cmd)
  (:gripper_pwm_cmd
   (&optional __gripper_pwm_cmd)
   (if __gripper_pwm_cmd (setq _gripper_pwm_cmd __gripper_pwm_cmd)) _gripper_pwm_cmd)
  (:serialization-length
   ()
   (+
    ;; int8 _ee_x_cmd
    1
    ;; int8 _ee_y_cmd
    1
    ;; int8 _ee_z_cmd
    1
    ;; int8 _ee_roll_cmd
    1
    ;; int8 _ee_pitch_cmd
    1
    ;; int8 _waist_cmd
    1
    ;; int8 _gripper_cmd
    1
    ;; int8 _robot_pose
    1
    ;; int8 _speed_cmd
    1
    ;; int8 _toggle_speed_cmd
    1
    ;; int8 _gripper_pwm_cmd
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int8 _ee_x_cmd
       (write-byte _ee_x_cmd s)
     ;; int8 _ee_y_cmd
       (write-byte _ee_y_cmd s)
     ;; int8 _ee_z_cmd
       (write-byte _ee_z_cmd s)
     ;; int8 _ee_roll_cmd
       (write-byte _ee_roll_cmd s)
     ;; int8 _ee_pitch_cmd
       (write-byte _ee_pitch_cmd s)
     ;; int8 _waist_cmd
       (write-byte _waist_cmd s)
     ;; int8 _gripper_cmd
       (write-byte _gripper_cmd s)
     ;; int8 _robot_pose
       (write-byte _robot_pose s)
     ;; int8 _speed_cmd
       (write-byte _speed_cmd s)
     ;; int8 _toggle_speed_cmd
       (write-byte _toggle_speed_cmd s)
     ;; int8 _gripper_pwm_cmd
       (write-byte _gripper_pwm_cmd s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int8 _ee_x_cmd
     (setq _ee_x_cmd (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _ee_x_cmd 127) (setq _ee_x_cmd (- _ee_x_cmd 256)))
   ;; int8 _ee_y_cmd
     (setq _ee_y_cmd (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _ee_y_cmd 127) (setq _ee_y_cmd (- _ee_y_cmd 256)))
   ;; int8 _ee_z_cmd
     (setq _ee_z_cmd (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _ee_z_cmd 127) (setq _ee_z_cmd (- _ee_z_cmd 256)))
   ;; int8 _ee_roll_cmd
     (setq _ee_roll_cmd (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _ee_roll_cmd 127) (setq _ee_roll_cmd (- _ee_roll_cmd 256)))
   ;; int8 _ee_pitch_cmd
     (setq _ee_pitch_cmd (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _ee_pitch_cmd 127) (setq _ee_pitch_cmd (- _ee_pitch_cmd 256)))
   ;; int8 _waist_cmd
     (setq _waist_cmd (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _waist_cmd 127) (setq _waist_cmd (- _waist_cmd 256)))
   ;; int8 _gripper_cmd
     (setq _gripper_cmd (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _gripper_cmd 127) (setq _gripper_cmd (- _gripper_cmd 256)))
   ;; int8 _robot_pose
     (setq _robot_pose (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _robot_pose 127) (setq _robot_pose (- _robot_pose 256)))
   ;; int8 _speed_cmd
     (setq _speed_cmd (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _speed_cmd 127) (setq _speed_cmd (- _speed_cmd 256)))
   ;; int8 _toggle_speed_cmd
     (setq _toggle_speed_cmd (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _toggle_speed_cmd 127) (setq _toggle_speed_cmd (- _toggle_speed_cmd 256)))
   ;; int8 _gripper_pwm_cmd
     (setq _gripper_pwm_cmd (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _gripper_pwm_cmd 127) (setq _gripper_pwm_cmd (- _gripper_pwm_cmd 256)))
   ;;
   self)
  )

(setf (get interbotix_joy_control::ArmJoyControl :md5sum-) "74891567b0665aa1963bdc439b948bf5")
(setf (get interbotix_joy_control::ArmJoyControl :datatype-) "interbotix_joy_control/ArmJoyControl")
(setf (get interbotix_joy_control::ArmJoyControl :definition-)
      "# Send commands from the joy_control node to the joy_robot_control node

# enum values that define the joystick controls for the robot

#########################################################################################################

# Control the motion of the virtual 'ee_gripper_link' or end effector using the modern_robotics_ik engine
# Position Control
int8 EE_X_INC = 1
int8 EE_X_DEC = 2
int8 EE_Y_INC = 3
int8 EE_Y_DEC = 4
int8 EE_Z_INC = 5
int8 EE_Z_DEC = 6

# Orientation Control
int8 EE_ROLL_CCW = 7
int8 EE_ROLL_CW = 8
int8 EE_PITCH_UP = 9
int8 EE_PITCH_DOWN = 10

#########################################################################################################

# Control the motion of independent joints on the Arm or send predefined robot poses
# Waist Joint Control
int8 WAIST_CCW = 11
int8 WAIST_CW = 12

# Gripper Control
int8 GRIPPER_OPEN = 13
int8 GRIPPER_CLOSE = 14

# Pose Control
int8 HOME_POSE = 15
int8 SLEEP_POSE = 16

#########################################################################################################

# Customize configurations for the Interbotix Arm
# Inc/Dec Joint speed
int8 SPEED_INC = 17
int8 SPEED_DEC = 18

# Quickly toggle between a fast and slow speed setting
int8 SPEED_COURSE = 19
int8 SPEED_FINE = 20

# Inc/Dec Gripper pressure
int8 GRIPPER_PWM_INC = 21
int8 GRIPPER_PWM_DEC = 22

#########################################################################################################

# Control the motion of the Interbotix Arm
int8 ee_x_cmd
int8 ee_y_cmd
int8 ee_z_cmd
int8 ee_roll_cmd
int8 ee_pitch_cmd

# Independent Joint/Pose Control
int8 waist_cmd
int8 gripper_cmd
int8 robot_pose

# Speed Configs
int8 speed_cmd
int8 toggle_speed_cmd
int8 gripper_pwm_cmd

")



(provide :interbotix_joy_control/ArmJoyControl "74891567b0665aa1963bdc439b948bf5")


