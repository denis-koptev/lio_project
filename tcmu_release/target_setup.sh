#!/bin/sh

# Script that sets up device to existing target
# Creates lun

# Input arguments required:
## 1. Target IQN
## 2. Backstore path (got from user_create script)
# Example: ./target_setup.sh iqn.2017-07.com.example:target user_0/test

# run as su

# run as superuser

if [ $(id -u) -ne 0 ]
	then echo "[ERROR] Permission denied. Please run as superuser." 
	exit
fi

# check arguments

if [ $# -ne 2 ]
then echo "[ERROR]		Wrong number of arguments. Must be 2."
	 echo "[ARGUMENTS]	target IQN, backstore path."
	 echo "[EXAMPLE]	./target_setup.sh iqn.2017-07.com.example:target user_0/test"
     exit
fi

cd /sys/kernel/config/target/iscsi/$1/tpgt_1

# generate next lun

cd lun
dir_name=lun_
idx=0

# if folder already exists, find next name that is not yet taken

while true; do
    lun_name=$dir_name$idx
    if [ ! -d $lun_name ]; then
        mkdir $lun_name
        break
    fi
    idx=$(($idx + 1))
done

cd $lun_name

ln -s /sys/kernel/config/target/core/$2
cd ../..

# create acls (only for loopback configuration)

cd acls
init_name=`grep '^InitiatorName=' /etc/iscsi/initiatorname.iscsi | sed 's/\(.*\)InitiatorName=\s*\(.*\)/\1\2/'`
cd $init_name

mkdir $lun_name
cd $lun_name
ln -s /sys/kernel/config/target/iscsi/$1/tpgt_1/lun/$lun_name/