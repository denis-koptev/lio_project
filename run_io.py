#!/usr/bin/env python3

'''

RUN_IO SCRIPT
Parses file with device list using regular expressions
Makes IO operations to propper devices

'''

import re
import os
import sys
import time
import json
import argparse
from lio_project.logger import Logger


LOG = Logger()


def parse_args():
    """ Parses arguments given to STDIN using default argparse module """

    parser = argparse.ArgumentParser()
    parser.add_argument('dev_list', help='path to a file with list of devices from lsscsi call')
    parser.add_argument('init_config', help='path to an interanl initiator JSON config')
    parser.add_argument('--log', help='path where LOG file will be created')
    parser.add_argument('--result', help='path where file with IO results will be created')
    parser.add_argument('--bs', help='block size in bytes for IO operations', default=4096)
    return parser.parse_args()


def get_json_from_file(path):
    """ Reads JSON configuration file from a given path """

    if not os.path.isfile(path):
        LOG.error('JSON config for initiator not found')
        sys.exit(1)
    else:
        config_file = open(path, 'r')
        config = json.load(config_file)
        config_file.close()
        return config


def parse_lio_dev(filename):
    """ Parses SCSI devices in a file from a given path """

    re_lun = r'(\d+(?=].*LIO))'
    re_any = r'.*'
    re_dev = r'((?<=/dev/)\S+)'

    pattern = re.compile(re_lun + re_any + re_dev)

    with open(filename, 'r') as dev_file:
        data = dev_file.read()

    devices = []

    for dev in pattern.findall(data):
        devices.append({'lun': 'lun_' + dev[0], 'dev': dev[1]})

    return devices


def write_random(dev_path, size, block_size):
    """ Executes random WRITE IO operations

    @dev_path     Path to a SCSI device to write to
    @size         Size of IO in bytes
    @block_size   Size of one IO block in bytes

    @ret          Dict with information about IO

    """

    success = 1
    message = 'OK'
    total_time = 0
    speed = 0

    if block_size > size:
        LOG.warning('Specified block size is larger that total io size. Reducing')
        block_size = size
        message = 'OK. Block size reduced.'
    block_count = int(size / block_size)  # Rude assumption (rounding)

    try:
        with open(dev_path, 'wb') as dev_file:
            start_time = time.time()
            for _ in range(block_count):
                dev_file.write(os.urandom(block_size))
            end_time = time.time()
            total_time = end_time - start_time
            speed = size / (total_time * 1024 * 1024)
            LOG.info('Time: %.2f s; Speed: %.2f MB/s' % (total_time, speed))
    except IOError as io_err:
        success = 0
        message = 'IO ERROR ({0}): {1}'.format(io_err.errno, io_err.strerror)

    return {
        'success': success,
        'message': message,
        'dev_path': dev_path,
        'dev_size': size,
        'bs': block_size,
        'total_time': '%.2f' % total_time,
        'speed': '%.2f' % speed
    }


def main():
    """ Main. Calls presented logic to run IO sessions as specified in config-file """
    # pylint: disable=locally-disabled, global-statement
    global LOG
    common_success = True
    args = parse_args()
    if args.log:
        LOG = Logger(filename=args.log)
    config = get_json_from_file(args.init_config)

    if args.bs:
        block_size = int(args.bs)
    else:
        block_size = 4096  # 4Kb

    if not os.path.isfile(args.dev_list):
        LOG.error('File with list of devices not found')
        sys.exit(1)

    devices = parse_lio_dev(args.dev_list)
    LOG.info('Found following devices: ' + str(devices))

    results = []

    for dev in config['devices']:
        LOG.info('Starting random IO to %s with %s type and lun=%s' % (dev['name'], dev['type'], dev['lun']))

        # Search device name in /dev
        dev_names = [item['dev'] for item in devices if item['lun'] == dev['lun']]
        if not dev_names:
            LOG.warning('Device was not found in /dev. Skipping.')
            continue
        if len(dev_names) > 1:
            LOG.warning('More than 1 device with such lun found. Taking first.')
        dev_name = dev_names[0]

        result = write_random('/dev/' + dev_name, int(dev['size']), block_size)
        result['dev_name'] = dev['name']
        result['dev_type'] = dev['type']
        result['dev_lun'] = dev['lun']
        results.append(result)
        if result['success'] == 0:
            common_success = False
        LOG.info('Result: %s' % str(result))

    if args.result:
        result_file = open(args.result, 'w')
        result_file.write(json.dumps(results, indent=4))
        result_file.close()

    if not common_success:
        LOG.warning('IO ended with errors. Check logs for details.')
        sys.exit(1)

    if args.log:
        LOG.close()


if __name__ == '__main__':
    main()
