#!/usr/bin/env python3
import rTemplate
import configparser
import datetime
import time
import pprint
#config_value = configparser.ConfigParser(interpolation=None)
#onfig_value.read_file(open("/var/tmp/network.cfg"))
import glob

pp=pprint.PrettyPrinter(indent=4)

events=glob.glob("./*.event")

with open("event_template.rtmpl") as f:
    event_template=f.read()

common_dict = rTemplate.colon_parser("event_common", EOL=False)

event_dict = {}
nonevent_dict = {}

for event_filename in events:
    template_dict = rTemplate.colon_parser(event_filename, starter_dict=common_dict, EOL=False)
    #print(template_dict["gtla"])
    tstruct = time.strptime(template_dict["date"],"%Y %B %d")
    event_key = time.strftime("%Y-%m-%d", tstruct) + template_dict["gtla"]
    if template_dict["skip"] == "no":
        event_dict[event_key] = template_dict.copy()
    elif template_dict["skip"] == "yes":
        nonevent_dict[event_key] = template_dict.copy()

import sys
import pprint
pd=pprint.PrettyPrinter(indent=4, stream=sys.stderr)
print("<b>Events This Month</b><br>")
for k in sorted(event_dict):
    event_list_template="<a href=$group_url>$group_name ($gtla)</a> [$date]<br>"
    event_list=rTemplate.rTemplate(event_list_template,
                                   identifiers=event_dict[k])
    print(event_list.last_pass_cleanup(event_list.substitute()))
    #print("----------------------------", file=sys.stderr)
    #pd.pprint(event_dict)

print("<br><br><b>No Events This Month</b><br>")
for k in sorted(nonevent_dict):
    event_list_template="<a href=$group_url>$group_name ($gtla)</a> []<br>"
    event_list=rTemplate.rTemplate(event_list_template,
                                   identifiers=nonevent_dict[k])
    print(event_list.last_pass_cleanup(event_list.substitute()))

for k in sorted(event_dict):
    event_final=rTemplate.rTemplate(event_template, identifiers=event_dict[k])
    print("<br><br><br>")
    print(event_final.last_pass_cleanup(event_final.substitute()),)

# footer
