#!/usr/bin/env python

import os
import sys
import argparse
import json

masters = []
workers = []

try:
    import json
except ImportError:
    import simplejson as json

class ExampleInventory(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        # Called with `--list`.
        if self.args.list:
            self.inventory = self.example_inventory()
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return empty inventory.
        else:
            self.inventory = self.empty_inventory()

        print json.dumps(self.inventory);

    # Example inventory for testing.
    def example_inventory(self):
        return {
            'masters': {
                'hosts': [','.join(map(str, masters))],
                },
            'workers': {
                'hosts': [','.join(map(str, workers))],
                }
            }
    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        parser.add_argument('--host', action = 'store')
        self.args = parser.parse_args()

with open('terraform.tfstate') as f:
    data = json.load(f)

resources = data["modules"][0]["resources"]

for resource in resources:
    resource_type = resources[resource]["type"]
    if resource_type == 'aws_instance':
        swarm_type = resources[resource]["primary"]["attributes"]["tags.swarm_type"]
        public_ip = resources[resource]["primary"]["attributes"]["public_ip"]
        if  swarm_type == "master":
            masters.append(public_ip)
        elif swarm_type == "worker":
            workers.append(public_ip)



# Get the inventory.
ExampleInventory()
