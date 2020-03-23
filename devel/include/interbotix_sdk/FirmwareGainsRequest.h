// Generated by gencpp from file interbotix_sdk/FirmwareGainsRequest.msg
// DO NOT EDIT!


#ifndef INTERBOTIX_SDK_MESSAGE_FIRMWAREGAINSREQUEST_H
#define INTERBOTIX_SDK_MESSAGE_FIRMWAREGAINSREQUEST_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace interbotix_sdk
{
template <class ContainerAllocator>
struct FirmwareGainsRequest_
{
  typedef FirmwareGainsRequest_<ContainerAllocator> Type;

  FirmwareGainsRequest_()
    : joint_id(0)
    , Kp_pos()
    , Ki_pos()
    , Kd_pos()
    , K1()
    , K2()
    , Kp_vel()
    , Ki_vel()  {
    }
  FirmwareGainsRequest_(const ContainerAllocator& _alloc)
    : joint_id(0)
    , Kp_pos(_alloc)
    , Ki_pos(_alloc)
    , Kd_pos(_alloc)
    , K1(_alloc)
    , K2(_alloc)
    , Kp_vel(_alloc)
    , Ki_vel(_alloc)  {
  (void)_alloc;
    }



   typedef int8_t _joint_id_type;
  _joint_id_type joint_id;

   typedef std::vector<int32_t, typename ContainerAllocator::template rebind<int32_t>::other >  _Kp_pos_type;
  _Kp_pos_type Kp_pos;

   typedef std::vector<int32_t, typename ContainerAllocator::template rebind<int32_t>::other >  _Ki_pos_type;
  _Ki_pos_type Ki_pos;

   typedef std::vector<int32_t, typename ContainerAllocator::template rebind<int32_t>::other >  _Kd_pos_type;
  _Kd_pos_type Kd_pos;

   typedef std::vector<int32_t, typename ContainerAllocator::template rebind<int32_t>::other >  _K1_type;
  _K1_type K1;

   typedef std::vector<int32_t, typename ContainerAllocator::template rebind<int32_t>::other >  _K2_type;
  _K2_type K2;

   typedef std::vector<int32_t, typename ContainerAllocator::template rebind<int32_t>::other >  _Kp_vel_type;
  _Kp_vel_type Kp_vel;

   typedef std::vector<int32_t, typename ContainerAllocator::template rebind<int32_t>::other >  _Ki_vel_type;
  _Ki_vel_type Ki_vel;





  typedef boost::shared_ptr< ::interbotix_sdk::FirmwareGainsRequest_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::interbotix_sdk::FirmwareGainsRequest_<ContainerAllocator> const> ConstPtr;

}; // struct FirmwareGainsRequest_

typedef ::interbotix_sdk::FirmwareGainsRequest_<std::allocator<void> > FirmwareGainsRequest;

typedef boost::shared_ptr< ::interbotix_sdk::FirmwareGainsRequest > FirmwareGainsRequestPtr;
typedef boost::shared_ptr< ::interbotix_sdk::FirmwareGainsRequest const> FirmwareGainsRequestConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::interbotix_sdk::FirmwareGainsRequest_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::interbotix_sdk::FirmwareGainsRequest_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace interbotix_sdk

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': False}
// {'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg'], 'interbotix_sdk': ['/home/jonathan/Desktop/Projects/WidowX200_RL/src/interbotix_ros_arms/interbotix_sdk/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::interbotix_sdk::FirmwareGainsRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::interbotix_sdk::FirmwareGainsRequest_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::interbotix_sdk::FirmwareGainsRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::interbotix_sdk::FirmwareGainsRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::interbotix_sdk::FirmwareGainsRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::interbotix_sdk::FirmwareGainsRequest_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::interbotix_sdk::FirmwareGainsRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "1a3c17ff4352d3a3bf5d6c64d4bd58a6";
  }

  static const char* value(const ::interbotix_sdk::FirmwareGainsRequest_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x1a3c17ff4352d3a3ULL;
  static const uint64_t static_value2 = 0xbf5d6c64d4bd58a6ULL;
};

template<class ContainerAllocator>
struct DataType< ::interbotix_sdk::FirmwareGainsRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "interbotix_sdk/FirmwareGainsRequest";
  }

  static const char* value(const ::interbotix_sdk::FirmwareGainsRequest_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::interbotix_sdk::FirmwareGainsRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "\n\
\n\
\n\
\n\
\n\
\n\
\n\
\n\
\n\
\n\
\n\
\n\
\n\
\n\
\n\
\n\
\n\
int8 joint_id\n\
\n\
\n\
\n\
\n\
int32[] Kp_pos\n\
int32[] Ki_pos\n\
int32[] Kd_pos\n\
\n\
\n\
\n\
\n\
int32[] K1\n\
int32[] K2\n\
\n\
\n\
\n\
int32[] Kp_vel\n\
int32[] Ki_vel\n\
";
  }

  static const char* value(const ::interbotix_sdk::FirmwareGainsRequest_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::interbotix_sdk::FirmwareGainsRequest_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.joint_id);
      stream.next(m.Kp_pos);
      stream.next(m.Ki_pos);
      stream.next(m.Kd_pos);
      stream.next(m.K1);
      stream.next(m.K2);
      stream.next(m.Kp_vel);
      stream.next(m.Ki_vel);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct FirmwareGainsRequest_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::interbotix_sdk::FirmwareGainsRequest_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::interbotix_sdk::FirmwareGainsRequest_<ContainerAllocator>& v)
  {
    s << indent << "joint_id: ";
    Printer<int8_t>::stream(s, indent + "  ", v.joint_id);
    s << indent << "Kp_pos[]" << std::endl;
    for (size_t i = 0; i < v.Kp_pos.size(); ++i)
    {
      s << indent << "  Kp_pos[" << i << "]: ";
      Printer<int32_t>::stream(s, indent + "  ", v.Kp_pos[i]);
    }
    s << indent << "Ki_pos[]" << std::endl;
    for (size_t i = 0; i < v.Ki_pos.size(); ++i)
    {
      s << indent << "  Ki_pos[" << i << "]: ";
      Printer<int32_t>::stream(s, indent + "  ", v.Ki_pos[i]);
    }
    s << indent << "Kd_pos[]" << std::endl;
    for (size_t i = 0; i < v.Kd_pos.size(); ++i)
    {
      s << indent << "  Kd_pos[" << i << "]: ";
      Printer<int32_t>::stream(s, indent + "  ", v.Kd_pos[i]);
    }
    s << indent << "K1[]" << std::endl;
    for (size_t i = 0; i < v.K1.size(); ++i)
    {
      s << indent << "  K1[" << i << "]: ";
      Printer<int32_t>::stream(s, indent + "  ", v.K1[i]);
    }
    s << indent << "K2[]" << std::endl;
    for (size_t i = 0; i < v.K2.size(); ++i)
    {
      s << indent << "  K2[" << i << "]: ";
      Printer<int32_t>::stream(s, indent + "  ", v.K2[i]);
    }
    s << indent << "Kp_vel[]" << std::endl;
    for (size_t i = 0; i < v.Kp_vel.size(); ++i)
    {
      s << indent << "  Kp_vel[" << i << "]: ";
      Printer<int32_t>::stream(s, indent + "  ", v.Kp_vel[i]);
    }
    s << indent << "Ki_vel[]" << std::endl;
    for (size_t i = 0; i < v.Ki_vel.size(); ++i)
    {
      s << indent << "  Ki_vel[" << i << "]: ";
      Printer<int32_t>::stream(s, indent + "  ", v.Ki_vel[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // INTERBOTIX_SDK_MESSAGE_FIRMWAREGAINSREQUEST_H
