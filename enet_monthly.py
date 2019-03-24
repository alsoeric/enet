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
    else:
        nonevent_dict[event_key] = template_dict.copy()
    #k = event_key
    # print(k)
    # print(event_dict[k]["group_name"])
    # print(event_dict[k]["gtla"])
    # print(event_dict[k]["date"])
    # print()
    # print("{} ({}) [{}]".format(event_dict[k]["group_name"],
    #                             event_dict[k]["gtla"],
    #                             event_dict[k]["date"] ))
    #
    #print(event_dict[event_key]["gtla"])

    #print(k)
    #pp.pprint(event_dict[k])

print("<b>Events This Month</b><br>")
for k in sorted(event_dict):
    print("<a href={}>{} ({})</a> [{}]<br>".format(event_dict[k]["group_url"],
        event_dict[k]["group_name"],
        event_dict[k]["gtla"],
        event_dict[k]["date"] ))

print("<br><br><b>No Events This Month</b><br>")
for k in sorted(nonevent_dict):
    print("<a href={}>{} ({})</a> [{}]<br>".format(nonevent_dict[k]["group_url"],
        nonevent_dict[k]["group_name"],
        nonevent_dict[k]["gtla"],
        "" ))

for k in sorted(event_dict):
    event_final=rTemplate.rTemplate(event_template, identifiers=event_dict[k])
    print("<br><br><br>")
    print(event_final.last_pass_cleanup(event_final.substitute()),)
