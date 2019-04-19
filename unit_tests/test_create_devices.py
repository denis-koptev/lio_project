import subprocess
import pytest
import logging
from .. import create_devices

LOGGER = logging.getLogger(__name__)

# Test data

dev_config_valid = [
    {
        "name": "fileio1",
        "type": "fileio",
        "size": "536870912",
        "lun": "lun_0"
    },
    {
        "name": "fileio2",
        "type": "fileio",
        "size": "536870912",
        "lun": "lun_1"
    },
]

dev_config_already_done = {
    "name": "fileio3",
    "type": "fileio",
    "size": "0",
    "lun": "lun_2"
}

dev_config_invalid = {
    "name": "fileio3",
    "type": "err_type",
    "size": "0",
    "lun": "lun_4"
}

empty_config = {}

# For cleanup

def flush_kernel_devices():
    LOGGER.info("Clearing test data...")
    res = subprocess.getstatusoutput("targetcli clearconfig confirm=True")
    LOGGER.info("Cleanup result: %s" % str(res))

@pytest.fixture(autouse=True)
def cleanup_each_test():
    flush_kernel_devices()

# Module initialization

def setup_module(module):
    pass

def teardown_module(module):
    flush_kernel_devices()


# Helper functions

def verify_device_data(dev_name):
    # Call special iSCSI CLI to get device
    output = subprocess.getstatusoutput("targetcli ls backstores/fileio/%s" % str(dev_name))
    if output[0] != 0:
        LOGGER.info("Failed to get %s device: %s" % (str(dev_name), str(output[1])))
        return False
    # If we succeeded to run command, find device_name in output
    # If name is found we consider that device is created
    return dev_name in output[1]

# Test functions

def test_empty_config():
    result = create_devices.create_device(empty_config)
    assert not result["success"], "Got success while creating device with empty config"

def test_valid_config():
    # Create valid devices
    for dev in dev_config_valid:
        LOGGER.info("Creating device %s" % dev["name"])
        result = create_devices.create_device(dev)
        assert result["success"], "Failed to create valid device: %s" % result["message"]
        assert verify_device_data(dev["name"]), "Failed to find device %s" % dev["name"]

def test_invalid_config():
    err_msg = "Device type %s not supported" % dev_config_invalid["type"]
    result = create_devices.create_device(dev_config_invalid)
    assert not result["success"], "Got success trying to create device with invalid type"
    assert result["message"] == err_msg, "Got unexpected error message: %s" % result["message"]
    LOGGER.info("Got expected error trying to create invalid device: %s" % result["message"])

def test_already_done():
    err_msg = "There is another device with name %s" % dev_config_already_done["name"]
    # First create valid device
    result = create_devices.create_device(dev_config_already_done)
    assert result["success"], "Failed to create first valid device: %s" % result["message"]
    # Create device again and expect error
    result = create_devices.create_device(dev_config_already_done)
    assert not result["success"], "Got success trying to create the same device"
    assert result["message"] == err_msg, "Got unexpected error message: %s" % result["message"]
    LOGGER.info("Got expected error message trying to create the same device: %s" % result["message"])


