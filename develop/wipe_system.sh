#!/bin/sh

### WIPE_SYSTEM ###

# Script closes iscsi initiator session and deletes all lio configuration

# Usage [debian]: sudo ./wipe_system.sh

if [ "$(id -u)" != "0" ]; then
    echo "[ERROR] This script must be run as root" 1>&2
    exit 1
fi

iscsiadm -m session -u
targetcli clearconfig confirm=True

