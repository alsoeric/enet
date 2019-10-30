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
    #print(template_dict["event_day"], template_dict["bnt_day"])
    event_key_template = "$event_year $event_month $event_day $time_start"
    #time_template="$time_start - $time_end"
    event_key_expanded = rTemplate.quick_rt(event_key_template,template_dict)
    skip_expanded = rTemplate.quick_rt("$skip",template_dict)
    #print(event_key_expanded, skip_expanded)

    tstruct = time.strptime(event_key_expanded,"%Y %B %d %I:%M %p")
    event_key = time.strftime("%Y-%m-%d-%H", tstruct) + template_dict["gtla"]
    if skip_expanded == "no":
        event_dict[event_key] = template_dict.copy()
    elif skip_expanded == "yes":
        nonevent_dict[event_key] = template_dict.copy()

import sys
import pprint
pd=pprint.PrettyPrinter(indent=4, stream=sys.stderr)
print("""<!DOCTYPE html>
<html lang="en">
<head></head>
<body><p><b>Events This Month</b></p>""")
for k in sorted(event_dict):
    event_list_template='<a href="$group_url" target="_blank">$group_name</a> ($gtla) [$date]<br>'
    event_list=rTemplate.rTemplate(event_list_template,
                                   identifiers=event_dict[k])
    print(event_list.last_pass_cleanup(event_list.substitute()))
    #print("----------------------------", file=sys.stderr)
    #pd.pprint(event_dict)

print("<p></p><p><b>No Events This Month</b></p>")
for k in sorted(nonevent_dict):
    event_list_template='<a href="$group_url" target="_blank">$group_name</a> ($gtla) []<br>'
    event_list=rTemplate.rTemplate(event_list_template,
                                   identifiers=nonevent_dict[k])
    print(event_list.last_pass_cleanup(event_list.substitute()))

for k in sorted(event_dict):
    print("<p></p><p></p>")
    event_final=rTemplate.rTemplate(event_template, identifiers=event_dict[k])
    print(event_final.last_pass_cleanup(event_final.substitute()),)

# footer
print("</body></html>")
