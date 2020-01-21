#!/usr/bin/env python3
import rTemplate
import configparser
import datetime
import time
import pprint
#config_value = configparser.ConfigParser(interpolation=None)
#onfig_value.read_file(open("/var/tmp/network.cfg"))
import glob

import sys

import yaml

events=glob.glob("./*.event")

# with open("event_template.rtmpl") as f:
#    event_template=f.read()

common_dict = rTemplate.colon_parser("event_common", EOL=False)

event_dict = {}
nonevent_dict = {}

# disassemble dict into event specific sections
# if name has prefix strip prefix, move to prefix specific dictionary 

event_prefix=['bnt', 'cnet', 'mdg', 'min', 'sib','snef', 'VF']

for k,i in common_dict.items():
    dict_prefix="common"
    for prefix in event_prefix:
        
        if k.startswith(prefix):
            k=k[len(prefix):]
            dict_prefix=prefix
            break
            
    print(dict_prefix,k)

#with open("./event_common.yaml",'w') as yaml_file:
#    event_yaml = yaml.dump(common_dict)

event_yaml = yaml.dump(common_dict)
#print(event_yaml)