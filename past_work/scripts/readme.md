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

### Question: what about /sys/devices/tcm_user folder?

### Question 2

* After uio creation we can try to start targetcli and after that exit
* Python script throws an error with some info:

	Traceback (most recent call last):
	  File "/usr/bin/targetcli", line 121, in <module>
	    main()
	  File "/usr/bin/targetcli", line 117, in main
	    root_node.ui_command_saveconfig()
	  File "/usr/lib/python3/dist-packages/targetcli/ui_root.py", line 86, in ui_command_saveconfig
	    self.rtsroot.save_to_file(savefile)
	  File "/usr/lib/python3/dist-packages/rtslib_fb/root.py", line 250, in save_to_file
	    f.write(json.dumps(self.dump(), sort_keys=True, indent=2))
	  File "/usr/lib/python3/dist-packages/rtslib_fb/root.py", line 146, in dump
	    d['storage_objects'] = [so.dump() for so in self.storage_objects]
	  File "/usr/lib/python3/dist-packages/rtslib_fb/root.py", line 146, in <listcomp>
	    d['storage_objects'] = [so.dump() for so in self.storage_objects]
	  File "/usr/lib/python3/dist-packages/rtslib_fb/tcm.py", line 820, in dump
	    d['level'] = self.level
	  File "/usr/lib/python3/dist-packages/rtslib_fb/tcm.py", line 800, in _get_level
	    return int(self._parse_info('PassLevel'))
	  File "/usr/lib/python3/dist-packages/rtslib_fb/tcm.py", line 173, in _parse_info
	    % key, ' '.join(info.split())).group(1)
	AttributeError: 'NoneType' object has no attribute 'group'


