#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#{'section': {'ALARM_MSG': [['Alarmzone 1',
#                            'unbekannt',
#                            'ausgelöst',
#                            '2025-03-06 17:26:19'],
#                           ['WatchDog: crond-restart',
#                            'unbekannt',
#                            'ausgelöst',
#                            '2025-03-06 17:25:37']]}}
                            
                         
                            
from cmk.agent_based.v2 import AgentSection, CheckPlugin, Service, Result, State, Metric, check_levels


#import json
import pprint


def parse_homematic_alarms(string_table):

  # print("Into parse")
  # pprint.pprint(string_table)

  result = { }
  for line in string_table:
    key = line[0]
    device = result.get(key)
    if key == 'ALARM_MSG':
      if device is None:
        device = []
        result[key] = device
      device.append(line[1:])
  return result


def discover_homematic_alarms(section):

  #print("in Discover")
  #pprint.pprint(section)

  yield Service()


def check_homematic_alarms(section):

  #print("Into Check")
  #pprint.pprint(section)

  state = State.OK
  devices = []

  messages = section.get('ALARM_MSG', None);
  
  if messages:
    for msg, t, s, desc, count, last in messages:
       state = State.CRIT
       devices.append("%s: %s, state: %s, (%sx, last: %s)" % (msg, desc, s, count, last))

  if state == State.OK:
    summary = 'No issues reported'
  else:
    summary = ', '.join(devices)

  yield Result(state=state, summary=summary)


agent_section_homematic_alarms = AgentSection(
    name = "homematic_alarms",
    parse_function = parse_homematic_alarms,
)

check_plugin_homematic_alarms = CheckPlugin(
    name = "homematic_alarms",
    service_name = "HomeMatic ALARM Messages",
    discovery_function = discover_homematic_alarms,
    check_function = check_homematic_alarms,
)




