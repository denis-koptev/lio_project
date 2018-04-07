#!/bin/sh

# Supported for Debian based systems

if test $(id -u) != 0 ; then
	SUDO=sudo
fi

$SUDO apt-get install -y cmake make gcc libglib2.0-dev
$SUDO apt-get install -y libkmod-dev libpthread-*
$SUDO apt-get install -y libnl-genl-3-dev
