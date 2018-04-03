import os
import sys
import json
import argparse

# START_INITIATOR SCRIPT
# Registers initiator IQN in /etc/iscsi/initiatorname.iscsi and reloads iscsid
# Takes unnecessary /path/to/log argumentm, and necessary /path/to/config argument


logfile = None


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='path to an internal initiator JSON config')
    parser.add_argument('--log', help='path where log file will be created')
    return parser.parse_args()


def log(msg):
    if logfile:
        logfile.write(msg + '\n')
    else:
        print(msg)


def get_json_from_file(path):
    if not os.path.isfile(path):
        log('[ERROR] JSON config for initiator not found')
        sys.exit(1)
    else:
        config_file = open(path, 'r')
        config = json.load(config_file)
        config_file.close()
        return config


def create_initiator(config):
    log('[INFO] Creating initiator ' + config['name'])
    iqn = config['iqn']

    if not os.path.isfile('/etc/iscsi/initiatorname.iscsi'):
        log('[ERROR] No initiatorname file found. You should install open-iscsi.')
        sys.exit(1)

    initiatorname = open('/etc/iscsi/initiatorname.iscsi', 'w')
    initiatorname.write('InitiatorName=' + iqn + '\n')
    initiatorname.close()

    log('[INFO] Restarting iscsid service')
    os.system('service iscsid restart')

    log('[INFO] Successfully registered initiator IQN')


def main():
    global logfile
    args = parse_args()
    if args.log:
        logfile = open(args.log, 'w')
    config = get_json_from_file(args.config)
    create_initiator(config)
    if args.log:
        logfile.close()


if __name__ == '__main__':
    main()

