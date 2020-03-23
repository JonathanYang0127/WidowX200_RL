#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/jonathan/Desktop/Projects/WidowX200_RL/src/interbotix_ros_arms/interbotix_descriptions"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/jonathan/Desktop/Projects/WidowX200_RL/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/jonathan/Desktop/Projects/WidowX200_RL/install/lib/python2.7/dist-packages:/home/jonathan/Desktop/Projects/WidowX200_RL/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/jonathan/Desktop/Projects/WidowX200_RL/build" \
    "/usr/bin/python2" \
    "/home/jonathan/Desktop/Projects/WidowX200_RL/src/interbotix_ros_arms/interbotix_descriptions/setup.py" \
    build --build-base "/home/jonathan/Desktop/Projects/WidowX200_RL/build/interbotix_ros_arms/interbotix_descriptions" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/jonathan/Desktop/Projects/WidowX200_RL/install" --install-scripts="/home/jonathan/Desktop/Projects/WidowX200_RL/install/bin"
