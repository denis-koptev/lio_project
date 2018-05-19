#!/bin/sh

### LIO_START_SESSION ###

# Main script to run the whole lio session.
# Includes creating devices, target and initiators; making IO operations.

# Usage [debian]: sudo ./lio_start_session.sh /path/to/json

if [ "$(id -u)" != "0" ]; then
    echo "[ERROR] This script must be run as root" 1>&2
    exit 1
fi

if [ "$#" -ne 1 ]; then
    echo "[ERROR] Invalid count of arguments"
    echo "[INFO] Usage (as root): ./lio_start_session.sh /path/to/config.json"
    exit 1
fi

echo "================================================="
echo "====== WELCOME TO LIO-SESSION START SCRIPT ======"
echo "================================================="

# User-side configuration file with JSON

CONFIG=$1

if [ ! -f $CONFIG ]; then
    echo "[ERROR] Specified config does not exist."
    exit 1
fi

# Session directory content #
# All internal configs, generated by lio_parse_json.py script
# File with target IP indicating that it was launched successfully
# Log files from creation and work processes (devices, target, initiators)

if [ -d "./session" ]; then
    echo "[INFO] Previous session directory exists. It will be recreated."
    rm -rf ./session
fi

mkdir ./session

# Internal JSON configs #
# In user-side config only high-level info is provided.
# All internal details (i.e.: IQNs and LUNs) are generated by python script
# Configs will be placed in session directory

echo "[INFO] Creating internal configs for target and initiators in ./session"
./parse_json.py $CONFIG --workdir ./session

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create JSON configs. Exiting..."
    exit 1
fi

# Launch target start up #
# tcmu-runner will be compiled and started as a daemon
# Configuration (corresponding to JSON) will be deployed
# Creation of file with IP address indicates, that target started normally

./start_target.sh

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to start target. Exiting..."
    exit 1
fi

if [ ! -f session/target_ip ]; then
    echo "[ERROR] Failed to start target: no file with IP. Exiting..."
    exit 1
fi

echo "[INFO] Target IP address: `cat session/target_ip`"

# Deploy initiators #
# All initiator config names are starting with 'initconf' prefix
# So, they all can be found and collected
# For each config new docker container will be started

#echo "[INFO] Launching initiators."
#for config in session/initconf*.json; do
#    echo $config
# Need to think how to pass iqn and other staff to docker
# docker run -v `pwd`:/lio_project -d deniskoptev/lio_initiator ./lio_project/lio_start_initiator.sh $config
#done

echo "[INFO] Launching host-initiator"
./start_initiator.sh session/initconf_init1.json

if [ $? -ne 0 ]; then
    echo "[WARNING] There were errors in initiators' work"
    exit 1
fi

echo "[INFO] LIO SESSION ENDED NORMALLY"

