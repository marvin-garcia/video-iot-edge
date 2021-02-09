#!/bin/sh

# Upgrade system
# sudo apt-get update && sudo apt-get upgrade

# Update package index and install dependencies
sudo apt-get install -y \
     cmake \
     build-essential \
     pkg-config \
     python3 \
     python3-pip \
     python3-dev \
     libopenjp2-7-dev \
     zlib1g-dev \
     curl \
     wget \
     libboost-python1.62.0 \
     libcurl4-openssl-dev

# Required for OpenCV
# Hierarchical Data Format
sudo apt-get install -y libhdf5-dev libhdf5-serial-dev
# for image files
sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng-dev
# for video files
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev
# for gui
sudo apt-get install -y libqt4-test libqtgui4 libqtwebkit4 libgtk2.0-dev
# high def image processing
sudo apt-get install -y libilmbase-dev libopenexr-
# GTK development library
sudo apt-get install -y libgtk2.0-dev
# extra dependencies for matrix optimization
sudo apt-get install -y libatlas-base-dev gfortran

# Upgrade pip
python3 -m pip install -U pip

# Create virtual env
python3 -m venv .arm32v7
source .arm32v7/bin/activate
sudo -H pip3 install setuptools
sudo -H pip3 install --index-url=https://www.piwheels.org/simple -r arm32v7-requirements.txt
