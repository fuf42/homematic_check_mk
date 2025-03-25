#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# [['remote_addon', '{"name":"CCU-Jack","webversion":"2.11.2"}'],
#  ['remote_addon', '{"name":"CUx-Daemon","webversion":"2.12"}'],
#  ['remote_addon', '{"name":"HM-Tools<br>","webversion":"0.7.0"}'],
#  ['remote_addon', '{"name":"Philips Hue","webversion":"3.2.5"}'],
#  ['remote_addon', '{"name":"XML-API","webversion":"2.3"}'],
#  ['local_addon', ' { "name": "CCU-Jack", "webversion": "2.11.2" }'],
#  ['local_addon', ' { "name": "check_mk_agent", "webversion": "1.3" }'],
#  ['local_addon', ' { "name": "CUx-Daemon", "webversion": "2.12" }'],
#  ['local_addon', ' { "name": "HM-Tools<br>", "webversion": "0.7.0" }'],
#  ['local_addon', ' { "name": "Philips Hue", "webversion": "3.2.5" }'],
#  ['local_addon', ' { "name": "XML-API", "webversion": "2.3" }']]


from cmk.agent_based.v2 import AgentSection, CheckPlugin, Service, Result, State, Metric, check_levels

import json
import pprint


def parse_homematic_addons(string_table):

  #  pprint.pprint(string_table)

  parsed = {}
  
  for line in string_table: 

    # pprint.pprint(line)

    t,d = line
    
    k = "remote" if t == "remote_addon" else "local"
    v = json.loads(d)
    # pprint.pprint(v)
    if not v['name'] in parsed:
      parsed[v['name']] = {}
    parsed[v['name']][k] = v["webversion"]

  # pprint.pprint(parsed)
  #
  # {'CCU-Jack': {'local': '2.11.2', 'remote': '2.11.2'},
  # 'CUx-Daemon': {'local': '2.12', 'remote': '2.12'},
  # 'HM-Tools<br>': {'local': '0.7.0', 'remote': '0.7.0'},
  # 'Philips Hue': {'local': '3.2.5', 'remote': '3.2.5'},
  # 'XML-API': {'local': '2.3', 'remote': '2.3'},
  # 'check_mk_agent': {'local': '1.3'}}

  return parsed


def discover_homematic_addons(section):

  # pprint.pprint(section)
  for key, value in section.items():
    yield Service(item = key)


def check_homematic_addons(item, section):
  #pprint.pprint(item)
  #pprint.pprint(section)

  item = section.get(item, None)
  # pprint.pprint(item)
  
  if item:
    local = item.get("local",  None)
    remote = item.get("remote", None)
  
    state = State.OK
    summary = "Version: %s" % local
    if remote:
      if remote != local:
        summary = summary + " (Update available: %s (!))" % remote
        state = State.WARN

    yield Result(state = state, summary = summary)


agent_section_homematic_addons = AgentSection(
  name = "homematic_addons",
  parse_function = parse_homematic_addons,
)

check_plugin_homematic_addons = CheckPlugin(
  name = "homematic_addons",
  service_name = "Homematic Addon %s",
  discovery_function = discover_homematic_addons,
  check_function = check_homematic_addons,
)


