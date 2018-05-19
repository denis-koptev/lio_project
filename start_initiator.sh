#!/bin/bash

# Arg: path/to/config.json

echo "----- ENTERING START_INITIATOR SCRIPT -----"

if [ "$(id -u)" != "0" ]; then
    echo "[ERROR] This script must be run as root" 1>&2
    exit 1
fi

if [ "$#" -ne 1 ]; then
    echo "[ERROR] Invalid count of arguments"
    echo "[INFO] Usage (as root): ./lio_start_initiator.sh /path/to/config.json"
    exit 1
fi

EMPTY=""
INITCONF=$1
DEVCONF=${INITCONF/.json/$EMPTY}_dev
LOG=${INITCONF/.json/$EMPTY}_log
IO=${INITCONF/.json/$EMPTY}_io_log
IORESULT=${INITCONF/.json/$EMPTY}_io_result

# Registering initiator IQN
./start_initiator.py $INITCONF --log $LOG

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to register Initiator IQN"
    exit 1
fi

echo "[INFO] Attempting to discover targets and log in"

TARGET_IP=`cat session/target_ip`

iscsiadm -m discovery -t sendtargets -p $TARGET_IP --login

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to discover targets and log in"
    exit 1
fi

#iscsiadm -m node --login -p $TARGET_IP:3260

#if [ $? -ne 0 ]; then
#    echo "[ERROR] Failed to log in to target"
#    exit 1
#fi

sleep 1 # Sometimes devices can be created slowly and we need to wait

echo "[INFO] Creating a file with the list of iSCSI devices: $DEVCONF"

lsscsi > $DEVCONF

if [ $? -ne 0 ]; then
    echo "[ERROR] Error creating device file. Maybe you don't have lsscsi tool installed"
    iscsiadm -m session -u
    exit 1
fi

echo "[INFO] Starting IO operations to devices"

./run_io.py $DEVCONF $1 --result $IORESULT #--log $IO

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to proceed IO"
    iscsiadm -m session -u
    exit 1
fi

echo "[INFO] IO operations finished normally"
echo "[INFO] Logging out of session"

iscsiadm -m session -u

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to log out of session"
    echo "[WARNING] You probably should reboot your system"
    exit 1
fi

