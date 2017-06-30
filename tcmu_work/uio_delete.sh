#!/bin/sh

if [ $# -ne 2 ]
then echo "Wrong number of arguments. Must be 2: HBA name, storage object name"
     exit
fi

rmdir "/sys/kernel/config/target/core/$1/$2"
rmdir "/sys/kernel/config/target/core/$1"