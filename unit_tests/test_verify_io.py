import pytest
from .. import verify_io

# Test data

empty_config = {}

error_msg_config = [
    {
        "success": 0,
        "message": "error message",
        "dev_path": "/dev/sdb",
        "dev_size": 0,
        "bs": 0,
        "total_time": 0,
        "speed": 0,
        "dev_name": "file1",
        "dev_type": "file",
        "dev_lun": "lun_0"
    },
]

good_config = [
    {
        "success": 1,
        "message": "OK",
        "dev_path": "/dev/sdb",
        "dev_size": 536870912,
        "bs": 4096,
        "total_time": "3.91",
        "speed": "130.91",
        "dev_name": "file1",
        "dev_type": "file",
        "dev_lun": "lun_0"
    },
]

incomplete_err_config = good_config

# Module initialization

def setup_module(module):
    pass

def teardown_module(module):
    pass


# Test functions

def test_empty_config():
    res, reports = verify_io.verify_io_success(empty_config)
    assert res == True, "Got unsuccessful result for empty config"
    assert len(reports) == 0, "Got non-empty reports for empty config"

def test_error_message():
    res, reports = verify_io.verify_io_success(error_msg_config)

    assert res != True, "Got successful result for unsuccessful IO"
    if not res:
        print("Got expected error message")

    assert len(reports) == 1, \
            "Length of reports for unsuccessful config is not 1: %d" % len(reports)

    assert ((error_msg_config[0]["dev_name"] in reports[0]) and \
            (error_msg_config[0]["message"] in reports[0])), \
            "dev_name and error message not found in report: %s" % reports[1]

def test_successfull_io():
    res, reports = verify_io.verify_io_success(good_config)
    assert res == True, "Got unsuccessful result for successful IO"

def test_incomplete_config():
    # Delete every field in config one by one and check if script is
    # able to return error gracefully
    keys = [ k for k in incomplete_err_config[0].keys() ]
    for k in keys:
        incomplete_err_config[0].pop(k)
        _ = verify_io.verify_io_success(incomplete_err_config)

