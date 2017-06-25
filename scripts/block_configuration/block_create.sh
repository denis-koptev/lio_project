#!/bin/sh

# run as su

if [ $(id -u) -ne 0 ]
	then echo "Please run as root" 
	exit
fi

# check args

if [ $# -ne 2 ]
	then echo "Wrong number of arguments. Must be 3: dir/blockdev_name, iblock dev name"
	exit
fi

# create lvm (lwm2 should be installed)

truncate --size 10M $1
dev_path=`losetup --find --show $1`
vgcreate vol_group $dev_path
lvcreate --size 4M --name log_vol vol_group

# create backstore for target

cd /sys/kernel/config/target/core

# generate next fileio folder

dir_name=iblock_
idx=0

# If file already exists, find next dir_name that is not yet taken
while true; do
    temp_name=$dir_name$idx
    if [ ! -d $temp_name ]; then
        mkdir $temp_name
        break
    fi
    idx=$(($idx + 1))
done

# create device

cd $temp_name
mkdir $2 # dev name
cd $2

echo "Your backstore path: $temp_name/$2"

# configure device

#echo "fd_dev_name=$1,fd_dev_size=$3" > control ???
echo "udev_path=/dev/vol_group/log_vol"
echo 1 > enable