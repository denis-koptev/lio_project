## Creating uio to make lio work with userspace

* Sequence of actions in ubuntu 16.04 terminal

`denis@ubuntu:/sys/kernel/config/target/core$ sudo mkdir user_1`

`denis@ubuntu:/sys/kernel/config/target/core/user_1$ sudo mkdir test`

`denis@ubuntu:/sys/kernel/config/target/core/user_1/test$ sudo su`

`root@ubuntu:/sys/kernel/config/target/core/user_1/test# echo -n dev_size=16777216 > control`

`root@ubuntu:/sys/kernel/config/target/core/user_1/test# echo -n dev_config=baz`

`addl_info_for_baz_handler > control`

`root@ubuntu:/sys/kernel/config/target/core/user_1/test# echo -n 1 > enable`

`root@ubuntu:/sys/kernel/config/target/core/user_1/test# cd /sys/class/uio/`

`root@ubuntu:/sys/class/uio# ls`

`uio0`

`root@ubuntu:/sys/class/uio# cd uio0`

`root@ubuntu:/sys/class/uio/uio0# ls`

`dev  device  event  maps  name  power  subsystem  uevent  version`

`root@ubuntu:/sys/class/uio/uio0# cat name `

`tcm-user/1/test/baz/addl_info_for_baz_handler`

`root@ubuntu:/sys/class/uio/uio0# cat maps/map0/size `

`0x0000000000110000`

## Working with scripts

### To create and delete uio

`sudo sh uio_create.sh user_1 test 4096`

`sudo sh uio_delete.sh user_1 test`

### To create target

`sudo sh target_create.sh iqn.2015-05.com.example:target`

### To create lun for uio

`sudo sh lun_create.sh iqn.2015-05.com.example:target user_1 test`

## After uio_create

### Directory /sys/devices/tcm_user/uio/uio0 appears

In this dir:

device -> ../../../tcm_user

subsystem -> ../../../../class/uio

name: tcm-user/1/test/baz/addl_info_for_baz_handler

### The same directory (uio0) appears (like a link?) in /sys/devices/tcm_user/uio/

Link to this (tcm_user/uio/uio0) folder appears in: /sys/class/uio

### user_1 folder appears in /sys/kernel/config/target/core

In this folder we have hba_info and hba_mode files and test folder

### Device uio0 appears in /dev

### Problem

Name of the device and info in config contains `baz/addl_info_for_baz_handler` path. It's strange, because we don't have it anywhere


