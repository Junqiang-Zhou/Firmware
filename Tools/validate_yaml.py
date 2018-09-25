#! /usr/bin/env python
""" Script to validate YAML file(s) against a YAML schema file """

from __future__ import print_function

import argparse
import os
import sys

try:
    import yaml
except:
    print("Failed to import yaml.")
    print("You may need to install it with 'sudo pip install pyyaml'")
    print("")
    raise

try:
    import cerberus
except:
    print("Failed to import cerberus.")
    print("You may need to install it with 'sudo pip install cerberus'")
    print("")
    raise


parser = argparse.ArgumentParser(description='Validate YAML file(s) against a schema')

parser.add_argument('yaml_file', nargs='+', help='YAML config file(s)')
parser.add_argument('--schema-file', type=str, action='store',
                    help='YAML schema file', required=True)
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                    help='Verbose Output')

args = parser.parse_args()
schema_file = args.schema_file
yaml_files = args.yaml_file
verbose = args.verbose

def load_yaml_file(file_name):
    with open(file_name, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            raise

# load the schema
schema = load_yaml_file(schema_file)
validator = cerberus.Validator(schema)

# validate yaml files
for yaml_file in yaml_files:
    if verbose: print("Validating {:}".format(yaml_file))
    document = load_yaml_file(yaml_file)
    # ignore top-level entries prefixed with __
    for key in document.keys():
        if key.startswith('__'): del document[key]

    if not validator.validate(document):
        print("Validation Errors:")
        print(validator.errors)
        print("")
        raise Exception("Validation of {:} failed".format(yaml_file))
