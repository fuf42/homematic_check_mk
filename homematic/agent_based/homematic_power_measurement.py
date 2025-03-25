#!/usr/bin/python
# -*- coding: utf-8 -*-

# Trockner (HM-ES-PMSw1-Pl KEQ0965227:2);ENERGY_COUNTER;28465.199982;2019-04-07 22:49:28
# Trockner (HM-ES-PMSw1-Pl KEQ0965227:2);POWER;0.200000;2019-04-07 22:49:28
# Trockner (HM-ES-PMSw1-Pl KEQ0965227:2);CURRENT;21.000000;2019-04-07 22:49:28
# Trockner (HM-ES-PMSw1-Pl KEQ0965227:2);VOLTAGE;231.100000;2019-04-07 22:49:28
# Trockner (HM-ES-PMSw1-Pl KEQ0965227:2);FREQUENCY;49.990000;2019-04-07 22:49:28

# CURRENT = Strom-(stärke) (Ampere)
# POWER = Leistung (Watt)

#

from cmk.agent_based.v2 import AgentSection, CheckPlugin, Service, Result, State, Metric, check_levels

# import json
import pprint



def discover_homematic_power_measurement(section):

  pprint.pprint(section)
  
  for line in section:
    data = section[line]
    if isinstance(data, dict):
      current = data.get('CURRENT', None)
      power = data.get('POWER', None)
      #voltage =  data.get('VOLTAGE', None)
      #frequency = data.get('FREQUENCY', None)
      #energy_counter = data.get('ENERGY_COUNTER', None)
      hsstype = data.get('HSSTYPE', None)

      if power is not None:
        yield Service(item = line)


def check_homematic_power_measurement(item, params, section):

  # pprint.pprint(params)
  
  for line in section:
    if line == item:
      data = section[line]

      # if data.get('HSSTYPE') == 'HM-ES-PMSw1-Pl':
      current = data.get('CURRENT', [0,None])
      power = data.get('POWER', None)
      voltage =  data.get('VOLTAGE', None)
      frequency = data.get('FREQUENCY', None)
      energy_counter = data.get('ENERGY_COUNTER', None)

      if power is None:
        return 3, 'Power is not available'

      date = power[1]
      power = float(power[0])
      current = float(current[0])/1000 # (mA)
      voltage = float(voltage[0])
      frequency = float(frequency[0])
      energy_counter = float(energy_counter[0])

      yield Metric( name = "current", value = current )
      yield Metric( name = "voltage", value = voltage )
      yield Metric( name = "frequency", value = frequency )
      yield Metric( name = "energy_counter", value = energy_counter )
      
      yield from check_levels(
         power,
         levels_upper = params['levels_upper'],
         levels_lower = params['levels_lower'],
         metric_name = "power",
         render_func=lambda v: "Power: %.1fW)" % v,
      )
      yield Result( state = State.OK, summary = "Current: %.1fA (last change: %s)" % (current, date) )


#homematic_power_measurement_default_levels = { }

check_plugin_homematic_power_measurement = CheckPlugin(
  name = "homematic_power_measurement",
  service_name = "Power %s",
  discovery_function = discover_homematic_power_measurement,
  check_function = check_homematic_power_measurement,
  check_default_parameters = {
    "levels_lower": ('no_levels', None),
    "levels_upper": ('no_levels', None)
  },
  sections = ["homematic"],
  check_ruleset_name = "homematic_power_measurement",
)

