FROM nvidia/cudagl:9.0-devel-ubuntu16.04
ENV CUDNN_VERSION 7.5.1.10
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
            libcudnn7=$CUDNN_VERSION-1+cuda9.0 \
            libcudnn7-dev=$CUDNN_VERSION-1+cuda9.0 && \
    apt-mark hold libcudnn7 && \
    rm -rf /var/lib/apt/lists/*


# Installing ROS
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu xenial main" > \
    /etc/apt/sources.list.d/ros-latest.list'
RUN apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key \
    421C365BD9FF1F717815A3895523BAEEB01FA116
RUN apt-get update
RUN apt-get install -y --allow-unauthenticated ros-kinetic-desktop-full
RUN rosdep init
RUN rosdep fix-permissions
RUN rosdep update
RUN echo "source /opt/ros/kinetic/setup.bash" >> /root/.bashrc
RUN /bin/bash -c "source /root/.bashrc"
RUN apt-get install -y apt-utils
RUN apt-get install -y --allow-unauthenticated python-rosinstall python-rosinstall-generator python-wstool build-essential

RUN apt-get install -y --allow-unauthenticated ros-kinetic-moveit-* && \
	apt-get install -y --allow-unauthenticated ros-kinetic-pcl-ros


RUN apt-get install -y git libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev
RUN apt-get install -y libglfw3-dev
RUN apt-get install -y cmake
RUN apt-get install -y nano
RUN apt-get install -y vim

RUN apt-get install -y python-pip
RUN pip install --upgrade pip
RUN pip install h5py
RUN pip install scikit-learn==0.20
RUN pip install scipy
RUN pip install torch
RUN pip install torchvision
RUN pip install matplotlib==1.5.1


#install rlkit
RUN apt-get update -q \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    curl \
    git \
    libgl1-mesa-dev \
    libgl1-mesa-glx \
    libglew-dev \
    libosmesa6-dev \
    software-properties-common \
    net-tools \
    unzip \
    vim \
    virtualenv \
    wget \
    xpra \
    xserver-xorg-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


#TODO: Change to python 2.7
RUN DEBIAN_FRONTEND=noninteractive add-apt-repository --yes ppa:deadsnakes/ppa && apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install --yes python2.7-dev python2.7 python-pip
RUN virtualenv --python=python2.7 env

RUN curl -o /usr/local/bin/patchelf https://s3-us-west-2.amazonaws.com/openai-sci-artifacts/manual-builds/patchelf_0.9_amd64.elf \
    && chmod +x /usr/local/bin/patchelf

ENV LANG C.UTF-8


#COPY vendor/Xdummy /usr/local/bin/Xdummy
#RUN chmod +x /usr/local/bin/Xdummy
#RUN dpkg --configure -a


RUN apt-get update && apt-get install -y libav-tools

WORKDIR /root/
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


#Set up anaconda
RUN curl -LO https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh
RUN bash Miniconda2-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda2-latest-Linux-x86_64.sh
#COPY ./bashrc /root/.bashrc


RUN bash -c 'source ~/.bashrc'
ENV PATH=$PATH:$HOME/miniconda/bin
RUN conda init

#Copy repositories for RL
RUN mkdir /root/rl_scripts/
COPY ./doodad /root/rl_scripts/doodad
COPY ./viskit /root/rl_scripts/viskit/
COPY ./railrl-private /root/rl_scripts/railrl-private


#Create conda env
RUN conda env create -f /root/rl_scripts/railrl-private/docker/railrl_v12_cuda10-1_mj2-0-2-2_torch1-1-0_gym0-12-5_py3-6-5/railrl-env-v12.yml -n widow200
RUN bash -c 'source activate widow200'
ENV PYTHONPATH=$PYTHONPATH:/opt/ros/kinetic/lib/python2.7/dist-packages/:
RUN bash -c 'source activate widow200 && pip install -e /root/rl_scripts/viskit/'


#Copy code/repository dependencies from WidowX200_RL
RUN mkdir /root/WidowX200_RL
COPY ./src /root/WidowX200_RL/src/
COPY ./start.sh /root/WidowX200_RL
COPY ./start_webcam_server.sh /root/WidowX200_RL
RUN rm -r /root/WidowX200_RL/src/iai_kinect2

#Install gym_replab and Widowx200_RL env requirements
RUN bash -c 'source activate widow200 && pip install -e /root/WidowX200_RL/src/widowx200_rl/gym_replab/ && pip install -r /root/WidowX200_RL/src/widowx200_rl/gym_replab/requirements.txt'


#Install repository dependencies
RUN pip install modern_robotics
RUN cd /root/WidowX200_RL && \
    rosdep update && \
    rosdep install --from-paths src --ignore-src -r -y
RUN apt-get install -y --allow-unauthenticated ros-kinetic-joint-state-publisher-gui \
    ros-kinetic-effort-controllers \
    ros-kinetic-gazebo-ros-control \
    ros-kinetic-joint-state-controller \
    ros-kinetic-joint-trajectory-controller \
    ros-kinetic-dynamixel-workbench-toolbox \
    ros-kinetic-joy
#TODO: udev rules might be a bit weird



#catkin_make
RUN /bin/bash -c 'source /opt/ros/kinetic/setup.bash; cd ~/WidowX200_RL/; catkin_make clean; catkin_make -DCATKIN_ENABLE_TESTING=False -DCMAKE_BUILD_TYPE=Release; catkin_make'
RUN echo "source ~/WidowX200_RL/devel/setup.bash; cd ~/ros_ws/" >> ~/.bashrc && \
	/bin/bash -c 'source ~/.bashrc'

