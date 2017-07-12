#!/bin/sh

if [ $# -ne 3 ]
then echo "Wrong number of arguments. Must be 3: HBA name, storage object name, size"
     exit
fi

mkdir -p "/sys/kernel/config/target/core/$1/$2"

cd /sys/kernel/config/target/core/$1/$2
echo -n dev_size=$3 > control
echo -n dev_config=alloc > control
echo -n 1 > enable

echo "Your backstore directory: $1/$2"
