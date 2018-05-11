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
from logger import Logger


LOG = Logger()
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


def create_device(config):
    if config['type'] == 'fileio':
        LOG.info('Configuring fileio device %s '
                 'and creaing storage' % config['name'])
        type_dir = CORE_DIR + 'fileio_'
        LOG.info('Creating backstore for device %s' % config['name'])
        storage = open('/' + config['name'], 'w')
        storage.truncate(int(config['size']))
        storage.close()
        # Config string for sysfs entry
        control = 'fd_dev_name=/' + config['name'] + ',fd_dev_size=' + config['size']
    elif config['type'] == 'alloc' or config['type'] == 'file':
        LOG.info('Configuring user device %s/%s' %
                 (config['type'], config['name']))
        type_dir = CORE_DIR + 'user_'
        control = 'dev_size=' + config['size'] + ',dev_config=' + config['type'] + '/' + config['name']
    else:
        LOG.warning('Device type %s is not supported' % config['type'])
        return

    # Discover existing paths for devices
    dev_paths = [dev for dev in glob.glob(type_dir + '*/' + config['name'])]

    if dev_paths:
        LOG.warning('There is another device with name: %s. Skipping...'
                    % config['name'])
        return

    LOG.info('Creating %s device with name: %s'
             % (config['type'], config['name']))
    idx = 0

    while os.path.isdir(type_dir + str(idx)):
        idx = idx + 1

    type_dir = type_dir + str(idx) + '/'
    LOG.info('Creating entry in sysfs: %s' % type_dir)
    os.makedirs(type_dir)

    dev_dir = type_dir + config['name'] + '/'
    LOG.info('Creating entry in sysfs: %s' % dev_dir)
    os.makedirs(dev_dir)

    LOG.info('Configuring params of device %s' % config['name'])
    open(dev_dir + 'control', 'w').write(control)
    LOG.info('Enabling device %s' % config['name'])
    open(dev_dir + 'enable', 'w').write('1')


def main():
    global LOG
    args = parse_args()
    if args.log:
        LOG = Logger(filename=args.log)
    config = get_json_from_file(args.config)

    LOG.info('JSON config was successfully read')
    LOG.info('Creating devices')

    if not os.path.isdir(CORE_DIR):
        LOG.error('No sysfs entry created for devices')
        sys.exit(1)

    for dev in config:
        create_device(dev)

    LOG.info('Finished creating devices')

    if args.log:
        LOG.close()


if __name__ == '__main__':
    main()
