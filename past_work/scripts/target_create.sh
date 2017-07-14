#!/bin/sh

# run as su

if [ $(id -u) -ne 0 ]
	then echo "Please run as root" 
	exit
fi

# check args

if [ $# -ne 1 ]
	then echo "Wrong number of arguments. Must be 1: target iqn"
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
