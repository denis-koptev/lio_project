#!/bin/sh

if [ "$(id -u)" != "0" ]; then
    echo "[ERROR] This script must be run as root" 1>&2
    exit 1
fi

if [ "$#" -ne 1 ]; then
    echo "[ERROR] Invalid count of arguments"
    echo "[INFO] Usage: ./lio_start_session.sh /path/to/config.json"
    exit 1
fi

CONFIG=$1

if [ ! -f $CONFIG ]; then
    echo "[ERROR] Specified config does not exist."
    exit 1
fi

if [ -d "./session" ]; then
    echo "[INFO] Previous session directory exists. It will be recreated."
    rm -rf ./session
fi

mkdir ./session

echo "[INFO] Creating internal configs for target and initiators in ./session"
python3 lio_parse_json.py $CONFIG --workdir ./session

if [ $? -ne 0 ]; then
    echo "Exiting..."
    exit 1
fi

echo "[INFO] Waiting for target docker container to start..."
echo "[INFO] Mounted folders: /sys/kernel/config, /etc/target, `pwd`/session"
docker run --privileged -v /sys/kernel/config:/sys/kernel/config -v /etc/target:/etc/target -v `pwd`:/lio_project -it deniskoptev/lio_target 

RETRIES=10
while [ ! -f session/tgt_ip && $RETRIES -ne 0 ];
do
    echo "[INFO] Waiting for docker target container to start: $RETRIES"
    # insert sleep
    # insert math expr
done

# When all work will be finished
# rm -rf ./session
