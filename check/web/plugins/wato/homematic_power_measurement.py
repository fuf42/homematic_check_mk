#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.plugins.wato import (
    HostRulespec,
    CheckParameterRulespecWithItem,
    IndividualOrStoredPassword,
    rulespec_registry,
)

from cmk.gui.valuespec import (
    CascadingDropdown,
    Dictionary,
    Integer,
    Float,
    ListOf,
    ListOfStrings,
    RegExp,
    TextAscii,
    Tuple,
)

from cmk.gui.plugins.wato import (
    rulespec_registry,
    HostRulespec,
    SNMPCredentials,
)

checkgroups = []
subgroup_os = _("Temperature, Humidity, Electrical Parameters, etc.")

register_check_parameters(
    subgroup_os,
    "homematic_power_measurement",
    _("Homematic electrical power"),
    Dictionary(
        title = _("Parameters for the Homematic power check"),
        help = _(""),
        elements = [
            ( "warning",
                Tuple(
                title = _("Warning level of power"),
                elements = [
                    Float(title = _("Lower than"), default_value = 0.0),
                    Float(title = _("Higher than"), default_value = 99999.0),
                ],
                ),
            ),
            ( "critical",
                Tuple(
                title = _("Critical level of power"),
                elements = [
                    Float(title = _("Lower than"), default_value = 0.0),
                    Float(title = _("Higher than"), default_value = 99999.0),
                ],
                ),
            ),
        ],
    ),
    TextAscii(
        title = _("Name of the device"),
        ),
    match_type = "dict",
)

