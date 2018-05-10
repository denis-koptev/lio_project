import os
import sys
import json
import glob
import argparse
from logger import Logger

# CREATE_DEVICES SCRIPT
# Creates sysfs entries and backstores for devices
# Takes unnecessary /path/to/log argument
# Takes necessary /path/to/config argument


log = Logger()
core_dir = '/sys/kernel/config/target/core/'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='path to an internal'
                        'devices JSON config')
    parser.add_argument('--log', help='path where log file will be created')
    return parser.parse_args()


def get_json_from_file(path):
    if not os.path.isfile(path):
        log.error('JSON config for devices not found')
        sys.exit(1)
    else:
        config_file = open(path, 'r')
        config = json.load(config_file)
        config_file.close()
        return config


def create_device(config):
    if config['type'] == 'fileio':
        log.info('Configuring fileio device %s '
                 'and creaing storage' % config['name'])
        type_dir = core_dir + 'fileio_'
        log.info('Creating backstore for device %s' % config['name'])
        storage = open('/' + config['name'], 'w')
        storage.truncate(int(config['size']))
        storage.close()
        # Config string for sysfs entry
        control = 'fd_dev_name=/' + config['name'] +
        ',fd_dev_size=' + config['size']
    elif config['type'] == 'alloc' or config['type'] == 'file':
        log.info('Configuring user device %s/%s' %
                 (config['type'], config['name']))
        type_dir = core_dir + 'user_'
        control = 'dev_size=' + config['size'] + ',dev_config=' +
        config['type'] + '/' + config['name']
    else:
        log.warning('Device type %s is not supported' % config['type'])
        return

    # Discover existing paths for devices
    dev_paths = [dev for dev in glob.glob(type_dir + '*/' + config['name'])]

    if len(dev_paths) != 0:
        log.warning('There is another device with name: %s. Skipping...'
                    % config['name'])
        return

    log.info('Creating %s device with name: %s'
             % (config['type'], config['name']))
    idx = 0

    while os.path.isdir(type_dir + str(idx)):
        idx = idx + 1

    type_dir = type_dir + str(idx) + '/'
    log.info('Creating entry in sysfs: %s' % type_dir)
    os.makedirs(type_dir)

    dev_dir = type_dir + config['name'] + '/'
    log.info('Creating entry in sysfs: %s' % dev_dir)
    os.makedirs(dev_dir)

    log.info('Configuring params of device %s' % config['name'])
    open(dev_dir + 'control', 'w').write(control)
    log.info('Enabling device %s' % config['name'])
    open(dev_dir + 'enable', 'w').write('1')


def main():
    global log
    args = parse_args()
    if args.log:
        log = Logger(filename=args.log)
    config = get_json_from_file(args.config)

    log.info('JSON config was successfully read')
    log.info('Creating devices')

    if not os.path.isdir(core_dir):
        log.error('No sysfs entry created for devices')
        sys.exit(1)

    for dev in config:
        create_device(dev)

    log.info('Finished creating devices')

    if args.log:
        log.close()


if __name__ == '__main__':
    main()
