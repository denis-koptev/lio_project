#!/bin/sh

# Supported for Debian based systems

if test $(id -u) != 0 ; then
	sudo su
fi

cmake .
make
make install

./tcmu-runner --handler-path $(pwd)