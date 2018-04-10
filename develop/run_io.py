import re
import os
import sys
import time
import json
import argparse

# RUN_IO SCRIPT
# Parses file with device list using regular expressions
# Makes IO operations to propper devices


logfile = None


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('dev_list', help='path to a file with list of devices from lsscsi call')
    parser.add_argument('init_config', help='path to an interanl initiator JSON config')
    parser.add_argument('--log', help='path where log file will be created')
    parser.add_argument('--result_path', help='path where file with IO results will be created')
    parser.add_argument('--bs', help='block size in bytes for IO operations', default=4096)
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


def parse_lio_dev(filename):
    re_lun = r'(\d+(?=].*LIO))'
    re_any = r'.*'
    re_dev = r'((?<=/dev/)\S+)'

    pattern = re.compile(re_lun + re_any + re_dev)

    with open(filename, 'r') as dev_file:
        data = dev_file.read()

    devices = []

    for dev in pattern.findall(data):
        devices.append({'lun':'lun_'+dev[0],'dev':dev[1]})

    return devices

def write_random(dev_path, size, bs):
    success = 1
    message = 'OK'
    total_time = 0
    speed = 0

    if (bs > size):
        log('[WARNING] Specified block size is larger that total io size. Reducing')
        bs = size
        message = 'OK. Block size reduced.'
    bc = int(size / bs) # Rude assumption (rounding)

    try:
        with open(dev_path, 'wb') as f:
            start_time = time.time()
            for i in range(bc):
                f.write(os.urandom(bs))
            end_time = time.time()
            total_time = end_time - start_time
            speed = size / (total_time*1024*1024)
            log('[INFO] Time: %.2f s; Speed: %.2f MB/s' % (total_time, speed))
    except Exception as e:
        success = 0
        message = 'ERROR: ' + str(e)

    return {
        'success' : success,
        'message' : message,
        'dev_path' : dev_path,
        'dev_size' : size,
        'bs' : bs,
        'total_time' : '%.2f' % total_time,
        'speed' : '%.2f' % speed
    }


def main():
    global logfile
    common_success = True
    args = parse_args()
    if args.log:
        logfile = open(args.log, 'w')
    config = get_json_from_file(args.init_config)

    if args.bs:
        bs = args.bs
    else:
        bs = 4096 # 4Kb

    if not os.path.isfile(args.dev_list):
        log('[ERROR] File with list of devices not found')
        sys.exit(1)

    devices = parse_lio_dev(args.dev_list)
    log('[INFO] Found following devices: ' + str(devices))

    results = []

    for dev in config['devices']:
        log('[INFO] Starting random IO to %s with %s type and lun=%s' % (dev['name'], dev['type'], dev['lun']))

        # Search device name in /dev
        dev_names = [item['dev'] for item in devices if item['lun'] == dev['lun']]
        if len(dev_names) == 0:
            log('[WARNING] Device was not found in /dev. Skipping.')
            continue
        if len(dev_names) > 1:
            log('[WARNING] More than 1 device with such lun found. Taking first.')
        dev_name = dev_names[0]

        result = write_random('/dev/' + dev_name, int(dev['size']), bs)
        result['dev_name'] = dev['name']
        result['dev_type'] = dev['type']
        result['dev_lun'] = dev['lun']
        results.append(result)
        if result['success'] == 0:
            common_success = False
        log('[INFO] Result: ' + str(result))

    if (args.result_path):
        result_file = open(args.result_path, 'w')
        result_file.write(json.dumps(results, indent=4))
        result_file.close()

    if not common_success:
        log('[WARNING] IO ended with errors. Check logs for details.')
        sys.exit(1)

if __name__ == '__main__':
    main()

