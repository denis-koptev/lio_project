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
