#!/bin/sh

if [ $# -ne 3 ]
then echo "Wrong number of arguments. Must be 3: HBA name, storage object name, size"
     exit
fi

# maybe insert deletion of old versions?

mkdir -p "/sys/kernel/config/target/core/$1/$2"

cd /sys/kernel/config/target/core/$1/$2
echo -n dev_size=$3 > control
# echo -n dev_config=baz/addl_info_for_baz_handler > control # path to some handler?
echo -n 1 > enable
