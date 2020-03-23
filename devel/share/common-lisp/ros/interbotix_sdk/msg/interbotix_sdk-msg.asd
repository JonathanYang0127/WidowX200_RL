
(cl:in-package :asdf)

(defsystem "interbotix_sdk-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "JointCommands" :depends-on ("_package_JointCommands"))
    (:file "_package_JointCommands" :depends-on ("_package"))
    (:file "SingleCommand" :depends-on ("_package_SingleCommand"))
    (:file "_package_SingleCommand" :depends-on ("_package"))
  ))