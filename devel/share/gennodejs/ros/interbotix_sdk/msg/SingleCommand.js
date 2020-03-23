// Auto-generated. Do not edit!

// (in-package interbotix_sdk.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class SingleCommand {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.joint_name = null;
      this.cmd = null;
    }
    else {
      if (initObj.hasOwnProperty('joint_name')) {
        this.joint_name = initObj.joint_name
      }
      else {
        this.joint_name = '';
      }
      if (initObj.hasOwnProperty('cmd')) {
        this.cmd = initObj.cmd
      }
      else {
        this.cmd = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type SingleCommand
    // Serialize message field [joint_name]
    bufferOffset = _serializer.string(obj.joint_name, buffer, bufferOffset);
    // Serialize message field [cmd]
    bufferOffset = _serializer.float64(obj.cmd, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type SingleCommand
    let len;
    let data = new SingleCommand(null);
    // Deserialize message field [joint_name]
    data.joint_name = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [cmd]
    data.cmd = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.joint_name.length;
    return length + 12;
  }

  static datatype() {
    // Returns string type for a message object
    return 'interbotix_sdk/SingleCommand';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '6d45868a3dac16da3c97708e8cdbf2c6';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # Send a command to the specified joint
    #
    # 'joint_name' is the name of the joint to control (any of the motor names listed
    # in the 'order' or 'singles' lists located in a motor config file - except for shadow motors)
    # 'cmd' can be a position [rad], velocity [rad/s], current [mA], or pwm depending on what operating
    # mode the joint is currently set at.
    #
    # Note that the gripper can be controlled by publishing this type of message to the
    # /<robot_name>/single_joint/command topic as well. There are two main differences between using
    # this topic and the /<robot_name>/gripper/command topic for controlling the gripper:
    #   1) By publishing to the /<robot_name>/gripper/command topic, you do not have to specify that you
    #      are commanding the gripper - it's automatically understood.
    #   2) When the gripper is in "position" control, using the /<robot_name>/gripper/command topic specifies a
    #      linear distance in meters between the gripper fingers. However, using the /<robot_name>/single_joint/command
    #      topic specifies an angular distance in radians.
    
    string joint_name
    float64 cmd
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new SingleCommand(null);
    if (msg.joint_name !== undefined) {
      resolved.joint_name = msg.joint_name;
    }
    else {
      resolved.joint_name = ''
    }

    if (msg.cmd !== undefined) {
      resolved.cmd = msg.cmd;
    }
    else {
      resolved.cmd = 0.0
    }

    return resolved;
    }
};

module.exports = SingleCommand;
