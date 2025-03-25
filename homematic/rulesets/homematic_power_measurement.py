#!/usr/bin/env python3

from cmk.rulesets.v1 import Label, Title
from cmk.rulesets.v1.form_specs import BooleanChoice, DefaultValue, DictElement, Dictionary, Float, LevelDirection, SimpleLevels
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic, Title



def _parameter_form_power_measurement():
    return Dictionary(
        title = Title("Parameters for the Homematic power check"),
        elements = {
            "levels_lower": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Lower percentage threshold for power_measurement"),
                    form_spec_template = Float(),
                    level_direction = LevelDirection.LOWER,
                    prefill_fixed_levels = DefaultValue(value=(0, 0)),
                ),
                required = True,
            ),
            "levels_upper": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Upper percentage threshold for power_measurement"),
                    form_spec_template = Float(),
                    level_direction = LevelDirection.UPPER,
                    prefill_fixed_levels = DefaultValue(value=(99999.0, 99999.0)),
                ),
                required = True,
            ),
        }
    )


rule_spec_homematic_power_measurement = CheckParameters(
    name = "homematic_power_measurement",
    title = Title("Homematic electrical power"),
    topic = Topic.GENERAL,
    #topic = _("Temperature, Humidity, Electrical Parameters, etc.")
    parameter_form = _parameter_form_power_measurement,
    condition = HostAndItemCondition(item_title=Title("homematic_power_measurement")),
)

