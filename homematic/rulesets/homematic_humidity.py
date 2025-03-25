#!/usr/bin/env python3

from cmk.rulesets.v1 import Label, Title
from cmk.rulesets.v1.form_specs import BooleanChoice, DefaultValue, DictElement, Dictionary, Float, LevelDirection, SimpleLevels
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic, Title



def _parameter_form_humidity():
    return Dictionary(
        title = Title("Parameters for the Homematic humidity check"),
        elements = {
            "levels_lower": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Lower percentage threshold for humidity"),
                    form_spec_template = Float(),
                    level_direction = LevelDirection.LOWER,
                    prefill_fixed_levels = DefaultValue(value=(40.0, 35.0)),
                    # required = True,
                ),
            ),
            "levels_upper": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Upper percentage threshold for humidity"),
                    form_spec_template = Float(),
                    level_direction = LevelDirection.UPPER,
                    prefill_fixed_levels = DefaultValue(value=(60.0, 65.0)),
                ),
            ),
        }
    )

rule_spec_homematic_humidity = CheckParameters(
    name = "homematic_humidity",
    title = Title("Homematic Humidity"),
    topic = Topic.GENERAL,
    parameter_form = _parameter_form_humidity,
    condition = HostAndItemCondition(item_title=Title("homematic_humidity")),
)

