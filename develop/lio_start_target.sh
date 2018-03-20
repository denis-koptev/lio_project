#!/bin/sh

# Run tcmu-runner

# There should be checks that: target module is loaded, tcmu-runner is loaded

# To identify that docker target started we will create file with target ip in session mounted folder
# echo `hostname -I | cut -d' ' -f1` > /lio_project/session/target_ip

# Create target devices

python3 /lio_project/lio_create_devices.py /lio_project/session/dev_config.json

# Create target itself and notify host script

python3 /lio_project/lio_start_target.py /lio_project/session/tgt_config.json
