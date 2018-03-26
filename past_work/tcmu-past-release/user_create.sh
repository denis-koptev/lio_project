#!/bin/sh

# Script for user-backstores creation
# Creates entries in sysfs for backstore device

# Input arguments required:
## 1. Handler type (file/alloc)
## 2. Device name (must be unique for one target)
## 3. Device (file or memory) size
# Example: ./user_create.sh alloc test_dev 1048576

# run as superuser

if [ $(id -u) -ne 0 ]
	then echo "[ERROR] Permission denied. Please run as superuser." 
	exit
fi

# check arguments

if [ $# -ne 3 ]
then echo "[ERROR]		Wrong number of arguments. Must be 3."
	 echo "[ARGUMENTS]	handler type, device name, device size."
	 echo "[EXAMPLE]	./user_create.sh alloc test_dev 1048576"
     exit
fi

# check that target_core_user module is loaded

if ! (lsmod | grep -q target_core_user); then
	echo "[ERROR] target_core_user module is not loaded" 
	exit
fi

# create backstore object in sysfs

cd /sys/kernel/config/target/core

# generate next user backstore

dir_name=user_
idx=0

# if folder already exists, find next name that is not yet taken

while true; do
    temp_name=$dir_name$idx
    if [ ! -d $temp_name ]; then
        mkdir $temp_name
        break
    fi
    idx=$(($idx + 1))
done

cd $temp_name
mkdir $2
cd $2

# configuration

echo -n dev_size=$3 > control
echo -n dev_config=$1/$2 > control
echo -n 1 > enable

# use this info to setup target for device using target_setup script

echo "[INFO] Your backstore directory: $temp_name/$2"
