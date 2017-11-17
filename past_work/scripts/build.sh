#!/bin/sh

if [ $(id -u) -ne 0 ]
	then echo "Please run as root" 
	exit
fi

apt-get install -y cmake
apt-get install -y libnl-3-dev
apt-get install -y libglib2.0-dev
apt-get install -y libpthread-*
apt-get install -y libdlib-dev
apt-get install -y libkmod-dev
apt-get install -y zlib*
apt-get install -y libnl-genl-3-dev

cmake .
make

cp tcmu-runner.conf /etc/dbus-1/system.d/tcmu-runner.conf
cp tcmu-runner /usr/bin/tcmu-runner
mkdir /etc/tcmu
cp tcmu.conf /etc/tcmu/tcmu.conf