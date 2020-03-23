
(cl:in-package :asdf)

(defsystem "interbotix_turret_control-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "TurretJoyControl" :depends-on ("_package_TurretJoyControl"))
    (:file "_package_TurretJoyControl" :depends-on ("_package"))
  ))