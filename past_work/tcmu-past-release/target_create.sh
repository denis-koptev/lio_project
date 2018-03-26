#!/bin/sh

# Script for target creation
# Generates IQN form current data and time
# Creates standard portal 127.0.0.1:3260
# Creates ACL for loopback configuration
# Turns off authorization

# No arguments required

# run as superuser

if [ $(id -u) -ne 0 ]
	then echo "[ERROR] Permission denied. Please run as superuser." 
	exit
fi

# check that target driver is loaded

if ! (lsmod | grep -q target); then
	echo "[ERROR] Target driver is not loaded" 
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

# create ACL for loopback configuration

cd acls
init_name=`grep '^InitiatorName=' /etc/iscsi/initiatorname.iscsi | sed 's/\(.*\)InitiatorName=\s*\(.*\)/\1\2/'`
mkdir $init_name
cd ..

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

# info

echo "[INFO] Target $iqn_name created"
echo "[INFO] Portal: 127.0.0.1:3260"