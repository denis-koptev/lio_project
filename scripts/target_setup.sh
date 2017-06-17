#!/bin/sh

# run as su

if [ $(id -u) -ne 0 ]
	then echo "Please run as root" 
	exit
fi

# check args

if [ $# -ne 2 ]
	then echo "Wrong number of arguments. Must be 2: target iqn, initiator iqn"
	exit
fi

# create iqn

cd /sys/kernel/config/target/iscsi
mkdir $1
cd $1

# create target portal group

mkdir tpgt_1
cd tpgt_1

# enable target

echo 1 > enable

# create acls



# create lun

#cd /sys/kernel/config/target/iscsi/$1/tpgt_1/lun
#mkdir lun_1
#cd lun_1