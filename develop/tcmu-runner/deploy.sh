#!/bin/sh

echo "Running CMake for tcmu-runner without qcow, rbd and glfs..."
cmake -Dwith-glfs=false -Dwith-qcow=false -Dwith-rbd=false -DSUPPORT_SYSTEMD=ON -DCMAKE_INSTALL_PREFIX=/usr .

echo "Running make to build tcmu-runner..."
echo "Note: if you have problems with iovec definitions, \
    replace <linux/uio.h> with <sys/uio.h> in target_core_user_local.h"
make

echo "Running make install..."
make install

echo "Setting up tcmu-runner service..."
cp tcmu-runner.conf /etc/dbus-1/system.d/
cp org.kernel.TCMUService1.service /usr/share/dbus-1/system-services/
cp tcmu-runner.service /lib/systemd/system

echo "Starting service..."
service tcmu-runner start
#systemctl daemon-reload
