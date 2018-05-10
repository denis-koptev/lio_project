import os
import sys
import json
import argparse
from logger import Logger

# VERIFY_IO SCRIPT
# Reads file with IO result in JSON format and verifies success


log = Logger()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('result_file', help='path to a file with IO result in JSON format')
    parser.add_argument('--log', help='path where log file will be created')
    return parser.parse_args()


def get_json_from_file(path):
    if not os.path.isfile(path):
        log.error('JSON config with IO results not found')
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
        if io_res['success'] != 1:
            report = 'IO to {} failed with message: {}'.format(io_res['dev_name'], io_res['message'])
            error_reports.append(report)
            log.error(report)
            success = False
    return success, error_reports


def main():
    global log
    args = parse_args()
    if args.log:
        log = Logger(filename=args.log)
    config = get_json_from_file(args.result_file)
    success, error_reports = verify_io_success(config)
    assert success, '\n'.join(error_reports)
    log.info('IO operations finished successfully')


if __name__ == '__main__':
    main()

