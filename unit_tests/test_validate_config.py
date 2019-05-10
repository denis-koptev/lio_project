import pytest
import logging
from jsonschema import ValidationError

from .. import parse_json

LOGGER = logging.getLogger()

# Test data

empty_config = {}

valid_config = {
  "target": {
    "name": "tgt1"
  },
  "devices": [
    {
      "name": "fileio1",
      "type": "fileio",
      "size": "536870912"
    },
    {
      "name": "file1",
      "type": "file",
      "size": "536870912"
    },
  ],
  "initiators": [
    {
      "name": "init1"
    }
  ],
  "io": []
}

missing_tgt_config = {
  "devices": [
    {
      "name": "fileio1",
      "type": "fileio",
      "size": "536870912"
    }
  ],
  "initiators": []
}

invalid_type_config = {
  "target": {
    "name": "tgt1"
  },
  "devices": [
    {
      "name": "fileio1",
      "type": "fileio",
      "size": 536870912
    }
  ],
  "initiators": []
}

invalid_member_config = {
  "target": {
    "invalid_member": "tgt1"
  },
  "devices": [],
  "initiators": []
}


# Module initialization

def setup_module(module):
    pass

def teardown_module(module):
    pass


# Test functions

def test_validate_valid_config():
    parse_json.validate_json(valid_config)

def test_validate_missing_tgt_config():
    try:
        parse_json.validate_json(missing_tgt_config)
    except ValidationError as err:
        LOGGER.info("Got expected exception: %s" % str(err)[:200])
    else:
        assert False, "Got no exception trying to validate incorrect config"

def test_validate_invalid_type_config():
    try:
        parse_json.validate_json(invalid_type_config)
    except ValidationError as err:
        LOGGER.info("Got expected exception: %s" % str(err)[:200])
    else:
        assert False, "Got no exception trying to validate incorrect config"

def test_validate_invalid_member_config():
    try:
        parse_json.validate_json(invalid_member_config)
    except ValidationError as err:
        LOGGER.info("Got expected exception: %s" % str(err)[:200])
    else:
        assert False, "Got no exception trying to validate incorrect config"


