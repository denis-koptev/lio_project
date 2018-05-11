'''

GET_TYPE_AVERAGE SCRIPT
Reads file with IO result in JSON format and counts average speed for each device type

'''

import os
import sys
import json
import argparse
from logger import Logger


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


def get_average_results(io_res_array):
    avg_dict = {}
    for io_res in io_res_array:
        if io_res['success'] != 1:
            continue
        key = io_res['dev_type']
        if key in avg_dict:
            avg_dict[key]['speed'] += float(io_res['speed'])
            avg_dict[key]['records'] += 1
        else:
            avg_dict[key] = {
                'speed': float(io_res['speed']),
                'records': 1
            }
    for key in avg_dict:
        avg_dict[key]['speed'] = float(avg_dict[key]['speed']) / int(avg_dict[key]['records'])
    return avg_dict

def main():
    global LOG
    args = parse_args()
    if args.log:
        LOG = Logger(filename=args.log)
    config = get_json_from_file(args.result_file)
    avg_dict = get_average_results(config)
    LOG.info('Average result: \n{}'.format(json.dumps(avg_dict, indent=4)))
    if args.log:
        LOG.close()


if __name__ == '__main__':
    main()
