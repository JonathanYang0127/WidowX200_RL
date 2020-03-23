// Generated by gencpp from file interbotix_sdk/RegisterValuesResponse.msg
// DO NOT EDIT!


#ifndef INTERBOTIX_SDK_MESSAGE_REGISTERVALUESRESPONSE_H
#define INTERBOTIX_SDK_MESSAGE_REGISTERVALUESRESPONSE_H


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
struct RegisterValuesResponse_
{
  typedef RegisterValuesResponse_<ContainerAllocator> Type;

  RegisterValuesResponse_()
    : values()  {
    }
  RegisterValuesResponse_(const ContainerAllocator& _alloc)
    : values(_alloc)  {
  (void)_alloc;
    }



   typedef std::vector<int32_t, typename ContainerAllocator::template rebind<int32_t>::other >  _values_type;
  _values_type values;





  typedef boost::shared_ptr< ::interbotix_sdk::RegisterValuesResponse_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::interbotix_sdk::RegisterValuesResponse_<ContainerAllocator> const> ConstPtr;

}; // struct RegisterValuesResponse_

typedef ::interbotix_sdk::RegisterValuesResponse_<std::allocator<void> > RegisterValuesResponse;

typedef boost::shared_ptr< ::interbotix_sdk::RegisterValuesResponse > RegisterValuesResponsePtr;
typedef boost::shared_ptr< ::interbotix_sdk::RegisterValuesResponse const> RegisterValuesResponseConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::interbotix_sdk::RegisterValuesResponse_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::interbotix_sdk::RegisterValuesResponse_<ContainerAllocator> >::stream(s, "", v);
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
struct IsFixedSize< ::interbotix_sdk::RegisterValuesResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::interbotix_sdk::RegisterValuesResponse_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::interbotix_sdk::RegisterValuesResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::interbotix_sdk::RegisterValuesResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::interbotix_sdk::RegisterValuesResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::interbotix_sdk::RegisterValuesResponse_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::interbotix_sdk::RegisterValuesResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "5dd1053b3769329bd3895728a55810d3";
  }

  static const char* value(const ::interbotix_sdk::RegisterValuesResponse_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x5dd1053b3769329bULL;
  static const uint64_t static_value2 = 0xd3895728a55810d3ULL;
};

template<class ContainerAllocator>
struct DataType< ::interbotix_sdk::RegisterValuesResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "interbotix_sdk/RegisterValuesResponse";
  }

  static const char* value(const ::interbotix_sdk::RegisterValuesResponse_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::interbotix_sdk::RegisterValuesResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "int32[] values\n\
\n\
";
  }

  static const char* value(const ::interbotix_sdk::RegisterValuesResponse_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::interbotix_sdk::RegisterValuesResponse_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.values);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct RegisterValuesResponse_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::interbotix_sdk::RegisterValuesResponse_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::interbotix_sdk::RegisterValuesResponse_<ContainerAllocator>& v)
  {
    s << indent << "values[]" << std::endl;
    for (size_t i = 0; i < v.values.size(); ++i)
    {
      s << indent << "  values[" << i << "]: ";
      Printer<int32_t>::stream(s, indent + "  ", v.values[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // INTERBOTIX_SDK_MESSAGE_REGISTERVALUESRESPONSE_H
