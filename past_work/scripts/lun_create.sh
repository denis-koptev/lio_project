#!/bin/sh

# run as su

if [ $(id -u) -ne 0 ]
	then echo "Please run as root" 
	exit
fi

# check args

if [ $# -ne 3 ]
	then echo "Wrong number of arguments. Must be 3: target iqn, HBA name, storage object name"
	exit
fi

# create lun

cd /sys/kernel/config/target/iscsi/$1/tpgt_1/lun
mkdir lun_1
cd lun_1

# create symbolic link to device

sudo ln -s /sys/kernel/config/target/core/$2/$3
