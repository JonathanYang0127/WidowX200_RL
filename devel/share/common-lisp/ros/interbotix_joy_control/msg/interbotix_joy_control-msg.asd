
(cl:in-package :asdf)

(defsystem "interbotix_joy_control-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "ArmJoyControl" :depends-on ("_package_ArmJoyControl"))
    (:file "_package_ArmJoyControl" :depends-on ("_package"))
  ))