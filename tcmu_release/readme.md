## TCMU USERSPACE PASSTHROUGH TUTORIAL

This tutorial describes how to connect TCM LIO driver to userspace using tcmu-runner and scripts to configure target and process SCSI comands.

Original tcmu-runner can be found here:
https://github.com/open-iscsi/tcmu-runner

### Starting

All tests below are made on Debian 9

1. You need some packages to be installed

* targetcli
* open-iscsi
* lsscsi

### Building and running tcmu-runner

tcmu-runner in our repo is different from original.
We removed unnecessary standard handlers (glfs, rbd, qcow)
On the other hand, this tcmu-runner has new handler 'alloc'
This handler works only with it's memory. Memory plays a device role in this case

* Install all dependencies (you can use dependency.sh script)
* To build it from project's folder run `cmake .`
* Then `make`
* Ensure, that target_core_user module is loaded (lsmod)
* If not, load it from /lib/modules/<kernel version>/kernel/drivers/target

*Note: otherwise, tcmu-runner should load it*

* Copy `tcmu-runner.conf` to `/etc/dbus-1/system.d/`. This allows tcmu-runner to be on the system bus, which is privileged.
* Copy tcmu-runner executable from tcmu-runner folder to /usr/bin/
* Create folder /etc/tcmu/ : `mkdir /etc/tcmu`
* Copy tcmu-runner/tcmu.conf to /etc/tcmu/ : `cp tcmu.conf /etc/tcmu/tcmu.conf`
* Run tcmu-runner using run.sh script from tcmu-runner directory (as root)

As a result of this actions tcmu-runner runs in loop.
Our alloc handler gives you some info from tcmu-runner console:

`>>> [ALLOC] handler_init`

### Creating backstore user device

Process your actions from different console as root

* Let's create device with type alloc (working with memory)

`./user_create alloc test_0 1048576`

After that script will give you backstore path (it'll be used later).
In this example: `[INFO] Your backstore directory: user_0/test_0`

tcmu-runner in other terminal prints some more messages:

		>>> [ALLOC] alloc_open
		>>> [ALLOC] dev size: 1048576

* Let's create a file device, too

`./user_create.sh file test_1 4096`

Result: `[INFO] Your backstore directory: user_1/test_1`

All created config can be seen using targetcli: `targetcli`

`/> ls`

		o- / ........................................................................................... [...]
		  o- backstores ................................................................................ [...]
		  | o- block .................................................................... [Storage Objects: 0]
		  | o- fileio ................................................................... [Storage Objects: 0]
		  | o- pscsi .................................................................... [Storage Objects: 0]
		  | o- ramdisk .................................................................. [Storage Objects: 0]
		  | o- user:alloc ............................................................... [Storage Objects: 1]
		  | | o- test_0 ........................................................ [test_0 (1.0MiB) deactivated]
		  | o- user:file ................................................................ [Storage Objects: 1]
		  |   o- test_1 ........................................................ [test_1 (4.0KiB) deactivated]
		  o- iscsi .............................................................................. [Targets: 0]
		  o- loopback ........................................................................... [Targets: 0]
		  o- vhost .............................................................................. [Targets: 0]

### Creating target

* It is simple: ./target_create.sh

		[INFO] Target iqn.2017-07.com.test:target-14-17-18 created
		[INFO] Portal: 127.0.0.1:3260

### Connecting target to backstores

* Use script target_setup.sh for every backstore device
* Specify target iqn and backstore path you got earlier

		./target_setup.sh iqn.2017-07.com.test:target-14-17-18 user_0/test_0
		./target_setup.sh iqn.2017-07.com.test:target-14-17-18 user_1/test_1

Result can be seen via targetcli

		  o- backstores ................................................................................ [...]
		  | o- block .................................................................... [Storage Objects: 0]
		  | o- fileio ................................................................... [Storage Objects: 0]
		  | o- pscsi .................................................................... [Storage Objects: 0]
		  | o- ramdisk .................................................................. [Storage Objects: 0]
		  | o- user:alloc ............................................................... [Storage Objects: 1]
		  | | o- test_0 .......................................................... [test_0 (1.0MiB) activated]
		  | o- user:file ................................................................ [Storage Objects: 1]
		  |   o- test_1 .......................................................... [test_1 (4.0KiB) activated]
		  o- iscsi .............................................................................. [Targets: 1]
		  | o- iqn.2017-07.com.test:target-14-17-18 ................................................ [TPGs: 1]
		  |   o- tpg1 ................................................................. [no-gen-acls, no-auth]
		  |     o- acls ............................................................................ [ACLs: 1]
		  |     | o- iqn.1993-08.org.debian:01:ef2e26bf3a9e ................................. [Mapped LUNs: 2]
		  |     |   o- mapped_lun0 ................................................... [lun0 user/test_0 (rw)]
		  |     |   o- mapped_lun1 ................................................... [lun1 user/test_1 (rw)]
		  |     o- luns ............................................................................ [LUNs: 2]
		  |     | o- lun0 ...................................................................... [user/test_0]
		  |     | o- lun1 ...................................................................... [user/test_1]
		  |     o- portals ...................................................................... [Portals: 1]
		  |       o- 0.0.0.0:3260 ....................................................................... [OK]
		  o- loopback ........................................................................... [Targets: 0]
		  o- vhost .............................................................................. [Targets: 0]


### Initiator side

* Connect to target

`iscsiadm -m discovery -t sendtargets -p 127.0.0.1 --login`

* Now we can see devices: `lsscsi`

		[0:0:0:0]    disk    VMware,  VMware Virtual S 1.0   /dev/sda 
		[2:0:0:0]    cd/dvd  NECVMWar VMware IDE CDR10 1.00  /dev/sr0 
		[3:0:0:0]    disk    LIO-ORG  TCMU device      0002  /dev/sdb 
		[3:0:0:1]    disk    LIO-ORG  TCMU device      0002  /dev/sdc

Now we can dd to and from this devices. In case of sdb all data will be stored in handler's memory. In case of sdc - in special file created by handler in tcmu-runner folder.

* Logout: `iscsiadm -m session -u`