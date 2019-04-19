import subprocess
import pytest
import os
import logging

from .. import start_target
from .. import create_devices

LOGGER = logging.getLogger(__name__)

# Test data

valid_full_config = {
    "name": "tgt1",
    "iqn": "iqn.2019-04.com.lio-project:tgt-tgt1",
    "devices": [
        {
            "name": "fileio1",
            "type": "fileio",
            "size": "536870912",
            "lun": "lun_0"
        },
    ],
    "acl": [
        "iqn.2019-04.com.lio-project:init-init1"
    ]
}

valid_tgt_config = {
        "name": "tgt1",
        "iqn": "iqn.2019-04.com.lio-project:tgt-tgt1"
}

invalid_tgt_config = {
        "name": "tgt2",
        "iqn": "invalid_iqn"
}


empty_config = {}


# Module initialization

def setup_module(module):
    os.chdir("../")
    try:
        os.makedirs("session")
    except:
        pass
    open("session/target_ip", "w").write("0.0.0.0")



def teardown_module(module):
    flush_kernel_devices()


# Helper functions

def verify_tgt_data(tgt_name):
    # Call special iSCSI CLI to get device
    output = subprocess.getstatusoutput("targetcli ls iscsi/%s" % str(tgt_name))
    if output[0] != 0:
        LOGGER.info("Failed to get target %s: %s" % (str(dev_name), str(output[1])))
        return False
    # If we succeeded to run command, find target_name in output
    # If name is found we consider that target is created
    return tgt_name in output[1]

def verify_portal_data(tgt_name):
    output = subprocess.getstatusoutput("targetcli ls iscsi/%s/tpg1/portals" % tgt_name)
    if output[0] != 0:
        LOGGER.info("Failed to get portal: %s" % str(output[1]))
        return False
    return "Portals: 0" not in output[1]

def verify_lun_data(tgt_name, lun):
    output = subprocess.getstatusoutput("targetcli ls iscsi/%s/tpg1/luns" % tgt_name)
    if output[0] != 0:
        LOGGER.info("Failed to get luns: %s" % str(output[1]))
        return False
    return lun in output[1]

# For cleanup

def flush_kernel_devices():
    LOGGER.info("Clearing test data...")
    res = subprocess.getstatusoutput("targetcli clearconfig confirm=True")
    LOGGER.info("Cleanup result: %s" % str(res))

@pytest.fixture(autouse=True)
def cleanup_each_test():
    flush_kernel_devices()


# Test functions

def test_empty_config():
    result = start_target.create_target(empty_config)
    assert not result["success"], "Got success while creating target with empty config"

def test_valid_full_config():
    # Create test device first
    result = create_devices.create_device(valid_full_config["devices"][0])
    if not result["success"]:
        message = "Failed to create device: %s" % result["message"]
        assert False, message

    # Create target
    tgt_name = valid_full_config["iqn"]
    result = start_target.create_target(valid_full_config)
    message = None
    dump = ""

    if not result["success"]:
        message = "Failed to create target: %s" % result["message"]

    if not verify_tgt_data(tgt_name):
        message = "Target not found in SYSFS"
    
    if not verify_portal_data(tgt_name):
        message = "Portal not found in SYSFS"

    last_lun = "lun%d" % (len(valid_full_config["devices"]) - 1)
    if not verify_lun_data(tgt_name, last_lun):
        message = "lun1 not found for target"

    if message is not None:
        dump_res = subprocess.getstatusoutput("targetcli ls")
        if dump_res[0] != 0:
            dump = "Failed to get dump: %s" % dump_res[1]
        dump = dump_res[1]
        LOGGER.info("DUMP: %s" % dump)
        assert False, message

def test_valid_target():
    tgt_name = valid_tgt_config["iqn"]
    result = start_target.create_main_target_dir(valid_tgt_config)

    assert result["success"], "Failed to create target: %s" % result["message"]

def test_same_target():
    tgt_name = valid_tgt_config["iqn"]
    result = start_target.create_main_target_dir(valid_tgt_config)
    assert result["success"], "Failed to create first target: %s" % result["message"]

    err_msg = "Target exists: %s" % tgt_name
    result = start_target.create_main_target_dir(valid_tgt_config)
    assert not result["success"], "Got successfull result trying to create the same target"
    assert result["message"] == err_msg, "Got unexpected error message %s" % result["message"]
    LOGGER.info("Got expected error trying to create the same target: %s" % result["message"])

def test_invalid_target():
    result = start_target.create_main_target_dir(invalid_tgt_config)
    assert not result["success"], "Got success while creating invalid target"
    LOGGER.info("Got expected error trying to create invalid target: %s" % result["message"])

