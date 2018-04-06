import os
import sys
import json
import glob
import argparse


# CREATE_DEVICES SCRIPT
# Creates sysfs entries and backstores for devices
# Rakes unnecessary /path/to/log argument and necessary /path/to/config argument


logfile = None
core_dir = '/sys/kernel/config/target/core/'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='path to an internal devices JSON config')
    parser.add_argument('--log', help='path where log file will be created')
    return parser.parse_args()


def log(msg):
    if logfile:
        logfile.write(msg + '\n')
    else:
        print(msg)


def get_json_from_file(path):
    if not os.path.isfile(path):
        log('[ERROR] JSON config for devices not found')
        sys.exit(1)
    else:
        config_file = open(path, 'r')
        config = json.load(config_file)
        config_file.close()
        return config


def create_device(config):
    if config['type'] == 'fileio':
        log('[INFO] Configuring fileio device ' + config['name'] + ' and creating storage')
        type_dir = core_dir + 'fileio_'
        log('[INFO] Creating backstore for device ' + config['name'])
        storage = open('/' + config['name'], 'w')
        storage.truncate(int(config['size']))
        storage.close()
        # Config string for sysfs entry
        control = 'fd_dev_name=/' + config['name'] + ',fd_dev_size=' + config['size'] 
    elif config['type'] == 'alloc' or config['type'] == 'file':
        log('[INFO] Configuring user device ' + config['type'] + '/' + config['name'])
        type_dir = core_dir + 'user_'
        control = 'dev_size=' + config['size'] + ',dev_config=' + config['type'] + '/' + config['name']
    else:
        log('[WARNING] Device type ' + config['type'] + ' is not supported')
        return

    # Discover existing paths for devices
    dev_paths = [ dev for dev in glob.glob(type_dir + '*/' + config['name']) ]

    if len(dev_paths) != 0:
        log('[WARNING] There is another device with name: ' + config['name'])
        log('[WARNING] Skipping...')
        return

    log('[INFO] Creating ' + config['type'] + ' device with name: ' + config['name'])
    idx = 0

    while os.path.isdir(type_dir + str(idx)):
        idx = idx + 1

    type_dir = type_dir + str(idx) + '/'
    log('[INFO] Creating entry in sysfs: ' + type_dir)
    os.makedirs(type_dir)

    dev_dir = type_dir + config['name'] + '/'
    log('[INFO] Creating entry in sysfs: ' + dev_dir)
    os.makedirs(dev_dir)

    log('[INFO] Configuring params of device ' + config['name'])
    open(dev_dir + 'control', 'w').write(control)
    log('[INFO] Enabling device ' + config['name'])
    open(dev_dir + 'enable', 'w').write('1')


def main():
    global logfile
    args = parse_args()
    if args.log:
        logfile = open(args.log, 'w')
    config = get_json_from_file(args.config)

    log('[INFO] JSON config was successfully read')
    log('[INFO] Creating devices')

    if not os.path.isdir(core_dir):
        log('[ERROR] No sysfs entry created for devices')
        sys.exit(1)

    for dev in config:
        create_device(dev)

    log('[INFO] Finished creating devices')
    logfile.close()

if __name__ == '__main__':
    main()

