'''

PARSE_JSON
Validates initial JSON configuration
Appends configuration with generated additional parameters

'''

import os
import json
import datetime
import sys
import argparse
from jsonschema import validate

# -- Scheme for JSON validation

SCHEME = {
    "type": "object",
    "properties": {
        "target": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
            },
            "required": ["name"]
        },
        "devices": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "type": {"type": "string"},
                    "size": {"type": "string"}
                },
                "required": ["name", "type", "size"]
            },
        },
        "initiators": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                },
                "required": ["name"]
            },
        },
    },
    "required": ["target", "devices", "initiators"]
}


# Overriden class for --show_scheme flag action (acts like help, not requirin config)

class _SchemeAction(argparse.Action):
    def __init__(self,
                 option_strings,
                 dest=argparse.SUPPRESS,
                 default=argparse.SUPPRESS,
                 help=None):
        super(_SchemeAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        print(json.dumps(SCHEME, indent=4))
        parser.exit()


# -- Arguments parsing

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='path to a config file with JSON object')
    parser.add_argument('--nosave', action='store_true', help='discard saving config to standard files')
    parser.add_argument('--print', action='store_true', help='print config')
    parser.add_argument('--workdir', help='location for new configs')
    parser.add_argument('--show_scheme', action=_SchemeAction, help='show correct build scheme for a config')
    return parser.parse_args()


def get_json_from_file(path):
    if not os.path.isfile(path):
        print('[ERROR] JSON config path is invalid. Exiting...')
        sys.exit(1)
    json_file = open(path)
    json_data = json.load(json_file)
    json_file.close()
    return json_data


def validate_json(json_data):
    validate(json_data, SCHEME)


def generate_target_iqn(tgt_name):
    now = datetime.datetime.now()
    return "iqn." + now.strftime('%Y-%m') + ".com.lio-project:tgt-" + tgt_name


def generate_initiator_iqn(init_name):
    now = datetime.datetime.now()
    return "iqn." + now.strftime('%Y-%m') + ".com.lio-project:init-" + init_name


def get_internal_jsons(tgt_json, inits_json, devs_json, io_json):
    idx = 0
    for dev in devs_json:
        dev['lun'] = 'lun_' + str(idx)
        idx = idx + 1

    tgt_json['iqn'] = generate_target_iqn(tgt_json['name'])
    tgt_json['devices'] = devs_json
    tgt_json['acl'] = []

    for init in inits_json:
        init['target_iqn'] = tgt_json['iqn']
        init['iqn'] = generate_initiator_iqn(init['name'])
        init['devices'] = devs_json
        init['io'] = [io for io in io_json if io['initiator'] == init['name']]
        tgt_json['acl'].append(init['iqn'])

    return {
        'tgt_json': tgt_json,
        'inits_json': inits_json,
        'devs_json': devs_json
    }


def main():
    args = parse_args()
    json_data = get_json_from_file(args.config)

    validate_json(json_data)

    tgt_json = json_data["target"]
    init_json = json_data["initiators"]
    dev_json = json_data["devices"]
    io_json = json_data["io"]

    # -- Internal config generation
    internal_jsons = get_internal_jsons(tgt_json, init_json, dev_json, io_json)

    wdir = ""
    if args.workdir:
        wdir = args.workdir + "/"

    if not args.nosave:
        for init in internal_jsons['inits_json']:
            init_file = open(wdir + 'initconf_' + init['name'] + '.json', 'w')
            init_file.write(json.dumps(init, indent=4))
            init_file.close()

        tgt_file = open(wdir + 'tgt_config.json', 'w')
        tgt_file.write(json.dumps(internal_jsons['tgt_json'], indent=4))
        tgt_file.close()

        dev_file = open(wdir + 'dev_config.json', 'w')
        dev_file.write(json.dumps(internal_jsons['devs_json'], indent=4))
        dev_file.close()

    if args.print:
        print(json.dumps(internal_jsons['tgt_json'], indent=4))
        print(json.dumps(internal_jsons['inits_json'], indent=4))
        print(json.dumps(internal_jsons['devs_json'], indent=4))


if __name__ == '__main__':
    main()
