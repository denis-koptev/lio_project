#!/bin/sh

### LIO_START_TARGET ###

echo "----- ENTERING START_TARGET SCRIPT -----"

# Run tcmu-runner

cd tcmu-runner
stty -echo
./deploy.sh
stty echo

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to start tcmu-runner daemon. Exiting..."
    exit 1
fi

cd ..

# Verify that propper modules are loaded

stty -echo
modinfo target_core_mod
stty echo

if [ $? -ne 0 ]; then
    echo "[ERROR] target module is not loaded. Exiting..."
    exit 1
fi

stty -echo
modinfo target_core_user
stty echo

if [ $? -ne 0 ]; then
    echo "[ERROR] target_core_user module is not loaded. Exiting..."
    exit 1
fi

# Create target devices

echo "[INFO] Creating devices."

python3 lio_create_devices.py session/dev_config.json

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create devices. Exiting..."
    exit 1
fi

echo "[INFO] Devices created successfully."

# Create target itself and notify to main script

echo "[INFO] Creating target."

python3 lio_start_target.py session/tgt_config.json

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create target. Exiting..."
    exit 1
fi

echo "[INFO] Target created successfully."

