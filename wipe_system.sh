#!/bin/sh

### WIPE_SYSTEM ###

# Script closes iscsi initiator session and deletes all lio configuration

# Usage [debian]: sudo ./wipe_system.sh

if [ "$(id -u)" != "0" ]; then
    echo "[ERROR] This script must be run as root" 1>&2
    exit 1
fi

echo "[INFO] Logging out of all possible iSCSI sessions"
iscsiadm -m session -u

echo "[INFO] Clearing target configuration via targetcli"
targetcli clearconfig confirm=True

echo "[INFO] Deleting tcmu-runner build products"
cd tcmu-runner
if [ -f CMakeCache.txt ]; then
    rm CMakeCache.txt
fi;
make clean

echo "[INFO] Stopping tcmu-runner.service"
systemctl stop tcmu-runner.service

echo "[INFO] Restarting targetctl.service"
systemctl stop rtslib-fb-targetctl.service
systemctl start rtslib-fb-targetctl.service

