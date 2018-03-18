#!/bin/sh

if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

echo "[INFO] Running docker container with targetcli"
echo "=============================================="

docker run --privileged -v /sys/kernel/config:/sys/kernel/config -v /etc/target:/etc/target -it ubuntu_lio targetcli

echo "=============================================="
echo "[INFO] Docker session ended"
