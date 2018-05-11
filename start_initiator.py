import os
import sys
import json
import argparse
from logger import Logger

# START_INITIATOR SCRIPT
# Registers initiator IQN in /etc/iscsi/initiatorname.iscsi and reloads iscsid
# Takes unnecessary /path/to/log argument, and necessary /path/to/config argument


log = Logger()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='path to an internal initiator JSON config')
    parser.add_argument('--log', help='path where log file will be created')
    return parser.parse_args()


def get_json_from_file(path):
    if not os.path.isfile(path):
        log.error('JSON config for initiator not found')
        sys.exit(1)
    else:
        config_file = open(path, 'r')
        config = json.load(config_file)
        config_file.close()
        return config


def create_initiator(config):
    log.info('Creating initiator %s' % config['name'])
    iqn = config['iqn']

    if not os.path.isfile('/etc/iscsi/initiatorname.iscsi'):
        log.error('No initiatorname file found. You should install open-iscsi.')
        sys.exit(1)

    initiatorname = open('/etc/iscsi/initiatorname.iscsi', 'w')
    initiatorname.write('InitiatorName=' + iqn + '\n')
    initiatorname.close()

    log.info('Restarting iscsid service')
    os.system('service iscsid restart')

    log.info('Successfully registered initiator IQN')


def main():
    global log
    args = parse_args()
    if args.log:
        log = Logger(filename=args.log)
    config = get_json_from_file(args.config)
    create_initiator(config)
    if args.log:
        log.close()


if __name__ == '__main__':
    main()
