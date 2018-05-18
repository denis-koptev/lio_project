# LIO Project

## Introduction

Linux-IO (LIO, TCM) - has been the Linux SCSI target since kernel version 2.6.38.
It supports a rapidly growing number of fabric modules, and all existing Linux block devices as backstores.

These repository provides system for userspace passthrought testing using various types of devices:
- block
- fileio
- user:file
- user:alloc

### Userspace passthrough

For many types of devices, creating a Linux kernel driver is overkill. 
All that is really needed is some way to handle an interrupt and provide access to the memory space of the device. 
The logic of controlling the device does not necessarily have to be within the kernel, 
as the device does not need to take advantage of any of other resources that the kernel provides.

For Linux-IO we have special module - TCMU (TCM in Userspace). 
It provides us with an opportunity to handle SCSI commands in userspace having userspace backstores.
Module name: `target_core_user`.

In this project we have support 2 userspace device types: file and alloc.

File allows to represent device as a simple file somewhere in your filesystem.

Alloc - is our hand-written device handler. It doesn't need any file or other device.
Alloc stores all data in the program memory and uses simple and fast C operations to copy bytes.

## Running simple LIO Session

### Cloning and installing dependencies

Further instructions are definitely correct for Ubuntu 16.04, 17.10 and 18.04.

* Clone this repo: `git clone https://github.com/denis-koptev/lio_project`
* `cd lio_project`
* Run `instal_deps` script: `sudo ./install_deps.sh`
This script will install all needed dependencies for LIO Project testing system and for tcmu-runner daemon (see below).

### JSON configuration

For your comfort all system can be entirely configured with the help of the config file in JSON format.
Example is provided in `lio_json_initial.json`

`parse_json.py` script validates initial JSON configuration and adds some additional 'low-level' parameters.

Limitations for JSON:

Target
* `target` object must be presented. It contains only `name` parameter

Devices
* `devices` JSON-array must be presented
* Each device contains 3 string parameters: `name`, `type` and `size`
* `type`: `block`, `fileio`, `file` or `alloc`
* `size` - in bytes (as string)
* `path` string to a logical volume for block device

Initiators
* `initiators` JSON-array must be presented
* Each `initiator` object contains only name
* `io` JSON-array must be presented
* `io` element plays role of one IO operation to one device for one initiator
* `io` contains 3 string parameters: `initiator` - initiator's name, `device` - device name, `size` - in bytes 

### Starting session

* It's simple: `sudo ./lio_start_session.sh lio_json_initial.json`

LIO Session consists of:

* Creation of devices
* Creation of target (IQN, LUNs, ACL, LunMappings, Portal will be created)
* Creation of one (at this time) initiator
* Login and IO operations for one (at this time) initiator

All results are collected in log-files. They can be found in `session` folder.
Main results are displayed in console.

_Note: if you want to configure and use block devices, you need to create logical volumes for them and specify correct paths in config.
Otherwise, you will get warnings, that devices couldn't be found. IO operations for non-existent devices will be skipped._
_For these aims `create_block.sh` is present._
_Use it in the following way: `sudo ./create_block.sh <backing file name> <vol_group size> <vol size>`_

### Typical displayed results:

```
denis@ubuntu:~/lio_project$ sudo ./lio_start_session.sh lio_json_initial.json 
=================================================
====== WELCOME TO LIO-SESSION START SCRIPT ======
=================================================
[INFO] Previous session directory exists. It will be recreated.
[INFO] Creating internal configs for target and initiators in ./session
----- ENTERING START_TARGET SCRIPT -----
[INFO] Building and starting tcmu-runner daemon
Warning: The unit file, source configuration file or drop-ins of tcmu-runner.service changed on disk. Run 'systemctl daemon-reload' to reload units.
[INFO] Verifying that propper modules are loaded
[INFO] Creating devices.
[INFO] Devices created successfully.
[INFO] Creating target.
[INFO] Target created successfully.
[INFO] Target IP address: 127.0.1.1
[INFO] Launching host-initiator
----- ENTERING START_INITIATOR SCRIPT -----
[INFO] Attempting to discover targets and log in
127.0.1.1:3260,1 iqn.2018-05.com.lio-project:tgt-tgt1
Logging in to [iface: default, target: iqn.2018-05.com.lio-project:tgt-tgt1, portal: 127.0.1.1,3260] (multiple)
Login to [iface: default, target: iqn.2018-05.com.lio-project:tgt-tgt1, portal: 127.0.1.1,3260] successful.
[INFO] Creating a file with the list of iSCSI devices: session/initconf_init1_dev
[INFO] Starting IO operations to devices
[INFO] Found following devices: [
{'lun': 'lun_0', 'dev': 'sdb'}, 
{'lun': 'lun_1', 'dev': 'sdv'}, 
...
{'lun': 'lun_19', 'dev': 'sdd'}, 
{'lun': 'lun_20', 'dev': 'sdc'}]
[INFO] Starting random IO to fileio1 with fileio type and lun=lun_0
[INFO] Time: 6.41 s; Speed: 79.85 MB/s
[INFO] Result: {'success': 1, 'message': 'OK', 'dev_path': '/dev/sdb', 'dev_size': 536870912, 'bs': 4096, 'total_time': '6.41', 'speed': '79.85', 'dev_name': 'fileio1', 'dev_type': 'fileio', 'dev_lun': 'lun_0'}
[INFO] Starting random IO to fileio2 with fileio type and lun=lun_1
[INFO] Time: 6.54 s; Speed: 78.28 MB/s
[INFO] Result: {'success': 1, 'message': 'OK', 'dev_path': '/dev/sdv', 'dev_size': 536870912, 'bs': 4096, 'total_time': '6.54', 'speed': '78.28', 'dev_name': 'fileio2', 'dev_type': 'fileio', 'dev_lun': 'lun_1'}
...
[INFO] Starting random IO to file1 with file type and lun=lun_7
[INFO] Time: 5.31 s; Speed: 96.45 MB/s
[INFO] Result: {'success': 1, 'message': 'OK', 'dev_path': '/dev/sdp', 'dev_size': 536870912, 'bs': 4096, 'total_time': '5.31', 'speed': '96.45', 'dev_name': 'file1', 'dev_type': 'file', 'dev_lun': 'lun_7'}
...
[INFO] Starting random IO to alloc1 with alloc type and lun=lun_15
[INFO] Time: 4.86 s; Speed: 105.36 MB/s
[INFO] Result: {'success': 1, 'message': 'OK', 'dev_path': '/dev/sdh', 'dev_size': 536870912, 'bs': 4096, 'total_time': '4.86', 'speed': '105.36', 'dev_name': 'alloc1', 'dev_type': 'alloc', 'dev_lun': 'lun_15'}
...
[INFO] Starting random IO to alloc7 with alloc type and lun=lun_20
[INFO] Time: 4.71 s; Speed: 108.71 MB/s
[INFO] Result: {'success': 1, 'message': 'OK', 'dev_path': '/dev/sdc', 'dev_size': 536870912, 'bs': 4096, 'total_time': '4.71', 'speed': '108.71', 'dev_name': 'alloc7', 'dev_type': 'alloc', 'dev_lun': 'lun_20'}
[INFO] IO operations finished normally
[INFO] Logging out of session
Logging out of session [sid: 2, target: iqn.2018-05.com.lio-project:tgt-tgt1, portal: 127.0.1.1,3260]
Logout of [sid: 2, target: iqn.2018-05.com.lio-project:tgt-tgt1, portal: 127.0.1.1,3260] successful.
[INFO] LIO SESSION ENDED NORMALLY
```

`start_target` scripts include tcmu-runner build stage.
You can have errors with `iovec` structure during compilation.
The best way for now - is to replace `#include <linux/uio.h>` with `#include <sys/uio.h>` in target_core_user_local.h

```
In file included from /home/denis/lio_project/tcmu-runner/target_core_user_local.h:7:0,
                 from /home/denis/lio_project/tcmu-runner/libtcmu.c:36:
/usr/include/linux/uio.h:17:8: error: redefinition of ‘struct iovec’
```

### Wiping system

Creating new session (with new config) while old configuration is presented - is not a problem.
All scripts are able to work with existing configuration entries and update them.
However, you can have some problems trying to change size or some other specific parameters (for example, for device)

So, if you have this problem or system crashed without any obvious reason you are able to wipe it.

`sudo ./wipe_system.sh`

After that you can create session again.
If problem remains, reboot your system.

## Internal architecture

Simplified architecture scheme

![LIO Project Architecture](https://pp.userapi.com/c846019/v846019297/4944c/N1d9Jc8eBrE.jpg?raw=true "LIO Project Architecture")

### tcmu-runner

tcmu-runner is a daemon, that provides API for interraction with TCMU. 
Each tcmu-runner handler contains C struct with handler functions for different operations (read, write, login, etc).
Daemon contains some default example handlers (file). Alloc - is a custom handler.

Original tcmu-runner repo: https://github.com/open-iscsi/tcmu-runner

Our tcmu-runner is a little bit different. It contains only file handler
(original daemon has glfs, QEMU Copy On Write and other handlers). Alloc - is our custom handler.

### System limitations and problems

* You can't set useful size for IO operation, but this parameter must be presented in JSON.
For now, entire device size will be used for IO operation.
* You can't choose block size for IO operations at this moment
* You can have compilation errors for tcmu-runner (see previous notes)
* You can have strange problems with device discovery while sripts are creating initiator (reboot OS)
* You can have problems if you are creating new configuration while previous one exists (wipe_system)

If you've noticed any other problems, please, let me know: koptevda@ya.ru

### Creation scripts

To create LIO Session `lio_start_session.sh` script uses some other modules (python, bash).

* `parse_json.py`
* `start_target.sh`
* `start_target.py`
* `start_initiator.sh`
* `start_initiator.py`
* `run_io.py`

### Verification and testing

To verify that IO ended correctly: `sudo python3 verify_io.py <path_to_json_io_results>`

Example: `sudo python3 verify_io.py session/initconf_init1_io_result `

To get average speed for each device type run `get_type_average.py` script

Example: `sudo python3 get_type_average.py session/initconf_init1_io_result`

#### Jenkins

Jenkins is used to run some tests. Description can be found in [jenkins](https://github.com/denis-koptev/lio_project/tree/master/jenkins) folder.
