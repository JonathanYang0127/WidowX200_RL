// Auto-generated. Do not edit!

// (in-package interbotix_turret_control.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class TurretJoyControl {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.pan_cmd = null;
      this.tilt_cmd = null;
      this.speed_cmd = null;
      this.toggle_speed_cmd = null;
    }
    else {
      if (initObj.hasOwnProperty('pan_cmd')) {
        this.pan_cmd = initObj.pan_cmd
      }
      else {
        this.pan_cmd = 0;
      }
      if (initObj.hasOwnProperty('tilt_cmd')) {
        this.tilt_cmd = initObj.tilt_cmd
      }
      else {
        this.tilt_cmd = 0;
      }
      if (initObj.hasOwnProperty('speed_cmd')) {
        this.speed_cmd = initObj.speed_cmd
      }
      else {
        this.speed_cmd = 0;
      }
      if (initObj.hasOwnProperty('toggle_speed_cmd')) {
        this.toggle_speed_cmd = initObj.toggle_speed_cmd
      }
      else {
        this.toggle_speed_cmd = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type TurretJoyControl
    // Serialize message field [pan_cmd]
    bufferOffset = _serializer.int8(obj.pan_cmd, buffer, bufferOffset);
    // Serialize message field [tilt_cmd]
    bufferOffset = _serializer.int8(obj.tilt_cmd, buffer, bufferOffset);
    // Serialize message field [speed_cmd]
    bufferOffset = _serializer.int8(obj.speed_cmd, buffer, bufferOffset);
    // Serialize message field [toggle_speed_cmd]
    bufferOffset = _serializer.int8(obj.toggle_speed_cmd, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type TurretJoyControl
    let len;
    let data = new TurretJoyControl(null);
    // Deserialize message field [pan_cmd]
    data.pan_cmd = _deserializer.int8(buffer, bufferOffset);
    // Deserialize message field [tilt_cmd]
    data.tilt_cmd = _deserializer.int8(buffer, bufferOffset);
    // Deserialize message field [speed_cmd]
    data.speed_cmd = _deserializer.int8(buffer, bufferOffset);
    // Deserialize message field [toggle_speed_cmd]
    data.toggle_speed_cmd = _deserializer.int8(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'interbotix_turret_control/TurretJoyControl';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'f699b95ec0a0298bd77c4a4d7f52404f';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # Send commands from the joy_node to the turret_control node
    
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new TurretJoyControl(null);
    if (msg.pan_cmd !== undefined) {
      resolved.pan_cmd = msg.pan_cmd;
    }
    else {
      resolved.pan_cmd = 0
    }

    if (msg.tilt_cmd !== undefined) {
      resolved.tilt_cmd = msg.tilt_cmd;
    }
    else {
      resolved.tilt_cmd = 0
    }

    if (msg.speed_cmd !== undefined) {
      resolved.speed_cmd = msg.speed_cmd;
    }
    else {
      resolved.speed_cmd = 0
    }

    if (msg.toggle_speed_cmd !== undefined) {
      resolved.toggle_speed_cmd = msg.toggle_speed_cmd;
    }
    else {
      resolved.toggle_speed_cmd = 0
    }

    return resolved;
    }
};

// Constants for message
TurretJoyControl.Constants = {
  PAN_CCW: 1,
  PAN_CW: 2,
  TILT_UP: 3,
  TILT_DOWN: 4,
  PAN_TILT_HOME: 5,
  SPEED_INC: 6,
  SPEED_DEC: 7,
  SPEED_COURSE: 8,
  SPEED_FINE: 9,
}

module.exports = TurretJoyControl;
