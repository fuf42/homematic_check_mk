#!/usr/bin/env python3

from cmk.rulesets.v1 import Label, Title
from cmk.rulesets.v1.form_specs import BooleanChoice, DefaultValue, DictElement, Dictionary, Float, LevelDirection, SimpleLevels
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic



def _parameter_form_dutycycle():
    return Dictionary(
        elements = {
            "levels_upper": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Upper threshold for dutycycle"),
                    form_spec_template = Float(),
                    level_direction = LevelDirection.UPPER,
                    prefill_fixed_levels = DefaultValue(value=(50.0, 70.0)),
                ),
                required = True,
            ),
        }
    )

rule_spec_homematic_dutycycle = CheckParameters(
    name = "homematic_dutycycle",
    title = Title("Duty Cycle"),
    topic = Topic.GENERAL,
    parameter_form = _parameter_form_dutycycle,
    condition = HostAndItemCondition(item_title=Title("homematic_dutycycle")),
)




