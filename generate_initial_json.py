'''

GENERATE_INITIAL_JSON SCRIPT
Generates file with initial JSON config

'''

import json
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('result_file', help='full path to a file with JSON wich must be created')
    parser.add_argument('--bs', help='block size of IO operations')
    parser.add_argument('--size', help='size of devices and IO operations')
    parser.add_argument('--dev_count', help='number of devices of each type [fileio, file, alloc]')
    return parser.parse_args()


def main():

    args = parse_args()
    bs = int(args.bs) if args.bs else 4096
    size = int(args.size) if args.size else bs*10
    dev_count = int(args.dev_count) if args.dev_count else 4

    config = {
        'target': {
            'name': 'tgt1'
        },
        'initiator': {
            'name': 'init1'
        },
        'devices': [],
        'io': []
    }

    for i in range(1, dev_count+1):
        for dev_type in ['fileio', 'file', 'alloc']:
            config['devices'].append({
                'name': dev_type + str(i),
                'type': dev_type,
                'size': str(size),
                })
            config['io'].append({
                'initiator': 'init1',
                'device': dev_type + str(i),
                'size': str(size),
                'bs': str(bs)
                })

    open(args.result_file, 'w').write(json.dumps(config, indent=4))


if __name__ == '__main__':
    main()
