import json
import datetime
import sys
import argparse
from jsonschema import validate

# -- Scheme for JSON validation

schema = {
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


# -- Overriden --show_scheme flag action (acts like help, not requirin config)

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
        print(json.dumps(schema, indent=4))
        parser.exit()


# -- Arguments parsing

parser = argparse.ArgumentParser()
parser.add_argument('config', help='path to a config file with JSON object')
parser.add_argument('--nosave', action='store_true', help='discard saving config to standard files')
parser.add_argument('--print', action='store_true', help='print config')
parser.add_argument('--workdir', help='location for new configs')
parser.add_argument('--show_scheme', action=_SchemeAction, help='show correct build scheme for a config')
args = parser.parse_args()

# -- Reading and validating initial JSON

json_file = open(args.config)
json_data = json.load(json_file)
validate(json_data, schema)

tgt_json = json_data["target"]
init_json = json_data["initiators"]
dev_json = json_data["devices"]
io_json = json_data["io"]

# -- Internal config generation

idx = 0
for dev in dev_json:
    dev['lun'] = 'lun' + str(idx)
    idx = idx + 1

now = datetime.datetime.now()
tgt_json['iqn'] = "iqn." + now.strftime('%Y-%m') + ".com.lio-project:tgt-" + tgt_json['name']

tgt_json['devices'] = dev_json
tgt_json['acl'] = []

for init in init_json:
    init['target_iqn'] = tgt_json['iqn']
    init['iqn'] = "iqn." + now.strftime('%Y-%m') + ".com.lio-project:init-" + init['name']
    tgt_json['acl'].append(init['iqn'])
    init['devices'] = dev_json
    init['io'] = [io for io in io_json if io['initiator'] == init['name']]

wdir = ""
if args.workdir:
    wdir = args.workdir + "/"

if not args.nosave:
    init_file = open(wdir + 'init_config.json', 'w')
    init_file.write(json.dumps(init_json, indent=4))
    init_file.close()

    tgt_file = open(wdir + 'tgt_config.json', 'w')
    tgt_file.write(json.dumps(tgt_json, indent=4))
    tgt_file.close()

if args.print:
    print(json.dumps(tgt_json, indent=4))
    print(json.dumps(init_json, indent=4))
