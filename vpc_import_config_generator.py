import json
import os
from jinja2 import Template
import argparse

template = """import {
  id = "{{vpc_id}}"
  to = aws_vpc.{{vpc_id}}
}

"""

tf_import_blocks = []

def parse_args():
    parser = argparse.ArgumentParser(description='Generate Terraform import configuration from JSON')
    parser.add_argument('json_file', type=str, help='JSON file to parse')
    return parser.parse_args()

args = parse_args()
# print(args.json_file)

with open(args.json_file) as json_file:
    data = json.load(json_file)
    vpc_data = data['Vpcs']
    for vpc in vpc_data:
        t = Template(template)
        tf_import_blocks.append(t.render(vpc_id=vpc["VpcId"]))
    with open('imports-' + args.json_file + '.tf', 'w') as f:
        f.write("\n".join(tf_import_blocks))
    
