#!/usr/bin/env python3

'''

CREATE_DEVICES SCRIPT
Creates sysfs entries and backstores for devices
Takes unnecessary /path/to/LOG argument
Takes necessary /path/to/config argument

'''

import os
import sys
import json
import glob
import argparse
# from subprocess import getstatusoutput
import logging
import logging.config


logging.config.fileConfig('logging.conf')
LOG = logging.getLogger('createdevices')

CORE_DIR = '/sys/kernel/config/target/core/'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='path to an internal'
                        'devices JSON config')
    parser.add_argument('--log', help='path where LOG file will be created')
    return parser.parse_args()


def get_json_from_file(path):
    if not os.path.isfile(path):
        LOG.error('JSON config for devices not found')
        sys.exit(1)
    else:
        config_file = open(path, 'r')
        config = json.load(config_file)
        config_file.close()
        return config


'''
def create_logical_volume(vol_name, vol_size):
    file_name = 'file_lv_' + vol_name
    file_path = '/' + file_name
    file_size = str(int(int(vol_size)*1.2))
    file_cmd = 'truncate --size {} {}'.format(file_size, file_path)
    status, output = getstatusoutput(file_cmd)
    LOG.info(str(status))
    LOG.info(output)

    dev_path_cmd = 'losetup --find --show {}'.format(file_path)
    status, output = getstatusoutput(dev_path_cmd)
    dev_path = output
    LOG.info(str(status))
    LOG.info(output)

    vg_name = 'vg_' + vol_name
    vol_name = 'lv_' + vol_name
    vg_cmd = 'vgcreate {} {}'.format(vg_name, dev_path)
    status, output = getstatusoutput(vg_cmd)
    LOG.info(str(status))
    LOG.info(output)
    lv_cmd = 'lvcreate --size {} --name {} {}'.format(vol_size, vol_name, vg_name)
    status, output = getstatusoutput(lv_cmd)
    LOG.info(str(status))
    LOG.info(output)

    return vg_name, vol_name
'''


def create_device(config):
    # Validate input configuration
    if ("type" not in config) or\
       ("name" not in config) or\
       ("size" not in config):
        LOG.error("Config for device must contain type, name and size")
        return {"success": False, "message": "Invalid config: %s" % str(config)}

    if config['type'] == 'fileio':
        LOG.info('Configuring fileio device %s '
                 'and creaing storage' % config['name'])
        type_dir = CORE_DIR + 'fileio_'
        LOG.debug('Creating backstore for device %s' % config['name'])

        try:
            storage = open('/' + config['name'], 'w')
            storage.truncate(int(config['size']))
            storage.close()
        except IOError as io_err:
            LOG.error("Failed to create file %s: %s" % (config['name'], str(io_err)))
            return {"success": False, "message": str(io_err)}

        # Config string for sysfs entry
        control = 'fd_dev_name=/' + config['name'] + ',fd_dev_size=' + config['size']

    elif config['type'] == 'block':
        LOG.info('Configuring block device %s with existing storage' % config['name'])
        type_dir = CORE_DIR + 'iblock_'

        if 'path' not in config:
            LOG.error('Path to an existing storage for block device not found in config')
            return {"success": False, "message":"Path to an existing storage for block device not found in config"}

        if not os.path.islink(config['path']):
            LOG.error('Logical volume not found in %s' % config['path'])
            return {"success": False, "message":"Logical volume not found"}

        control = 'udev_path={}'.format(config['path'])

    elif config['type'] == 'alloc' or config['type'] == 'file':
        LOG.info('Configuring user device %s/%s' %
                 (config['type'], config['name']))
        type_dir = CORE_DIR + 'user_'
        control = 'dev_size=' + config['size'] + ',dev_config=' + config['type'] + '/' + config['name']

    else:
        LOG.warning('Device type %s is not supported' % config['type'])
        return {"success": False, "message": "Device type %s not supported" % config['type']}

    # Discover existing paths for devices
    dev_paths = [dev for dev in glob.glob(type_dir + '*/' + config['name'])]

    if dev_paths:
        LOG.warning('There is another device with name: %s. Skipping...'
                    % config['name'])
        return {"success": False, "message": "There is another device with name %s" % config['name']}

    LOG.info('Creating %s device with name: %s'
             % (config['type'], config['name']))
    idx = 0

    while os.path.isdir(type_dir + str(idx)):
        idx = idx + 1

    try:
        type_dir = type_dir + str(idx) + '/'
        LOG.debug('Creating entry in sysfs: %s' % type_dir)
        os.makedirs(type_dir)

        dev_dir = type_dir + config['name'] + '/'
        LOG.debug('Creating entry in sysfs: %s' % dev_dir)
        os.makedirs(dev_dir)

        LOG.debug('Configuring params of device %s' % config['name'])
        open(dev_dir + 'control', 'w').write(control)
        LOG.debug('Enabling device %s' % config['name'])
        open(dev_dir + 'enable', 'w').write('1')
    except IOError as io_err:
        LOG.error("Failed to create entry in sysfs: %s" % str(io_err))
        return {"success": False, "message": "SYSFS error: %s" % str(io_err)}

    return {"success": True, "message": "Device %s successfully created" % config['name']}


def main():
    global LOG
    args = parse_args()
    #if args.log:
    #    LOG = Logger(filename=args.log)
    config = get_json_from_file(args.config)

    LOG.info('JSON config was successfully read')
    LOG.info('Creating devices')

    if not os.path.isdir(CORE_DIR):
        LOG.error('No sysfs entry created for devices')
        sys.exit(1)

    for dev in config:
        create_device(dev)

    LOG.info('Finished creating devices')

    #if args.log:
    #    LOG.close()


if __name__ == '__main__':
    main()
