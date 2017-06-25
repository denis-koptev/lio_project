## iblock device creation and target configuration

* Script block_create.sh creates logical volume and scsi backstore
* Script target_setup.sh creates target, tpg, acl and lun

### Device creation

* Create directory in which we'll store file for log volume

`mkdir /home/denis/iscsi_files`

* Find block_create script

`cd /home/denis/Desktop/lio_project/scripts/block_configuration`

* This script should be run as root `su`

* Running this scrip you need to specify directory and name for file and name for backstore device

* In this example:  `sh block_create.sh /home/iscsi_files/test_file test_block`

* Script will give you some info:

	Physical volume "/dev/loop2" successfully created.
	Volume group "vol_group_1" successfully created
	Logical volume "log_vol" created.
	Your backstore path: iblock_0/test_block

* /dev/loop2 is the first loopback device which is free
* You will use backstore path (here: iblock_0/test_block) later

### Target setup

* Locate target_setup.sh script

* You have to specify backstore path, given to you by block_create script

* Script will automatically generate iqn, you don't need to specify it

* In this example: `sh target_setup.sh iblock_0/test_block`

* Let's check everything is ok
* `targetcli`
* `ls`

	o- / ..................................................................... [...]
	  o- backstores .......................................................... [...]
	  | o- block .............................................. [Storage Objects: 1]
	  | | o- test_block ........................... [ (4.0MiB) write-thru activated]
	  | o- fileio ............................................. [Storage Objects: 0]
	  | o- pscsi .............................................. [Storage Objects: 0]
	  | o- ramdisk ............................................ [Storage Objects: 0]
	  o- iscsi ........................................................ [Targets: 1]
	  | o- iqn.2017-06.com.test:target-25-04-40 .......................... [TPGs: 1]
	  |   o- tpg1 ........................................... [no-gen-acls, no-auth]
	  |     o- acls ...................................................... [ACLs: 1]
	  |     | o- iqn.1993-08.org.debian:01:ef2e26bf3a9e ........... [Mapped LUNs: 1]
	  |     |   o- mapped_lun0 ........................ [lun0 block/test_block (rw)]
	  |     o- luns ...................................................... [LUNs: 1]
	  |     | o- lun0 ........................................... [block/test_block]
	  |     o- portals ................................................ [Portals: 1]
	  |       o- 0.0.0.0:3260 ................................................. [OK]
	  o- loopback ..................................................... [Targets: 0]
	  o- vhost ........................................................ [Targets: 0]

* `exit`


### Let's work on the initiator side

* Discover: `iscsiadm -m discovery -t sendtargets -p 0.0.0.0`

`127.0.0.1:3260,1 iqn.2017-06.com.test:target-25-04-40`

* Connect: `iscsiadm -m node -p 127.0.0.1 --login`

* Check: `iscsiadm -m session -P 0`

* `lsscsi` (Find our new device. In this example - /dev/sdb)

* Create file to dd from it: `touch init_file`
* `echo Hello World > init_file`

* Use dd: `dd if=/home/denis/Desktop/init_file of=/dev/sdb bs=64k iflag=direct`

* Problem: We'll get error, because we're attempting to dd from file to block:
dd: error reading '/home/denis/Desktop/init_file': Invalid argument

* On the other hand, bytes were copied
* Check the result: `cat /home/iscsi_files/test_file`

You'll get a lot of info in this file. But it ends with:

	...
	contents = "Text Format Volume Group"
	version = 1

	description = ""

	creation_host = "debian"	# Linux debian 4.9.0-3-amd64 #1 SMP Debian 4.9.30-2+deb9u1 (2017-06-18) x86_64
	creation_time = 1498354560	# Sun Jun 25 04:36:00 2017

	Hello World

Hello World was written

* Log out of session: `iscsiadm -m node -u`