## EMC LIO PROJECT

## targetcli configuration

### Install libs

Install targetcli 
`sudo apt-get install targetcli`

Install open-iscsi 
`sudo apt-get install open-iscsi`

If you're creating loop device install 
`sudo apt-get install lvm2`

### Creating device

How to create device: 

* `sudo truncate --size 100M dev_file`
* `sudo losetup --find --show dev_file`
* You can see something like this: */dev/loop0*
* `sudo vgcreate vol_group /dev/loop0`
* `sudo lvcreate --size 50M --name log_vol vol_group`
* `sudo lvs` - to show created volume

### Creating target

First, let target load on every system boot 

* `sudo systemctl start target`
* `sudo systemctl enable target`

Launch targetcli: `sudo targetcli`

Create device as iblock: `backstores/iblock create name=storage1 dev=/dev/vol_group/log_vol`

Create iqn for target: `/iscsi create iqn.2017-03.com.example:target`

*Note: we can use create without name argument. After that iqn-name will be*
*set up by default. But it's better to set your own unique name*

Set-up authentication

* `cd cd /iscsi/iqn…/tpg1/`
* `set parameter AuthMethod=None`
* `set attribute authentication=0`

*Note: in this example authentication is turned off for simplicity*

Now we must get iqn-name of initiator
If can be found here: `sudo cat /etc/iscsi/initiatorname.iscsi`
*Note: outside of targetcli interface*

Return back to targetcli terminal
Add initiator iqn: `acls/ create iqn.1993-08…`

*Note: iqn.1993-08... - is example. Your real iqn can be found in initiatorname.iscsi*

Create LUN and portal for this configuration:

* `luns/ create /backstores/iblock/storage1`
* `portals/ create`

*Note: you can specify ip-address after create*
*By default it was set up as your host ip in the local network*

Save your configuration: `saveconfig`

Exit: `exit`

## Set up initiator

Turn-off firewall:

* `sudo firewall-cmd --permanent --add-port=3260/tcp`
* `sudo firewall-cmd --reload`

*Note: specify here the port you set up in portal creation*

How can we see our target?
Answer: `sudo iscsiadm --mode discovery --type sendtargets --portal XXX.XXX.XXX.XXX`

*Note: specify here the ip-address fromn portal creation*

Log in: 
`sudo iscsiadm --mode node --targetname iqn.2017-03.com.example:target --portal XXX.XXX.XXX.XXX:3260 --login`

Now we can see our session: `sudo iscsiadm -m session -P 0`

iscsi device was created. How to see it?
Answer: `sudo lsblk --scsi` 
or 
`sudo lsscsi`

## Writing to device

`sudo dd if=/dev/sdb of=/dev/null bs=64k iflag=direct`

*Note: in 'if' parameter specify device, created by lio*

## Finishing

Log out: 
`sudo iscsiadm -m node -u`

Now there are no sessions: 
`sudo iscsiadm -m session -P 0`



