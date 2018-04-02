import re
import os
import sys
import time
import json

# FIND_DEV SCRIPT
# Parses file with device list using regular expressions
# Returns LUN and device name in /dev

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


def main():

    if len(sys.argv) != 3:
        print('[ERROR] Not enough arguments provided')
        print('[INFO] Usage: run_io.py /path/to/dev/list /path/to/init/config')
        sys.exit(1)

    # TODO: Insert checks
    dev_path = sys.argv[1]
    config_file = open(sys.argv[2], 'r')
    config = json.load(config_file)
    config_file.close()

    devices = parse_lio_dev(dev_path)
    print('[INFO] Found following devices: ' + str(devices))

    # This is just for testing purposes
    for dev in config['devices']:
        print('[INFO] Starting random IO to %s with %s type and lun=%s' % (dev['name'], dev['type'], dev['lun']))

        # Search device name in /dev
        dev_names = [item['dev'] for item in devices if item['lun'] == dev['lun']]
        if len(dev_names) == 0:
            print('[WARNING] Device was not found in /dev. Skipping.')
            continue
        if len(dev_names) > 1:
            print('[WARNING] More than 1 device with such lun found. Taking first.')
        dev_name = dev_names[0]

        with open('/dev/' + dev_name, 'wb') as f:
            start_time = time.time()
            for i in range(500):
                try:
                    f.write(os.urandom(1024*1024))
                except Exception as e:
                    print('[ERROR] ' + str(e))
                    break
            end_time = time.time()
            total_time = end_time - start_time
            speed = 500 / total_time
            print('[INFO] Time: %.2f s; Speed: %.2f MB/s' % (total_time, speed))

if __name__ == '__main__':
    main()

