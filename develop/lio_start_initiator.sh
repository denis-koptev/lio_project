#!/bin/sh

# Arg: path/to/config.json

if [ "$(id -u)" != "0" ]; then
    echo "[ERROR] This script must be run as root" 1>&2
    exit 1
fi

if [ "$#" -ne 1 ]; then
    echo "[ERROR] Invalid count of arguments"
    echo "[INFO] Usage (as root): ./lio_start_initiator.sh /path/to/config.json"
    exit 1
fi

# Registering initiator IQN
python3 lio_start_initiator.py $1

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to register Initiator IQN"
    exit 1
fi

echo "[INFO] Attempting to descover targets and log in"

TARGET_IP=`cat session/target_ip`

iscsiadm -m discovery -t sendtargets -p $TARGET_IP

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to discover targets"
    exit 1
fi

iscsiadm -m node --login -p $TARGET_IP:3260

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to log in to target"
    exit 1
fi

lsscsi > session/initdev

python3 parse_dev.py session/initdev # Only for host initiator TODO: modify it for container

iscsiadm -m session -u
