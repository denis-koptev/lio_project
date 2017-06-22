#!/bin/sh

# run as su

if [ $(id -u) -ne 0 ]
	then echo "Please run as root" 
	exit
fi

# check args

# create file

touch /home/denis/test_file
echo 1234567989abcdefg > /home/denis/test_file

# create backstore

cd /sys/kernel/config/target/core
mkdir fileio_0
cd fileio_0
mkdir test_dev
cd test_dev
echo "fd_dev_name=/home/denis/test_file,fd_dev_size=1048576" > control
echo 1 > enable

# create iqn

cd /sys/kernel/config/target/iscsi
mkdir iqn.2017-06.com.example:target
cd iqn.2017-06.com.example:target

# create target portal group

mkdir tpgt_1
cd tpgt_1

# enable target

echo 1 > enable

# create lun

cd lun
mkdir lun_0
cd lun_0
ln -s /sys/kernel/config/target/core/fileio_0/test_dev/
cd ../..

# create acls

cd acls
mkdir iqn.1993-08.org.debian:01:ef2e26bf3a9e
mkdir lun_0
cd lun_0
ln -s /sys/kernel/config/target/iscsi/iqn2017-06.com.example\:target/tpgt_1/lun/lun_0/
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