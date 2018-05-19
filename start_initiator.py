#!/usr/bin/env python3

'''

START_INITIATOR SCRIPT
Registers initiator IQN in /etc/iscsi/initiatorname.iscsi and reloads iscsid
Takes unnecessary /path/to/LOG argument, and necessary /path/to/config argument

'''

import os
import sys
import json
import argparse
from logger import Logger


LOG = Logger()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='path to an internal initiator JSON config')
    parser.add_argument('--log', help='path where LOG file will be created')
    return parser.parse_args()


def get_json_from_file(path):
    if not os.path.isfile(path):
        LOG.error('JSON config for initiator not found')
        sys.exit(1)
    else:
        config_file = open(path, 'r')
        config = json.load(config_file)
        config_file.close()
        return config


def create_initiator(config):
    LOG.info('Creating initiator %s' % config['name'])
    iqn = config['iqn']

    if not os.path.isfile('/etc/iscsi/initiatorname.iscsi'):
        LOG.error('No initiatorname file found. You should install open-iscsi.')
        sys.exit(1)

    initiatorname = open('/etc/iscsi/initiatorname.iscsi', 'w')
    initiatorname.write('InitiatorName=' + iqn + '\n')
    initiatorname.close()

    LOG.info('Restarting iscsid service')
    os.system('service iscsid restart')

    LOG.info('Successfully registered initiator IQN')


def main():
    global LOG
    args = parse_args()
    if args.log:
        LOG = Logger(filename=args.log)
    config = get_json_from_file(args.config)
    create_initiator(config)
    if args.log:
        LOG.close()


if __name__ == '__main__':
    main()
