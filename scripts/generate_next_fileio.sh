#!/bin/sh

dir_name=fileio_
idx=0

# If file already exists, find next dir_name that is not yet taken
while true; do
    temp_name=$dir_name$idx
    if [ ! -d $temp_name ]; then
        mkdir $temp_name
        echo "Created \"$temp_name\""
        exit 0
    fi
    idx=$(($idx + 1))
done