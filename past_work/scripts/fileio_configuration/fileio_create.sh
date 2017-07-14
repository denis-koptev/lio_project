#!/bin/sh

# run as su

if [ $(id -u) -ne 0 ]
	then echo "Please run as root" 
	exit
fi

# check args

if [ $# -ne 3 ]
	then echo "Wrong number of arguments. Must be 3: dir/filename, fileio dev name, size"
	exit
fi

# create file itself

touch $1
truncate -s $3 $1

# set up backstore for target

cd /sys/kernel/config/target/core

# generate next fileio folder

dir_name=fileio_
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
mkdir $2
cd $2

echo "Your backstore path: $temp_name/$2"

# configure device

echo "fd_dev_name=$1,fd_dev_size=$3" > control
echo 1 > enable