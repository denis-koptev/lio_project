import re
import os
import sys
import time

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
        devices.append({'lun':dev[0],'dev':dev[1]})

    return devices


def main():
    # TODO: Insert args check
    filename = sys.argv[1]
    devices = parse_lio_dev(filename)
    print('[INFO] Found following devices: ' + str(devices))

    # This is just for testing purposes
    for dev in devices:
        print('[INFO] Starting random IO to ' + dev['dev'])
        with open('/dev/' + dev['dev'], 'wb') as f:
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

