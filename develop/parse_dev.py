import re
import sys

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


if __name__ == '__main__':
    main()

