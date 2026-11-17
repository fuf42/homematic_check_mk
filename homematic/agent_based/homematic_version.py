#!/usr/bin/python
#
#
#   'UPDATE_MSG': {' 3.65.6.20220723': [' 3.65.11.20221005']},
#
#
#
#  {'section': [('VERSION_INFO',
#              'homematic_version',
#              '3.79.6.20250220',
#              '3.79.6.20250220')]}
#
#


from cmk.agent_based.v2 import AgentSection, CheckPlugin, Service, Result, State, Metric, check_levels

#import json
import pprint


def parse_homematic_version(string_table):

    #print("parse string_table:")
    #pprint.pprint(string_table)

    parsed = []
    for line in string_table:
        if len(line) == 4:
            parsed.append(tuple(line))
    return parsed


def discover_homematic_version(section):

    #print("discover section:")
    #pprint.pprint(section)

    for item in section:

        # ('VERSION_INFO', 'homematic_version', '3.79.6.20250220', '3.79.6.20250220')
        if len(item) == 4:
            yield Service()


def check_homematic_version(section):

    #print("check section:")
    #pprint.pprint(section)
    #pprint.pprint(section[0])
    #pprint.pprint(section[0][0])

    versioninfo, t, local, remote = section[0]
    #print( versioninfo, t, local, remote )

    # the CCU sends an empty value (or "n/a") when its update lookup failed;
    # that is not a version, so we cannot compare and do not raise a WARN
    remote_clean = (remote or "").strip().lower()
    if remote_clean in ("", "n/a", "na", "none", "unknown"):
        yield Result(state=State.OK, summary="Firmware %s (update check unavailable)" % local)
    elif (local or "").strip().lower() != remote_clean:
        yield Result(state=State.WARN, summary="Firmware %s (%s is available (!))" % (local, remote))
    else:
        yield Result(state=State.OK, summary="Firmware %s (up to date)" % local)



agent_section_homematic_version = AgentSection(
    name = "homematic_version",
    parse_function = parse_homematic_version,
)

check_plugin_homematic_version = CheckPlugin(
    name = "homematic_version",
    service_name = "HomeMatic Version",
    discovery_function = discover_homematic_version,
    check_function = check_homematic_version,
)

