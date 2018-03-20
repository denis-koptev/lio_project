import os
import sys
import json

# Create log file in shared session folder
log = open('/lio_project/session/dev_log', 'w')

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
    if dev['type'] == 'file':
        log.write('[INFO] Creating file device with name: ' + dev['name'] + '\n')
        type_dir = core_dir + 'fileio_'
        idx = 0

        while os.path.isdir(type_dir + str(idx)):
            idx = idx + 1

        # TODO: Insert checks for existing directories
        # TODO: Script must be able to create some parts of device with existing ones

        type_dir = type_dir + str(idx) + '/'
        log.write('[INFO] Creating entry in sysfs: ' + type_dir + '\n')
        os.makedirs(type_dir)

        dev_dir = type_dir + dev['name'] + '/'
        log.write('[INFO] Creating entry in sysfs: ' + dev_dir + '\n')
        os.makedirs(dev_dir)
        log.write('[INFO] Creating storage object: /' + dev['name'] + '\n')

        storage = open('/' + dev['name'], 'w')
        storage.truncate(int(dev['size']))
        storage.close()

        log.write('[INFO] Configuring device ' + dev['name'] + '\n')
        open(dev_dir + 'control', 'w').write('fd_dev_name=/' + dev['name'] + ',fd_dev_size=' + dev['size'])
        log.write('[INFO] Enabling device ' + dev['name'] + '\n')
        open(dev_dir + 'enable', 'w').write('1')
    else:
        log.write('[WARNING] ' + dev['type'] + ' device type is not supported\n')
        continue

log.write('[INFO] Finished creating devices\n')
log.close()

