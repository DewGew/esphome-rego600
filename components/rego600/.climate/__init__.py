import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import climate
from esphome.components.sensor import Sensor
from esphome.const import CONF_ID, CONF_SENSOR_ID
from .. import rego_ns, RegoInterfaceComponent, CONF_HUB_ID, CONF_REGO_VARIABLE, CONF_VALUE_FACTOR, not_zero_or_small

DEPENDENCIES = ['rego600']

RegoClimate = rego_ns.class_("RegoClimate", climate.Climate, cg.PollingComponent)

CONFIG_SCHEMA = climate.climate_schema(RegoClimate).extend(
    {
        cv.GenerateID(): cv.declare_id(RegoClimate),
        cv.GenerateID(CONF_HUB_ID): cv.use_id(RegoInterfaceComponent),
        cv.Required(CONF_REGO_VARIABLE): cv.hex_uint16_t,
        cv.Optional(CONF_VALUE_FACTOR, default=1.): cv.All(cv.float_, not_zero_or_small),
        cv.Optional(CONF_SENSOR_ID): cv.use_id(Sensor),
    }
).extend(cv.polling_component_schema('10s'))

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await climate.register_climate(var, config)
    cg.add(var.set_rego_variable(int(config[CONF_REGO_VARIABLE])))
    cg.add(var.set_value_factor(config[CONF_VALUE_FACTOR]))
    if CONF_SENSOR_ID in config:
        indoor_sensor = await cg.get_variable(config[CONF_SENSOR_ID])
        cg.add(var.set_indoor_sensor(indoor_sensor))
    paren = await cg.get_variable(config[CONF_HUB_ID])
    cg.add(var.register_hub(paren))
