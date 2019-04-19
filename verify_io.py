#!/usr/bin/env python3

'''

VERIFY_IO SCRIPT
Reads file with IO result in JSON format and verifies success

'''

import os
import sys
import json
import argparse
from .logger import Logger


LOG = Logger()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('result_file', help='path to a file with IO result in JSON format')
    parser.add_argument('--log', help='path where LOG file will be created')
    return parser.parse_args()


def get_json_from_file(path):
    if not os.path.isfile(path):
        LOG.error('JSON config with IO results not found')
        sys.exit(1)
    else:
        config_file = open(path, 'r')
        config = json.load(config_file)
        config_file.close()
        return config


def verify_io_success(io_res_array):
    success = True
    error_reports = []
    for io_res in io_res_array:
        # Validate IO config
        if ("success" not in io_res) or\
           ("message" not in io_res) or\
           ("dev_name" not in io_res):
            LOG.error("Config must contain success, message and dev_name")
            return False, error_reports

        if io_res['success'] != 1:
            report = 'IO to {} failed with message: {}'.format(io_res['dev_name'], io_res['message'])
            error_reports.append(report)
            LOG.error(report)
            success = False
    return success, error_reports


def main():
    global LOG
    args = parse_args()
    if args.log:
        LOG = Logger(filename=args.log)
    config = get_json_from_file(args.result_file)
    success, error_reports = verify_io_success(config)
    assert success, '\n'.join(error_reports)
    LOG.info('IO operations finished successfully')
    if args.log:
        LOG.close()


if __name__ == '__main__':
    main()
