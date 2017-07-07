## Starting to work with tcmu

### Set up of tcmu-runner

tcmu-runner is a special "API" for tcmu usage and writing handlers for scsi commands

* First, clone repo from https://github.com/open-iscsi/tcmu-runner
* Install all dependencies (you can use script tcmu_runner_depend.sh)
* To build it from project's folder run `cmake .`
* Then `make`
* Ensure, that target_core_user module is loaded (lsmod)
* If not, load it from /lib/modules/<kernel version>/kernel/drivers/target

*Note: otherwise, tcmu-runner should load it*

* Copy `tcmu-runner.conf` to `/etc/dbus-1/system.d/`. This allows tcmu-runner to be on the system bus, which is privileged.
* If using systemd, copy `org.kernel.TCMUService1.service` to `/usr/share/dbus-1/system-services/` and `tcmu-runner.service` to `/lib/systemd/system`.
* Copy tcmu-runner executable from tcmu-runner folder to /usr/bin/
* Create folder /etc/tcmu/ : `mkdir /etc/tcmu`
* Copy tcmu-runner/tcmu.conf to /etc/tcmu/ : `cp tcmu.conf /etc/tcmu/tcmu.conf`
* tcmu-runner usage: `tcmu-runner -h`

		options:
			-h, --help: print this message and exit
			-V, --version: print version and exit
			-d, --debug: enable debug messages
			--handler-path: set path to search for handler modules
				default is /usr/local/lib/tcmu-runner
			-l, --tcmu-log-dir: tcmu log dir
				default is /var/log/

* By default, handlers for commands are placed in /usr/local/lib/tcmu-runner
* Let's setup tcmu-runner folder as handler folder and run it with debug messages
* `tcmu-runner --handler-path /home/<user>/Desktop/tcmu-runner/ -d`
* Debug prints:

		2017-06-30 12:40:09.014 2815 [DEBUG] main:832 : handler path: /home/denis/Desktop/tcmu-runner/
		2017-06-30 12:40:09.015 2815 [DEBUG] load_our_module:523 : Module 'target_core_user' is already loaded
		2017-06-30 12:40:09.015 2815 [DEBUG] main:845 : 5 runner handlers found
		2017-06-30 12:40:09.017 2815 [DEBUG] dbus_bus_acquired:437 : bus org.kernel.TCMUService1 acquired
		2017-06-30 12:40:09.023 2815 [DEBUG] dbus_name_acquired:453 : name org.kernel.TCMUService1 acquired

* Now targetcli can see all user handlers:

	  o- backstores .......................................................... [...]
	  | o- block .............................................. [Storage Objects: 0]
	  | o- fileio ............................................. [Storage Objects: 0]
	  | o- pscsi .............................................. [Storage Objects: 0]
	  | o- ramdisk ............................................ [Storage Objects: 0]
	  | o- user:fbo ........................................... [Storage Objects: 0]
	  | o- user:file .......................................... [Storage Objects: 0]
	  | o- user:glfs .......................................... [Storage Objects: 0]
	  | o- user:qcow .......................................... [Storage Objects: 0]
	  | o- user:rbd ........................................... [Storage Objects: 0]

### Creating uio

* Ensure tcmu-runner is running (here - with debug prints)
* Run script uio_create.sh as root and specify hba-name, dev-name and size
* Example: `sh uio_create.sh user_1 test 4096`

*Note: hba-name has its own strict structure user_x*

* As a result entries in sysfs will be created (/sys/class/uio, /sys/kernel/config/target/core)
* If everything is ok dev in /dev will be created
* tcmu-runner prints following:

		2017-06-30 12:53:37.379 3091 [DEBUG] dev_added:656 test: Got block_size 512, size in bytes 4096
		2017-06-30 12:53:37.379 3091 [DEBUG] file_open:103 : config file/test
		
* After that, tcmu-runner will detect this and create file (test) in dir where it's running

* In targetcli:

	  | o- user:file .......................................... [Storage Objects: 1]
	  | | o- test ...................................... [test (4.0KiB) deactivated]

*Note: after this step sth goes wrong. After exiting targetcli python prints errors while saving config*

*Idea: maybe sth wrong with configstring file/test in uio_create script*

### Configuring target

* Run script target_setup.sh specifying local backstore-path
* In this case: `sh target_setup.sh user_1/test`
* Now, we have target. In targetcli:

		o- / ..................................................................... [...]
		  o- backstores .......................................................... [...]
		  | o- block .............................................. [Storage Objects: 0]
		  | o- fileio ............................................. [Storage Objects: 0]
		  | o- pscsi .............................................. [Storage Objects: 0]
		  | o- ramdisk ............................................ [Storage Objects: 0]
		  | o- user:fbo ........................................... [Storage Objects: 0]
		  | o- user:file .......................................... [Storage Objects: 1]
		  | | o- test ........................................ [test (4.0KiB) activated]
		  | o- user:glfs .......................................... [Storage Objects: 0]
		  | o- user:qcow .......................................... [Storage Objects: 0]
		  | o- user:rbd ........................................... [Storage Objects: 0]
		  o- iscsi ........................................................ [Targets: 1]
		  | o- iqn.2017-06.com.test:target-30-12-57 .......................... [TPGs: 1]
		  |   o- tpg1 ........................................... [no-gen-acls, no-auth]
		  |     o- acls ...................................................... [ACLs: 1]
		  |     | o- iqn.1993-08.org.debian:01:ef2e26bf3a9e ........... [Mapped LUNs: 1]
		  |     |   o- mapped_lun0 ............................... [lun0 user/test (rw)]
		  |     o- luns ...................................................... [LUNs: 1]
		  |     | o- lun0 .................................................. [user/test]
		  |     o- portals ................................................ [Portals: 1]
		  |       o- 0.0.0.0:3260 ................................................. [OK]
		  o- loopback ..................................................... [Targets: 0]
		  o- vhost ........................................................ [Targets: 0]

*Note: we still have errors on exit*

### Connecting on initiator side

* Discover: `iscsiadm -m discovery -t sendtargets -p 0.0.0.0`
* Result of discovery: `127.0.0.1:3260,1 iqn.2017-06.com.test:target-30-12-57`
* Log in: `iscsiadm -m node -p 127.0.0.1 --login`
* Result: 

		Logging in to [iface: default, target: iqn.2017-06.com.test:target-30-12-57, portal: 127.0.0.1,3260] (multiple)
		Login to [iface: default, target: iqn.2017-06.com.test:target-30-12-57, portal: 127.0.0.1,3260] successful.

* tcmu-runner prints:

		2017-06-30 13:01:01.768 3091 [DEBUG_SCSI_CMD] tcmu_cdb_debug_info:1026 : 12 0 0 0 24 0 
		2017-06-30 13:01:01.768 3091 [DEBUG] handle_inquiry:1815 test: no enabled ports found. Skipping ALUA support
		...
		2017-06-30 13:01:01.776 3091 [DEBUG_SCSI_CMD] tcmu_cdb_debug_info:1026 : a3 c 1 41 0 0 0 0 2 0 0 0 
		2017-06-30 13:01:01.776 3091 [WARN] tcmur_cmdproc_thread:585 : Command 0xa3 not supported
		...

* This means sth is still wrong, but connection was done
* Let's check: `iscsiadm -m session -P 0`
* Result:

		tcp: [1] 127.0.0.1:3260,1 iqn.2017-06.com.test:target-30-12-57 (non-flash)

* `iscsiadm`

		[0:0:0:0]    disk    VMware,  VMware Virtual S 1.0   /dev/sda 
		[2:0:0:0]    cd/dvd  NECVMWar VMware IDE CDR10 1.00  /dev/sr0 
		[3:0:0:0]    disk    LIO-ORG  TCMU device      0002  /dev/sdb 

* Let's dd something: 

		root@debian:/home/denis/Desktop# touch init_file
		root@debian:/home/denis/Desktop# echo Hello World > init_file 
		root@debian:/home/denis/Desktop# dd if=/home/denis/Desktop/init_file of=/dev/sdb
		0+1 records in
		0+1 records out
		12 bytes copied, 0.0105804 s, 1.1 kB/s
		
* To control write operation some debug prints were added to file_example.c (tcmu-runner)

* But tcmu-runner still cannot handle some commands:

		...
		2017-06-30 13:06:33.650 3091 [DEBUG] handle_inquiry:1815 test: no enabled ports found. Skipping ALUA support
		2017-06-30 13:06:33.650 3091 [DEBUG_SCSI_CMD] tcmu_cdb_debug_info:1026 : 12 1 83 0 fe 0 
		2017-06-30 13:06:33.650 3091 [DEBUG] handle_inquiry:1815 test: no enabled ports found. Skipping ALUA support
		2017-06-30 13:06:33.650 3091 [DEBUG_SCSI_CMD] tcmu_cdb_debug_info:1026 : 0 0 0 0 0 0 
		2017-06-30 13:06:33.650 3091 [DEBUG_SCSI_CMD] tcmu_cdb_debug_info:1026 : 28 0 0 0 0 0 0 0 8 0 
		2017-06-30 13:06:33.651 3091 [DEBUG_SCSI_CMD] tcmu_cdb_debug_info:1026 : 0 0 0 0 0 0 	

* On the other hand, debug prints:

		2017-07-03 11:43:21.487 18062 [DEBUG_SCSI_CMD] tcmu_cdb_debug_info:1026 : 28 0 0 0 0 0 0 0 8 0 
		[DEBUG PRINT] WRITE OPERATION
		[CONTENT] Hello World
		
* Content of test file:

		root@denis-linux:~/Desktop/tcmu-runner# cat test
		Hello World

### Finishing

* `iscsiadm -m node -u`
* targetcli: `clearconfig confirm=True`

### Complex configuration

	o- / ..................................................................... [...]
	  o- backstores .......................................................... [...]
	  | o- block .............................................. [Storage Objects: 0]
	  | o- fileio ............................................. [Storage Objects: 0]
	  | o- pscsi .............................................. [Storage Objects: 0]
	  | o- ramdisk ............................................ [Storage Objects: 0]
	  | o- user:fbo ........................................... [Storage Objects: 0]
	  | o- user:file .......................................... [Storage Objects: 3]
	  | | o- test_1 .................................... [test_1 (8.0KiB) activated]
	  | | o- test_2 .................................... [test_2 (4.0KiB) activated]
	  | | o- test_3 .................................... [test_3 (4.0KiB) activated]
	  | o- user:glfs .......................................... [Storage Objects: 0]
	  | o- user:qcow .......................................... [Storage Objects: 0]
	  | o- user:rbd ........................................... [Storage Objects: 0]
	  o- iscsi ........................................................ [Targets: 2]
	  | o- iqn.2017-07.com.test:target-05-15-52 .......................... [TPGs: 1]
	  | | o- tpg1 ........................................... [no-gen-acls, no-auth]
	  | |   o- acls ...................................................... [ACLs: 1]
	  | |   | o- iqn.1993-08.org.debian:01:b78c0c04e80 ............ [Mapped LUNs: 2]
	  | |   |   o- mapped_lun0 ............................. [lun0 user/test_1 (rw)]
	  | |   |   o- mapped_lun1 ............................. [lun1 user/test_3 (rw)]
	  | |   o- luns ...................................................... [LUNs: 2]
	  | |   | o- lun0 ................................................ [user/test_1]
	  | |   | o- lun1 ................................................ [user/test_3]
	  | |   o- portals ................................................ [Portals: 1]
	  | |     o- 0.0.0.0:3260 ................................................. [OK]
	  | o- iqn.2017-07.com.test:target-05-15-53 .......................... [TPGs: 1]
	  |   o- tpg1 ........................................... [no-gen-acls, no-auth]
	  |     o- acls ...................................................... [ACLs: 1]
	  |     | o- iqn.1993-08.org.debian:01:b78c0c04e80 ............ [Mapped LUNs: 1]
	  |     |   o- mapped_lun0 ............................. [lun0 user/test_2 (rw)]
	  |     o- luns ...................................................... [LUNs: 1]
	  |     | o- lun0 ................................................ [user/test_2]
	  |     o- portals ................................................ [Portals: 1]
	  |       o- 0.0.0.0:3260 ................................................. [OK]
	  o- loopback ..................................................... [Targets: 0]
	  o- vhost ........................................................ [Targets: 0]

### Connecting to it

`# iscsiadm -m discovery -t sendtargets -p 127.0.0.1`

	127.0.0.1:3260,1 iqn.2017-07.com.test:target-05-15-52
	127.0.0.1:3260,1 iqn.2017-07.com.test:target-05-15-53
		
`# iscsiadm -m node -T iqn.2017-07.com.test:target-05-15-52 -p 127.0.0.1 --login`

	Logging in to [iface: default, target: iqn.2017-07.com.test:target-05-15-52, portal: 127.0.0.1,3260] (multiple)
	Login to [iface: default, target: iqn.2017-07.com.test:target-05-15-52, portal: 127.0.0.1,3260] successful.
		
`# lsscsi`

	[0:0:0:0]    disk    VMware,  VMware Virtual S 1.0   /dev/sda 
	[2:0:0:0]    cd/dvd  NECVMWar VMware IDE CDR10 1.00  /dev/sr0 
	[3:0:0:0]    disk    LIO-ORG  TCMU device      0002  /dev/sdb 
	[3:0:0:1]    disk    LIO-ORG  TCMU device      0002  /dev/sdc 
	
### While logging in

	|---------------------------------------------|--------------------|
	| CDB                                         | COMMAND TYPE       |
	|---------------------------------------------|--------------------|
	| 12 0 0 0 24 0                               | inquiry            |
	| 12 1 0 0 ff 0                               | inquiry            |
	| 12 1 80 0 ff 0                              | inquiry            |
	| 12 1 83 0 ff 0                              | inquiry            |
	| 0 0 0 0 0 0                                 | test unit ready    |
	| 9e 10 0 0 0 0 0 0 0 0 0 0 0 20 0 0          | service action in  |
	| 12 1 0 0 40 0                               | inquiry            |
	| 12 1 b0 0 40 0                              | inquiry            |
	| 12 1 0 0 40 0                               | inquiry            |
	| 12 1 b1 0 40 0                              | inquiry            |
	| 1a 0 3f 0 4 0                               | mode sense         |
	| 1a 0 8 0 4 0                                | mode sense         |
	| a3 c 1 12 0 0 0 0 2 0 0 0 (not supported)   | maintenance in     |
	| a3 c 1 93 0 0 0 0 2 0 0 0 (not supported)   | maintenance in     |
	| a3 c 1 41 0 0 0 0 2 0 0 0 (not supported)   | maintenance in     |
	| 0 0 0 0 0 0                                 | test unit ready    |
	| 9e 10 0 0 0 0 0 0 0 0 0 0 0 20 0 0          | service action in  |
	| 12 1 0 0 40 0                               | inquiry            |
	| 12 1 b0 0 40 0                              | inquiry            |
	| 12 1 0 0 40 0                               | inquiry            |
	| 12 1 b1 0 40 0                              | inquiry            |
	| 1a 0 3f 0 4 0                               | mode sense         |
	| 1a 0 8 0 4 0                                | mode sense         |
	| a3 c 1 12 0 0 0 0 2 0 0 0 (not supported)   | maintenance in     |
	| a3 c 1 93 0 0 0 0 2 0 0 0 (not supported)   | maintenance in     |
	| a3 c 1 41 0 0 0 0 2 0 0 0 (not supported)   | maintenance in     |
	| 28 0 0 0 0 0 0 0 8 0                        | read               |
	| 0 0 0 0 0 0                                 | test unit ready    |
	| 9e 10 0 0 0 0 0 0 0 0 0 0 0 20 0 0          | service action in  |
	| 12 1 0 0 40 0                               | inquiry            |
	| 12 1 b0 0 40 0                              | inquiry            |
	| 12 1 0 0 40 0                               | inquiry            |
	| 12 1 b1 0 40 0                              | inquiry            |
	| 1a 0 3f 0 4 0                               | mode sense         |
	| 1a 0 8 0 4 0                                | mode sense         |
	| a3 c 1 12 0 0 0 0 2 0 0 0 (not supported)   | maintenance in     |
	| a3 c 1 93 0 0 0 0 2 0 0 0 (not supported)   | maintenance in     |
	| a3 c 1 41 0 0 0 0 2 0 0 0 (not supported)   | maintenance in     |
	| 28 0 0 0 0 0 0 0 8 0                        | read               |
	| 0 0 0 0 0 0                                 | test unit ready    |
	| 0 0 0 0 0 0                                 | test unit ready    |
	| 9e 10 0 0 0 0 0 0 0 0 0 0 0 20 0 0          | service action in  |
	| 12 1 0 0 40 0                               | inquiry            |
	| 12 1 b0 0 40 0                              | inquiry            |
	| 12 1 0 0 40 0                               | inquiry            |
	| 12 1 b1 0 40 0                              | inquiry            |
	| 1a 0 3f 0 4 0                               | mode sense         |
	| 1a 0 8 0 4 0                                | mode sense         |
	| a3 c 1 12 0 0 0 0 2 0 0 0 (not supported)   | maintenance in     |
	| a3 c 1 93 0 0 0 0 2 0 0 0 (not supported)   | maintenance in     |
	| a3 c 1 41 0 0 0 0 2 0 0 0 (not supported)   | maintenance in     |
	| 12 0 0 0 fe 0                               | inquiry            |
	| 0 0 0 0 0 0                                 | test unit ready    |
	| 12 1 0 0 fe 0                               | inquiry            |
	| 12 1 80 0 fe 0                              | inquiry            |
	| 12 1 83 0 fe 0                              | inquiry            |
	| 0 0 0 0 0 0                                 | test unit ready    |
	| 28 0 0 0 0 0 0 0 8 0                        | read               |
	| 0 0 0 0 0 0                                 | test unit ready    |
	| 85 6 20 0 5 0 fe 0 0 0 0 0 0 40 ef 0 (n.s.) | ATA pass-through   |
	| 85 8 e 0 0 0 1 0 0 0 0 0 0 40 ec 0  (n.s.)  | ATA pass-through   |
	| 0 0 0 0 0 0                                 | test unit ready    |
	| 0 0 0 0 0 0                                 | test unit ready    |
	|------------------------------------------------------------------| 
