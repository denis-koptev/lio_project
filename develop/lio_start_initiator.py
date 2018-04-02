import os
import sys
import json


if len(sys.argv) != 2:
    print('[ERROR] You need to specify /path/to/config.json')
    sys.exit(1)

if not os.path.isfile(sys.argv[1]):
    print('[ERROR] Config file not found')
    sys.exit(1)

config_file = open(sys.argv[1], 'r')
config = json.load(config_file)
config_file.close()

print('[INFO] Creating initiator with the following config:')
print(json.dumps(config, indent=4))

iqn = config['iqn']

if not os.path.isfile('/etc/iscsi/initiatorname.iscsi'):
    print('[ERROR] No initiatorname file found. You should install open-iscsi.')
    sys.exit(1)

initiatorname = open('/etc/iscsi/initiatorname.iscsi', 'w')
initiatorname.write('InitiatorName=' + iqn + '\n')
initiatorname.close()

os.system('service iscsid restart')

print('[INFO] Successfully registered initiator IQN')

