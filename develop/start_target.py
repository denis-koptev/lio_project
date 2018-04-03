import os
import sys
import socket
import json
import glob
import argparse

# START_TARGET SCRIPT
# Creates target IQN, TPG, LUNs, LUN-maps and etc.
# Takes unnecessary /path/to/log argument and necessary /path/to/config argument


logfile = None


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='path to and internal target JSON config')
    parser.add_argument('--log', help='path where log file will be created')
    return parser.parse_args()


def log(msg):
    if logfile:
        logfile.write(msg + '\n')
    else:
        print(msg)


def get_json_from_file(path):
    if not os.path.isfile(path):
        log('[ERROR] JSON config for target not found')
        sys.exit(1)
    else:
        config_file = open(path, 'r')
        config = json.load(config_file)
        config_file.close()
        return config


# This function needs to be splitted
def create_target(config):
    log('[INFO] JSON config was successfully read')
    log('[INFO] Creating target with name:  %s' % config['name'])

    # Create target itself via sysfs

    iscsi_dir = '/sys/kernel/config/target/iscsi/'
    tgt_dir = iscsi_dir + config['iqn'] + '/'

    log('[INFO] Creating Target IQN: ' + config['iqn'])

    if not os.path.isdir(iscsi_dir):
        log('[ERROR] Directory for target configuration does not exist')
        sys.exit(1)

    if os.path.isdir(tgt_dir):
        log('[WARNING] Target with such iqn exists: ' + config['iqn'])
    else:
        log('[INFO] Creating entry in sysfs: ' + tgt_dir)
        os.makedirs(tgt_dir)

    # Create target portal group

    log('[INFO] Creating Target Portal Group: tpgt_1')

    tpg_dir = tgt_dir + 'tpgt_1/'
    if os.path.isdir(tpg_dir):
        log('[WARNING] Target Portal Group already exists')
    else:
        os.makedirs(tpg_dir)
        log('[INFO] Creating entry in sysfs: ' + tpg_dir)

    # Enable target

    log('[INFO] Enabling target')
    open(tpg_dir + 'enable', 'w').write('1')

    # Set no auth

    log('[INFO] Switching auth off')

    attrib_dir = tpg_dir + 'attrib/'
    param_dir = tpg_dir + 'param/'
    if not os.path.isdir(attrib_dir) or not os.path.isdir(param_dir):
        log('[ERROR] No sysfs entries for AUTH configuration')
        sys.exit(1)
    else:
        open(attrib_dir + 'authentication', 'w').write('0')
        open(param_dir + 'AuthMethod', 'w').write('None')

    # Fill ACL

    log('[INFO] Creating ACL')

    acl_dir = tpg_dir + 'acls/'
    if not os.path.isdir(acl_dir):
        log('[ERROR] No sysfs entry for ACLs created')
        sys.exit(1)

    for iqn in config['acl']:
        if os.path.isdir(acl_dir + iqn):
            log('[WARNING] IQN ' + iqn + ' already presented in ACL')
        else:
            log('[INFO] Creating entry in sysfs: ' + acl_dir + iqn)
            os.makedirs(acl_dir + iqn)

    # Create portal

    ipaddr = socket.gethostbyname(socket.gethostname())
    log('[INFO] Creating portal using IP: ' + ipaddr)

    portal_dir = tpg_dir + 'np/'
    ip_dir = portal_dir + ipaddr + ':3260/'
    if not os.path.isdir(portal_dir):
        log('[ERROR] No sysfs entry for portal created')
        sys.exit(1)
    else:
        if os.path.isdir(ip_dir):
            log('[WARNING] Portal ' + ipaddr + ':3260 already presented')
        else:
            log('[INFO] Creating entry in sysfs: ' + ip_dir)
            os.makedirs(ip_dir)

    # Add luns for devices if exist

    log('[INFO] Binding backstores with target')

    lun_dir = tpg_dir + 'lun/'
    if not os.path.isdir(lun_dir):
        log('[ERROR] No sysfs entry for luns created')
        sys.exit(1)

    core_path = '/sys/kernel/config/target/core/'
    if not os.path.isdir(core_path):
        log('[ERROR] sysfs entry for devices is not presented')
        sys.exit(1)

    for dev in config['devices']:
        if dev['type'] == 'fileio':
            type_path = core_path + 'fileio_*/'
        elif dev['type'] == 'file' or dev['type'] == 'alloc':
            type_path = core_path + 'user_*/'
        else:
            log('[WARNING] ' + dev['type'] + ' device type is not supported')

        dev_paths = [ dev for dev in glob.glob(type_path + dev['name']) ]
        if len(dev_paths) == 0:
            log('[ERROR] Device ' + dev['name'] + ' not found')
            sys.exit(1)
        if len(dev_paths) > 1:
            log('[ERROR] More than 1 ' + dev['type'] + ' devices with name ' + dev['name'] + ' exist')
            log('[ERROR] '.join(dev_paths))
            sys.exit(1)
        dev_lun_dir = lun_dir + dev['lun'] + '/'
        if os.path.isdir(dev_lun_dir):
            log('[WARNING] sysfs entry already exists: ' + dev_lun_dir)
            log('[WARNING] Skipping...')
        else:
            log('[INFO] Creating sysfs entry: ' + dev_lun_dir)
            os.makedirs(dev_lun_dir)
            log('[INFO] Creating symlink to ' + dev_paths[0])
            os.symlink(dev_paths[0], dev_lun_dir + dev['name'])
        # Make lun mapping
        for init in config['acl']:
            # acl_dir + init
            log('[INFO] Creating lun mapping: ' + init + ' -> ' + dev['name'])
            map_dir = acl_dir + init + '/' + dev['lun'] + '/'
            if os.path.isdir(map_dir):
                log('[WARNING] Sysfs entry for lun-map already exists: ' + map_dir)
                log('[WARNING] Skipping creation of entire lun-map with symlink...')
            else:
                log('[INFO] Creating sysfs entry: ' + map_dir)
                os.makedirs(map_dir)
                log('[INFO] Creating symlink: ' + map_dir + dev['lun'] + ' -> ' + dev_lun_dir)
                os.symlink(dev_lun_dir, map_dir + dev['lun'])

    # To let host know that target started and to inform
    # initiators about its IP we will create file in mounted folder

    ip_file = open('session/target_ip', 'w')
    ip_file.write(ipaddr)
    ip_file.close()
    log('Target IP was written to session/target_ip : ' + ipaddr)

def main():
    global logfile
    args = parse_args()
    if args.log:
        logfile = open(args.log, 'w')
    config = get_json_from_file(args.config)
    create_target(config)
    if args.log:
        logfile.close()

if __name__ == '__main__':
    main()

