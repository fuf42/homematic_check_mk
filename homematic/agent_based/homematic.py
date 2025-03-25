#!/usr/bin/python
# -*- coding: utf-8 -*-

from cmk.agent_based.v2 import AgentSection, CheckPlugin, Service, Result, State, Metric, check_levels

# import json
import pprint


degree_sign= u'\N{DEGREE SIGN}'



def parse_homematic(string_table):

  #pprint.pprint(string_table)
    
  result = { }
  for item in string_table:
    #pprint.pprint(item)

    key = item[0]
    device = result.get(key)
    if key == 'SVC_MSG':
      if device is None:
        device = []
        result[key] = device
      device.append(item[1:])
    else:
      if device is None:
        device = { }
        result[key] = device
      device[item[1]] = item[2:]

  return result


def discover_homematic(section):
  yield Service(item = 'Low Battery devices')
  yield Service(item = 'Unreachable devices')
  yield Service(item = 'Service Messages')


def check_homematic(item, section):
  messages = section.get('SVC_MSG', None);

  # pprint.pprint(messages)
  
  state = State.OK
  devices = []

  #state = max(state, State.WARN, key=lambda s: s.value) # ChatGPT sagt, das geht so. Geht auch. Aber schön ist es nicht.
  #pprint.pprint(state)

  if messages is not None:
    for msg in messages:
    
      # pprint.pprint(msg)
      
      if item == 'Low Battery devices':
        if msg[1] == 'LOWBAT':
          state = State.CRIT
          devices.append(msg[0])
      elif item == 'Unreachable devices':
        if msg[1] == 'UNREACH':
          state = State.CRIT
          devices.append(msg[0])
        elif msg[1] == 'STICKY_UNREACH':
          state = max(state, State.WARN, key=lambda s: s.value)
          devices.append(msg[0])
      elif item == 'Service Messages':
        if msg[1] not in [ 'LOWBAT', 'UNREACH', 'STICKY_UNREACH' ]:
          if msg[1] in [ 'CONFIG_PENDING', 'DEVICE_IN_BOOTLOADER', 'UPDATE_PENDING', 'USBH_POWERFAIL' ]:
            state = max(state, State.WARN, key=lambda s: s.value)
          else:
            state = State.CRIT
          devices.append(msg[0] + ':' + msg[1])

  if state == State.OK:
    summary = 'No issues reported'
  else:
    summary = ', '.join(devices)

  yield Result( state = state, summary = summary)


agent_section_homematic = AgentSection(
  name = "homematic",
  parse_function = parse_homematic,
)

check_plugin_homematic = CheckPlugin(
  name = "homematic",
  service_name = "Homematic %s",
  discovery_function = discover_homematic,
  check_function = check_homematic,
)

############

def discover_homematic_humidity(section):

  # pprint.pprint(section)
 
  for line in section:
    data = section[line]
    if isinstance(data, dict):
      temperature = data.get('TEMPERATURE', data.get('ACTUAL_TEMPERATURE', None))
      # humidity = data.get('HUMIDITY', None)
      humidity = data.get('HUMIDITY', data.get('ACTUAL_HUMIDITY', None))

      #pprint.pprint(line)
      
      if temperature is not None and humidity is not None:
        yield Service( item = line)


def check_homematic_humidity(item, params, section):

  #pprint.pprint(item)
  #pprint.pprint(params)
  
  for line in section:
    if line == item:
      data = section[line]
      temperature = data.get('TEMPERATURE', data.get('ACTUAL_TEMPERATURE', None))
      # humidity = data.get('HUMIDITY', None)
      humidity = data.get('HUMIDITY', data.get('ACTUAL_HUMIDITY', None))

      if humidity is None or temperature is None:
        return Result(state = State.UNKNOWN, summary='Humidity or temperature are not available')

      date = humidity[1]
      temperature = float(temperature[0])
      humidity = float(humidity[0])

      #if humidity <= params['critical'][0] or humidity >= params['critical'][1]:
      #  state = State.CRIT
      #elif humidity <= params['warning'][0] or humidity >= params['warning'][1]:
      #  state = State.WARN
      #else:
      #  state = State.OK

      # message = "Temperature: %.1f%sC, Humidity: %.0f%% (last change: %s)" % (temperature, degree_sign, humidity, date)

      yield Metric(name = "temperature", value = temperature)
      # yield Metric(name = "humidity", value = humidity)     

      yield from check_levels(
         humidity,
         levels_upper = params['levels_upper'],
         levels_lower = params['levels_lower'],
         metric_name = "humidity",
         render_func=lambda v: "Humidity: %.0f%%" % v,
      )
      
      yield Result(state = State.OK, summary="Temperature: %.1f%sC (last change: %s)" % (temperature, degree_sign, date))



# oldold
#
#factory_settings['homematic_humidity_default_levels'] = {
#    'warning' : (40, 60),
#    'critical': (35, 65),
#}

# old
#
#homematic_humidity_default_levels = { 
#    'warning' : (40, 60),
#    'critical': (35, 65),
#}

# does not give possibility to change limits, really ruleset needed??
#
homematic_humidity_default_levels = { 
    'levels_lower': ("fixed", (40,35)),
    'levels_upper': ("fixed", (60,65))
}

check_plugin_homematic_humidity = CheckPlugin(
  name = "homematic_humidity",
  service_name = "Humidity %s",
  discovery_function = discover_homematic_humidity,
  check_function = check_homematic_humidity,
  check_default_parameters = homematic_humidity_default_levels,
  # check_default_parameters = {},
  check_ruleset_name = "homematic_humidity",
  sections=["homematic"],
)


###

def discover_homematic_dutycycle(section):

  # pprint.pprint(section)
  
  for line in section:
    data = section[line]
    if isinstance(data, dict) and data.get('DUTY_CYCLE', None) is not None:
      yield Service( item = line )


def check_homematic_dutycycle(item, params, section):

  #pprint.pprint(item)
  #pprint.pprint(params)
  #pprint.pprint(section)

  # Parameters({'levels_upper': ('fixed', (10.0, 20.0))})
  # Parameters({'levels_upper': ('no_levels', None)})
  # Parameters({'levels_upper': ('fixed', (50, 70))})

  #levels_upper = params['levels_upper'][1]
  
  # crit = params['critical'] = 70
  # warn = params['warning]'] = 50
  #crit = params['levels_upper'][1][1]
  #warn = params['levels_upper'][1][0]

  for line in section:
    if line == item:
      data = section[line]
      
      # pprint.pprint(data)
      
      dutycycle = data.get('DUTY_CYCLE', None)

      if dutycycle is None:
        yield Result(state = State.UNKNOWN, summary = 'Duty cycle is not available')
        return

#      try:
#        dutycycle= float(dutycycle[0])
#      except ValueError:
#        # HMIP-PSM-2 and others are returning True/False for dutycycle (WTF?)
#        if dutycycle[0].lower() in ("yes", "true", "t", "1"):
#          dutycycle = True
#        else:
#          dutycycle = False
#          
#      if dutycycle is True or dutycycle >= crit:
#        state = state.CRIT
#      elif dutycycle >= warn:
#        state = State.WARN
#      else:
#        state = State.OK
#
#      message = "Duty cycle: %s" % (dutycycle)
#
#      # yield Metric(name = "dutycycle", value = dutycycle, levels = params['levels_upper'] )
#      #perfdata = [
#      #  ('dutycycle', dutycycle, params['warning'], params['critical'], 0, 100),
#      #]
#
#      yield Result(state = state, summary = message)

      # wie umgehen mit DutyCycle == True?
      try:
        dutycycle = float(dutycycle[0])
      except ValueError:
        yield Result( state = State.CRIT, summary = "Duty cycle is True (reached)" )
        return

      yield from check_levels(
         dutycycle,
         levels_upper = params['levels_upper'],
         metric_name = "dutycycle",
         label = "Duty cycle",
         boundaries = (0.0, 100.0),
         # notice_only = True,
         render_func=lambda v: "%.1f" % v,
      )


homematic_dutycycle_default_levels = {
  "levels_upper": ("fixed", (50, 70))
}

check_plugin_homematic_dutycycle = CheckPlugin(
  name = "homematic_dutycycle",
  service_name = "Duty cycle %s",
  discovery_function = discover_homematic_dutycycle,
  check_function = check_homematic_dutycycle,
  check_default_parameters = homematic_dutycycle_default_levels,
  # check_default_parameters = { },
  # check_default_parameters = {"levels_upper": ("fixed", (5, 70)) },
  check_ruleset_name = "homematic_dutycycle",
  sections = ["homematic"],
)

