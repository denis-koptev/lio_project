#!/usr/bin/env python3

'''

START_TARGET SCRIPT
Creates target IQN, TPG, LUNs, LUN-maps and etc.
Takes unnecessary /path/to/LOG argument and necessary /path/to/config argument

'''

import os
import sys
import socket
import json
import glob
import argparse
import re
from .logger import Logger


LOG = Logger()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='path to and internal target JSON config')
    parser.add_argument('--log', help='path where LOG file will be created')
    return parser.parse_args()


def get_json_from_file(path):
    if not os.path.isfile(path):
        LOG.error('JSON config for target not found')
        sys.exit(1)
    else:
        config_file = open(path, 'r')
        config = json.load(config_file)
        config_file.close()
        return config


def build_func_result(success, message, args=[]):
    return {
        "success": success, 
        "message": message,
        "args": args
    }

def create_main_target_dir(config):
    # Verify IQN format
    if re.match(r"iqn\..[0-9\-]*\.[a-zA-Z\.\:]*", config["iqn"]) is None:
        LOG.error("IQN does not match standards: %s" % config["iqn"])
        return build_func_result(False, "IQN does not match standards: %s" % config["iqn"])

    iscsi_dir = '/sys/kernel/config/target/iscsi/'
    tgt_dir = iscsi_dir + config['iqn'] + '/'

    LOG.info('Creating Target IQN: %s' % config['iqn'])

    if not os.path.isdir(iscsi_dir):
        LOG.error('Directory for target configuration does not exist')
        return build_funct_result(False, "Directory for target configuration does not exist")

    if os.path.isdir(tgt_dir):
        LOG.warning('Target with such iqn exists: %s' % config['iqn'])
        return build_func_result(False, "Target exists: %s" % config['iqn'], [tgt_dir])
    else:
        LOG.info('Creating entry in sysfs: %s' % tgt_dir)
        try:
            os.makedirs(tgt_dir)
        except OSError as os_err:
            LOG.error("Failed to create target directory: %s" % str(os_err))
            return build_func_result(False, "Failed to create target: %s" % str(os_err))

    return build_func_result(True, "Successfully created", [tgt_dir])


def create_tpg(config, tgt_dir):
    tpg_dir = tgt_dir + 'tpgt_1/'
    if os.path.isdir(tpg_dir):
        LOG.warning('Target Portal Group already exists')
        return build_func_result(False, "Target Portal Group already exists", [tpg_dir])

    os.makedirs(tpg_dir)
    LOG.info('Created entry in sysfs: %s' % tpg_dir)
    return build_func_result(True, "Target Portal Group successfully created", [tpg_dir])


def add_single_lun(dev, config, tpg_dir, acl_dir):
    lun_dir = tpg_dir + 'lun/'
    if not os.path.isdir(lun_dir):
        LOG.error('No sysfs entry for luns created: %s' % lun_dir)
        return build_func_result(False, "No sysfs entry for luns")

    core_path = '/sys/kernel/config/target/core/'
    if not os.path.isdir(core_path):
        LOG.error('sysfs entry for devices is not presented')
        return build_func_result(False, "No sysfs entry for devices")

    if dev['type'] == 'fileio':
        type_path = core_path + 'fileio_*/'
    elif dev['type'] == 'block':
        type_path = core_path + 'iblock_*/'
    elif dev['type'] == 'file' or dev['type'] == 'alloc':
        type_path = core_path + 'user_*/'
    else:
        LOG.warning('%s device type is not supported' % dev['type'])
        return build_func_result(False, "Device type %s not supported" % dev["type"])

    dev_paths = [dev for dev in glob.glob(type_path + dev['name'])]
    if not dev_paths:
        LOG.warning('Device ' + dev['name'] + ' not found. Skipping all for it.')
        return build_func_result(False, "Device %s not found" % dev["name"])

    if len(dev_paths) > 1:
        LOG.error('More than 1 %s devices with name %s exist' % (dev['type'], dev['name']))
        LOG.error(' '.join(dev_paths))
        sys.exit(1)

    dev_lun_dir = lun_dir + dev['lun'] + '/'
    if os.path.isdir(dev_lun_dir):
        LOG.warning('sysfs entry already exists: %s' % dev_lun_dir)
        LOG.warning('Skipping...')
        return build_func_result(False, "LUN already exists")

    LOG.info('Creating sysfs entry: %s' % dev_lun_dir)
    os.makedirs(dev_lun_dir)
    LOG.info('Creating symlink to %s' % dev_paths[0])
    os.symlink(dev_paths[0], dev_lun_dir + dev['name'])

    # Make lun mapping
    for init in config['acl']:
        # acl_dir + init
        LOG.info('Creating lun mapping: %s -> %s' % (init, dev['name']))
        map_dir = acl_dir + init + '/' + dev['lun'] + '/'
        if os.path.isdir(map_dir):
            LOG.warning('Sysfs entry for lun-map already exists: %s' % map_dir)
            LOG.warning('Skipping creation of entire lun-map with symlink...')
            return build_func_result(False, "Mapping already exists")

        LOG.info('Creating sysfs entry: %s' % map_dir)
        os.makedirs(map_dir)
        LOG.info('Creating symlink: %s -> %s' % (map_dir + dev['lun'], dev_lun_dir))
        os.symlink(dev_lun_dir, map_dir + dev['lun'])

    return build_func_result(True, "LUN successfully created")


def add_luns(config, tpg_dir, acl_dir):

    for dev in config['devices']:
        result = add_single_lun(dev, config, tpg_dir, acl_dir)

    return build_func_result(True, "Successfully created all luns")


# This function needs to be split
def create_target(config):
    LOG.info('JSON config was successfully read')
    LOG.info('Creating target with name:  %s' % config['name'])

    # Create target itself via sysfs
    result = create_main_target_dir(config)
    if not result["args"]:
        sys.exit(1)

    tgt_dir = result["args"][0]

    # Create target portal group

    LOG.info('Creating Target Portal Group: tpgt_1')

    result = create_tpg(config, tgt_dir)
    if not result["args"]:
        sys.exit(1)

    tpg_dir = result["args"][0]

    # Enable target

    LOG.info('Enabling target')
    open(tpg_dir + 'enable', 'w').write('1')

    # Set no auth

    LOG.info('Switching auth off')

    attrib_dir = tpg_dir + 'attrib/'
    param_dir = tpg_dir + 'param/'
    if not os.path.isdir(attrib_dir) or not os.path.isdir(param_dir):
        LOG.error('No sysfs entries for AUTH configuration found')
        sys.exit(1)
    else:
        open(attrib_dir + 'authentication', 'w').write('0')
        open(param_dir + 'AuthMethod', 'w').write('None')

    # Fill ACL

    LOG.info('Creating ACL')

    acl_dir = tpg_dir + 'acls/'
    if not os.path.isdir(acl_dir):
        LOG.error('No sysfs entry for ACLs created')
        sys.exit(1)

    for iqn in config['acl']:
        if os.path.isdir(acl_dir + iqn):
            LOG.warning('IQN %s already presented in ACL' % iqn)
        else:
            LOG.info('Creating entry in sysfs: %s' % (acl_dir + iqn))
            os.makedirs(acl_dir + iqn)

    # Create portal

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ipaddr = s.getsockname()[0]
    s.close()
    LOG.info('Creating portal using IP: %s' % ipaddr)

    portal_dir = tpg_dir + 'np/'
    ip_dir = portal_dir + ipaddr + ':3260/'
    if not os.path.isdir(portal_dir):
        LOG.error('No sysfs entry for portal created')
        sys.exit(1)
    else:
        if os.path.isdir(ip_dir):
            LOG.warning('Portal %s:3260 already presented' % ipaddr)
        else:
            LOG.info('Creating entry in sysfs: %s' % ip_dir)
            os.makedirs(ip_dir)

    # Add luns for devices if exist

    LOG.info('Binding backstores with target')
    result = add_luns(config, tpg_dir, acl_dir)
    if not result["success"]:
        sys.exit(1)

    # To let host know that target started and to inform
    # initiators about its IP we will create file in mounted folder

    ip_file = open('session/target_ip', 'w')
    ip_file.write(ipaddr)
    ip_file.close()
    LOG.info('Target IP was written to session/target_ip: %s' % ipaddr)

    return build_func_result(True, "Successfully create target")


def main():
    global LOG
    args = parse_args()
    if args.log:
        LOG = Logger(filename=args.log)
    config = get_json_from_file(args.config)
    create_target(config)
    if args.log:
        LOG.close()


if __name__ == '__main__':
    main()
