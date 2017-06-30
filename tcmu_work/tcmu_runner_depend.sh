#!/bin/sh

if [ $(id -u) -ne 0 ]
	then echo "Please run as root" 
	exit
fi

apt-get install cmake
apt-get install libnl-3-dev
apt-get install libglib2.0-dev
apt-get install libpthread-*
apt-get install libdlib-dev
apt-get install libkmod-dev
apt-get install glusterfs-*
apt-get install librbd*
apt-get install zlib*
apt-get install libnl-genl-3-dev