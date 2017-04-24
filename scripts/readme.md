## Creating uio to make lio work with userspace

* Sequence of actions in ubuntu 16.04 terminal

`denis@ubuntu:/sys/kernel/config/target/core$ sudo mkdir user_1
`denis@ubuntu:/sys/kernel/config/target/core/user_1$ sudo mkdir test

`denis@ubuntu:/sys/kernel/config/target/core/user_1/test$ sudo su

`root@ubuntu:/sys/kernel/config/target/core/user_1/test# echo -n dev_size=16777216 > control
`root@ubuntu:/sys/kernel/config/target/core/user_1/test# echo -n dev_config=baz/`addl_info_for_baz_handler > control
`root@ubuntu:/sys/kernel/config/target/core/user_1/test# echo -n 1 > enable

`root@ubuntu:/sys/kernel/config/target/core/user_1/test# cd /sys/class/uio/
`root@ubuntu:/sys/class/uio# ls
`uio0

`root@ubuntu:/sys/class/uio# cd uio0
`root@ubuntu:/sys/class/uio/uio0# ls
`dev  device  event  maps  name  power  subsystem  uevent  version

`root@ubuntu:/sys/class/uio/uio0# cat name 
`tcm-user/1/test/baz/addl_info_for_baz_handler

`root@ubuntu:/sys/class/uio/uio0# cat maps/map0/size 
`0x0000000000110000
