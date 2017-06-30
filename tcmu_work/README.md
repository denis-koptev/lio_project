## Starting to work with tcmu

### Set up of tcmu-runner

tcmu-runner is a special "API" for tcmu usage and writing handlers for scsi commands

* First, clone repo from https://github.com/open-iscsi/tcmu-runner
* Install all dependencies (you can use script tcmu_runner_depend.sh)
* To build it from project's folder run `cmake .`
* Then `make`
* Ensure, that target_core_user module is loaded (lsmod)
* If not, load it from /lib/modules/<kernel version>/kernel/drivers/target
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

* Run script uio_create.sh as root and specify hba-name, dev-name and size
* Example: `sh uio_create.sh user_1 test 4096`

*Note: hba-name has its own strict structure user_x*

* As a result entries in sysfs will be created (/sys/class/uio, /sys/kernel/config/target/core)
* If everything is ok dev in /dev will be created
