#!/bin/sh

# run as su

if [ $(id -u) -ne 0 ]
	then echo "Please run as root" 
	exit
fi

# check args

if [ $# -ne 3 ]
	then echo "Wrong number of arguments. Must be 3: dir/block_file, vg size, lv size"
	exit
fi

# create lvm (lwm2 should be installed)

truncate --size $2 $1
dev_path=`losetup --find --show $1`

cd /dev

vg_name=vol_group_
idx=0

# If file already exists, find next dir_name that is not yet taken
while true; do
    temp_name=$vg_name$idx
    if [ ! -d $temp_name ]; then
        break
    fi
    idx=$(($idx + 1))
done
vg_name=$temp_name

vgcreate $vg_name $dev_path

lvcreate --size $3 --name log_vol $vg_name

echo "Path to logical volume: /dev/$vg_name/log_vol"

