import os
import sys
import json
import glob

# Create log file in shared session folder
log = open('session/dev_log', 'w')

if len(sys.argv) < 2:
    log.write('[ERROR] Config file with JSON was not specified\n')
    sys.exit(1)


log.write('[INFO] Reading JSON config\n')

config_file = open(sys.argv[1], 'r')
config = json.load(config_file)
config_file.close()

log.write('[INFO] JSON config was successfully read\n')
log.write('[INFO] Creating devices with following parameters:\n')
log.write(json.dumps(config, indent=4) + '\n')

core_dir = '/sys/kernel/config/target/core/'

if not os.path.isdir(core_dir):
    log.write('[ERROR] No sysfs entry created for devices')

for dev in config:
    if dev['type'] == 'fileio':
        log.write('[INFO] Configuring fileio device ' + dev['name'] + '  and creating storage\n')
        type_dir = core_dir + 'fileio_'
        # Create file itself
        storage = open('/' + dev['name'], 'w')
        storage.truncate(int(dev['size']))
        storage.close()
        control = 'fd_dev_name=/' + dev['name'] + ',fd_dev_size=' + dev['size'] 
    elif dev['type'] == 'alloc' or dev['type'] == 'file':
        log.write('[INFO] Configuring user device ' + dev['type'] + '/' + dev['name'] + '\n')
        type_dir = core_dir + 'user_'
        control = 'dev_size=' + dev['size'] + ',dev_config=' + dev['type'] + '/' + dev['name']
    else:
        log.write('[WARNING] Device type ' + dev['type'] + ' is not supported\n')
        continue

    dev_paths = [ dev for dev in glob.glob(type_dir + '*/' + dev['name']) ]

    if len(dev_paths) != 0:
        log.write('[WARNING] There is another device with name: ' + dev['name'] + '\n')
        log.write('[WARNING] Skipping...\n')
        continue

    log.write('[INFO] Creating ' + dev['type'] + ' device with name: ' + dev['name'] + '\n')
    idx = 0

    while os.path.isdir(type_dir + str(idx)):
        idx = idx + 1

    type_dir = type_dir + str(idx) + '/'
    log.write('[INFO] Creating entry in sysfs: ' + type_dir + '\n')
    os.makedirs(type_dir)

    dev_dir = type_dir + dev['name'] + '/'
    log.write('[INFO] Creating entry in sysfs: ' + dev_dir + '\n')
    os.makedirs(dev_dir)

    log.write('[INFO] Configuring params of device ' + dev['name'] + '\n')
    open(dev_dir + 'control', 'w').write(control)
    log.write('[INFO] Enabling device ' + dev['name'] + '\n')
    open(dev_dir + 'enable', 'w').write('1')

log.write('[INFO] Finished creating devices\n')
log.close()

