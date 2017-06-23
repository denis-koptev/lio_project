#!/bin/sh

# run as su

if [ $(id -u) -ne 0 ]
	then echo "Please run as root" 
	exit
fi

# check args

if [ $# -ne 1 ]
	then echo "Wrong number of arguments. Must be 1: backstore path"
	exit
fi

# create iqn

cd /sys/kernel/config/target/iscsi
iqn_name=iqn.$(date +%Y-%m).com.test:target-$(date +%d-%H-%M)
mkdir $iqn_name
cd $iqn_name

# create target portal group

mkdir tpgt_1
cd tpgt_1

# enable target

echo 1 > enable

# create lun

cd lun
mkdir lun_0
cd lun_0
ln -s /sys/kernel/config/target/core/$1
cd ../..

# create acls

cd acls

init_name=`grep '^InitiatorName=' /etc/iscsi/initiatorname.iscsi | sed 's/\(.*\)InitiatorName=\s*\(.*\)/\1\2/'`

mkdir $init_name
cd $init_name
mkdir lun_0
cd lun_0
ln -s /sys/kernel/config/target/iscsi/$iqn_name/tpgt_1/lun/lun_0/
cd ../../..

# set auth params to None

cd attrib
echo 0 > authentication
cd ..

cd param
echo None > AuthMethod
cd ..

# create portal

cd np
mkdir 0.0.0.0:3260