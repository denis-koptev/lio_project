import sys
import socket
import json

# We can confirm that target started only if all configuration will be successfully created

# Create log file in shared session folder
log = open('/lio_project/session/target_log', 'w')

if len(sys.argv) < 2:
    log.write('[ERROR] Config file with JSON was not specified\n')
    sys.exit(1)

log.write('[INFO] Reading JSON config\n')

config_file = open(sys.argv[1], 'r')
config = json.load(config_file)
config_file.close()

log.write('[INFO] JSON config was successfully read\n')
log.write('[INFO] Creating target with following parameters:\n')
log.write(json.dumps(config, indent=4) + '\n')

# To let host know that target started and to inform
# initiators about its IP we will create file in mounted folder

ipaddr = socket.gethostbyname(socket.gethostname())
ip_file = open('/lio_project/session/target_ip', 'w')
ip_file.write(ipaddr)
ip_file.close()

log.close()

