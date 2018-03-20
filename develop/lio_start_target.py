import os
import sys
import socket
import json
import glob

# We can confirm that target started only if all configuration will be successfully created

# Create log file in shared session folder
log = open('/lio_project/session/target_log', 'w')

if len(sys.argv) < 2:
    log.write('[ERROR] Config file with JSON was not specified\n')
    sys.exit(1)

log.write('[INFO] Reading JSON config\n')

config_file = open(sys.argv[1], 'r')
config = json.load(config_file)
config_file.close()

log.write('[INFO] JSON config was successfully read\n')
log.write('[INFO] Creating target with following parameters:\n')
log.write(json.dumps(config, indent=4) + '\n')

# Create target itself via sysfs

iscsi_dir = '/sys/kernel/config/target/iscsi/'
tgt_dir = iscsi_dir + config['iqn'] + '/'

log.write('[INFO] Creating Target: ' + config['iqn'] + '\n')

if not os.path.isdir(iscsi_dir):
    log.write('[ERROR] Directory for target configuration does not exist\n')
    sys.exit(1)

if os.path.isdir(tgt_dir):
    log.write('[WARNING] Target with such iqn exists: ' + config['iqn'] + '\n')
else:
    log.write('[INFO] Creating entry in sysfs: ' + tgt_dir + '\n')
    os.makedirs(tgt_dir)

# Create target portal group

log.write('[INFO] Creating Target Portal Group: tpgt_1\n')

tpg_dir = tgt_dir + 'tpgt_1/'
if os.path.isdir(tpg_dir):
    log.write('[WARNING] Target Portal Group already exists\n')
else:
    os.makedirs(tpg_dir)
    log.write('[INFO] Creating entry in sysfs: ' + tpg_dir + '\n')

# Enable target

log.write('[INFO] Enabling target\n')
open(tpg_dir + 'enable', 'w').write('1')

# Set no auth

log.write('[INFO] Switching auth off\n')

attrib_dir = tpg_dir + 'attrib/'
param_dir = tpg_dir + 'param/'
if not os.path.isdir(attrib_dir) or not os.path.isdir(param_dir):
    log.write('[ERROR] No sysfs entries for AUTH configuration\n')
    sys.exit(1)
else:
    open(attrib_dir + 'authentication', 'w').write('0')
    open(param_dir + 'AuthMethod', 'w').write('None')

# Fill ACL

log.write('[INFO] Creating ACL\n')

acl_dir = tpg_dir + 'acls/'
if not os.path.isdir(acl_dir):
    log.write('[ERROR] No sysfs entry for ACLs created\n')
    sys.exit(1)

for iqn in config['acl']:
    if os.path.isdir(acl_dir + iqn):
        log.write('[WARNING] IQN ' + iqn + ' already presented in ACL\n')
    else:
        log.write('[INFO] Creating entry in sysfs: ' + acl_dir + iqn + '\n')
        os.makedirs(acl_dir + iqn)

# Create portal

ipaddr = socket.gethostbyname(socket.gethostname())
log.write('[INFO] Creating portal using IP: ' + ipaddr + '\n')

portal_dir = tpg_dir + 'np/'
ip_dir = portal_dir + ipaddr + ':3260/'
if not os.path.isdir(portal_dir):
    log.write('[ERROR] No sysfs entry for portal created\n')
    sys.exit(1)
else:
    if os.path.isdir(ip_dir):
        log.write('[WARNING] Portal ' + ipaddr + ':3260 already presented\n')
    else:
        log.write('[INFO] Creating entry in sysfs: ' + ip_dir + '\n')
        os.makedirs(ip_dir)

# Add luns for devices if exist

log.write('[INFO] Binding backstores with target\n')

lun_dir = tpg_dir + 'lun/'
if not os.path.isdir(lun_dir):
    log.write('[ERROR] No sysfs entry for luns created\n')
    sys.exit(1)

core_path = '/sys/kernel/config/target/core/'
if not os.path.isdir(core_path):
    log.write('[ERROR] sysfs entry for devices is not presented\n')
    sys.exit(1)

for dev in config['devices']:
    if dev['type'] == 'file':
        type_path = core_path + 'fileio_*/';
        dev_paths = [ dev for dev in glob.glob(type_path + dev['name']) ]
        if len(dev_paths) == 0:
            log.write('[ERROR] Device ' + dev['name'] + ' not found\n')
            sys.exit(1)
        if len(dev_paths) > 1:
            log.write('[ERROR] More than 1 ' + dev['type'] + ' devices with name ' + dev['name'] + ' exist\n')
            log.write('[ERROR] '.join(dev_paths) + '\n')
            sys.exit(1)
        dev_lun_dir = lun_dir + dev['lun'] + '/'
        if os.path.isdir(dev_lun_dir):
            log.write('[WARNING] sysfs entry already exists: ' + dev_lun_dir + '\n')
        else:
            log.write('[INFO] Creating sysfs entry: ' + dev_lun_dir + '\n')
            os.makedirs(dev_lun_dir)
            log.write('[INFO] Creating symlink to ' + dev_paths[0] + '\n]')
            os.symlink(dev_paths[0], dev_lun_dir + dev['name'])
        # Make lun mapping
        # TODO: Make checks for existing directories
        for init in config['acl']:
            # acl_dir + init
            log.write('[INFO] Creating lun mapping: ' + init + ' -> ' + dev['name'] + '\n')
            map_dir = acl_dir + init + '/' + dev['lun'] + '/'
            log.write('[INFO] Creating sysfs entry: ' + map_dir + '\n')
            os.makedirs(map_dir)
            log.write('[INFO] Creating symlink: ' + map_dir + dev['lun'] + ' -> ' + dev_lun_dir + '\n')
            os.symlink(dev_lun_dir, map_dir + dev['lun'])
    else:
        log.write('[WARNING] ' + dev['type'] + ' device type is not supported\n')

# To let host know that target started and to inform
# initiators about its IP we will create file in mounted folder

ip_file = open('/lio_project/session/target_ip', 'w')
ip_file.write(ipaddr)
ip_file.close()
log.write('Target IP was written to session/target_ip : ' + ipaddr + '\n')

log.close()

