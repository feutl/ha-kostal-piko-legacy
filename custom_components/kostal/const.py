"""Constants for the Kostal piko integration."""
from datetime import timedelta

from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
)

DOMAIN = "kostal"

DEFAULT_NAME = "Kostal Piko"

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)

SENSOR_TYPES = {
    "solar_generator_power": ["Solar generator power", UnitOfPower.WATT, "mdi:solar-power"],
    "consumption_phase_1": ["Consumption phase 1", UnitOfPower.WATT, "mdi:power-socket-eu"],
    "consumption_phase_2": ["Consumption phase 2", UnitOfPower.WATT, "mdi:power-socket-eu"],
    "consumption_phase_3": ["Consumption phase 3", UnitOfPower.WATT, "mdi:power-socket-eu"],
    "current_power": ["Current power", UnitOfPower.WATT, "mdi:solar-power"],
    "total_energy": ["Total energy", UnitOfEnergy.KILO_WATT_HOUR, "mdi:solar-power"],
    "daily_energy": ["Daily energy", UnitOfEnergy.KILO_WATT_HOUR, "mdi:solar-power"],
    "string1_voltage": ["String 1 voltage", UnitOfElectricPotential.VOLT, "mdi:current-ac"],
    "string1_current": ["String 1 current", UnitOfElectricCurrent.AMPERE, "mdi:flash"],
    "string2_voltage": ["String 2 voltage", UnitOfElectricPotential.VOLT, "mdi:current-ac"],
    "string2_current": ["String 2 current", UnitOfElectricCurrent.AMPERE, "mdi:flash"],
    "string3_voltage": ["String 3 voltage", UnitOfElectricPotential.VOLT, "mdi:current-ac"],
    "string3_current": ["String 3 current", UnitOfElectricCurrent.AMPERE, "mdi:flash"],
    "l1_voltage": ["L1 voltage", UnitOfElectricPotential.VOLT, "mdi:current-ac"],
    "l1_power": ["L1 power", UnitOfPower.WATT, "mdi:power-plug"],
    "l2_voltage": ["L2 voltage", UnitOfElectricPotential.VOLT, "mdi:current-ac"],
    "l2_power": ["L2 power", UnitOfPower.WATT, "mdi:power-plug"],
    "l3_voltage": ["L3 voltage", UnitOfElectricPotential.VOLT, "mdi:current-ac"],
    "l3_power": ["L3 power", UnitOfPower.WATT, "mdi:power-plug"],
    "status": ["Status", None, "mdi:solar-power"],
}
