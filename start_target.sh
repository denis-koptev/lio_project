#!/bin/sh

### LIO_START_TARGET ###

echo "----- ENTERING START_TARGET SCRIPT -----"

# Run tcmu-runner

echo "[INFO] Building and starting tcmu-runner daemon"

cd tcmu-runner
./deploy.sh > /dev/null

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to start tcmu-runner daemon. Continuing anyway..."
fi

cd ..

# Verify that propper modules are loaded

echo "[INFO] Verifying that propper modules are loaded"

modinfo target_core_mod > /dev/null

if [ $? -ne 0 ]; then
    echo "[ERROR] target module is not loaded. Exiting..."
    #exit 1
fi

modinfo target_core_user > /dev/null

if [ $? -ne 0 ]; then
    echo "[ERROR] target_core_user module is not loaded. Exiting..."
    #exit 1
fi

# Create target devices

echo "[INFO] Creating devices."

./create_devices.py session/dev_config.json --log session/dev_log

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create devices. Exiting..."
    exit 1
fi

echo "[INFO] Devices created successfully."

# Create target itself and notify to main script

echo "[INFO] Creating target."

./start_target.py session/tgt_config.json --log session/target_log

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create target. Exiting..."
    exit 1
fi

echo "[INFO] Target created successfully."

