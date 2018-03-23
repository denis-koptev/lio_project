#!/bin/sh

# Supported for Debian based systems

if test $(id -u) != 0 ; then
	SUDO=sudo
fi

$SUDO apt-get install -y cmake make gcc libnl-3-dev libglib2.0-dev zlib1g-dev
$SUDO apt-get install -y libkmod-dev libpthread-* libdlib-dev libkmod-dev
$SUDO apt-get install -y libnl-genl-3-dev librbd-dev
