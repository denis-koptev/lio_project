## Configuring target to work with fileio devices

There are script for file and device creation and for target creation and configuring

### Create file and fileio device

* Run as root: `su`
* `cd lio_project/scripts/fileio_configuration`
* Using fileio_create script you must specify path and name for file, device name and size: 
`sh fileio_create.sh /home/denis/Desktop/target_file file_dev 1024`
* File on desktop appears, device folders in sysfs appears (/sys/kernel/config/target/core/fileio_#/file_dev)
* Script will print your path to backstore (will be used later)

### Let's create file on initiator side

For example, we'll be able to dd from this file to scsi dev

`cd /home/denis/Desktop`

`touch init_file`

`echo Hello World > init_file`

### Configuring target

Use target_setup script from lio_project/scripts/fileio_configuration

* You don't need to specify iqn for target (it will be formed using date and time)
* You need to specify path to backstore (in this example: fileio_3/file_dev)
* Usage: `sh target_setup.sh fileio_3/file_dev`
* Entries in sysfs appears (/sys/kernel/config/target/iscsi/iqn.../tpgt_1/...)

### Let's connect target with open-iscsi initiator

* Discover

`root@debian:/# iscsiadm -m discovery -t sendtargets -p 0.0.0.0`

`127.0.0.1:3260,1 iqn.2017-06.com.example:target-23-06-00`

* Connect

`root@debian:/# iscsiadm -m node -p 127.0.0.1 --login`

`Logging in to [iface: default, target: iqn.2017-06.com.example:target-23-06-00, portal: 127.0.0.1,3260] (multiple)`

`Login to [iface: default, target: iqn.2017-06.com.example:target-23-06-00, portal: 127.0.0.1,3260] successful.`

* Check

`root@debian:/# lsscsi | grep FILEIO`

`[3:0:0:0]    disk    LIO-ORG  FILEIO           4.0   /dev/sdb `

* dd

`root@debian:/# dd if=/home/denis/Desktop/init_file of=/dev/sdb`

`0+1 records in
0+1 records out
12 bytes copied, 0.508858 s, 0.0 kB/s`

`root@debian:/# cat /home/denis/Desktop/target_file `

`Hello World`

* Quit session

`iscsiadm -m node -u`

## Configuration prints

    o- / .............................................................. [...]
      o- backstores ................................................... [...]
      | o- block ....................................... [Storage Objects: 0]
      | o- fileio ...................................... [Storage Objects: 1]
      | | o- file_dev  [/home/denis/Desktop/tgt_file (1.0KiB)]
      | o- pscsi ....................................... [Storage Objects: 0]
      | o- ramdisk ..................................... [Storage Objects: 0]
      o- iscsi ................................................. [Targets: 0]
      o- loopback .............................................. [Targets: 0]
      o- vhost ................................................. [Targets: 0]
      
        o- / .............................................................. [...]
          o- backstores ................................................... [...]
          | o- block ....................................... [Storage Objects: 0]
          | o- fileio ...................................... [Storage Objects: 1]
          | | o- file_dev  [/home/denis/Desktop/tgt_file (1.0KiB) write-thru act]
          | o- pscsi ....................................... [Storage Objects: 0]
          | o- ramdisk ..................................... [Storage Objects: 0]
          o- iscsi ................................................. [Targets: 1]
          | o- iqn.2017-07.com.test:target-10-15-33 ................... [TPGs: 1]
          |   o- tpg1 .................................... [no-gen-acls, no-auth]
          |     o- acls ............................................... [ACLs: 1]
          |     | o- iqn.1993-08.org.debian:01:ef2e26bf3a9e .... [Mapped LUNs: 1]
          |     |   o- mapped_lun0 .................. [lun0 fileio/file_dev (rw)]
          |     o- luns ............................................... [LUNs: 1]
          |     | o- lun0 ...... [fileio/file_dev (/home/denis/Desktop/tgt_file)]
          |     o- portals ......................................... [Portals: 1]
          |       o- 0.0.0.0:3260 .......................................... [OK]
          o- loopback .............................................. [Targets: 0]
          o- vhost ................................................. [Targets: 0]
