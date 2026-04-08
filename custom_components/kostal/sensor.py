"""Support for Kostal PIKO Photvoltaic (PV) inverter."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
)

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

from .const import SENSOR_TYPES, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the sensor dynamically."""
    _LOGGER.info("Setting up kostal piko sensor")

    async def async_add_sensors(sensors, coordinator):
        """Add sensors with coordinator."""
        # Get inverter info for device setup
        info = await hass.async_add_executor_job(coordinator.piko._get_info)
        _sensors = []
        for sensor in sensors:
            _sensors.append(PikoSensor(coordinator, sensor, info, entry.title))

        async_add_entities(_sensors)

    async_dispatcher_connect(hass, "kostal_init_sensors", async_add_sensors)


class PikoSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Piko inverter value."""

    def __init__(self, coordinator, sensor_type, info=None, name=None):
        """Initialize the sensor."""
        super().__init__(coordinator)
        _LOGGER.debug("Initializing PikoSensor: %s", sensor_type)
        self._sensor = SENSOR_TYPES[sensor_type][0]
        self._name = name
        self.type = sensor_type
        self._unit_of_measurement = SENSOR_TYPES[self.type][1]
        self._icon = SENSOR_TYPES[self.type][2]
        self.serial_number = info[0] if info else None
        self.model = info[1] if info else None

        if self._unit_of_measurement == UnitOfEnergy.KILO_WATT_HOUR:
            self._attr_device_class = SensorDeviceClass.ENERGY
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        elif self._unit_of_measurement in (
            UnitOfElectricCurrent.AMPERE,
            UnitOfElectricPotential.VOLT,
            UnitOfPower.WATT,
        ):
            self._attr_state_class = SensorStateClass.MEASUREMENT

            if self._unit_of_measurement == UnitOfElectricCurrent.AMPERE:
                self._attr_device_class = SensorDeviceClass.CURRENT
            elif self._unit_of_measurement == UnitOfElectricPotential.VOLT:
                self._attr_device_class = SensorDeviceClass.VOLTAGE
            elif self._unit_of_measurement == UnitOfPower.WATT:
                self._attr_device_class = SensorDeviceClass.POWER

    @property
    def name(self):
        """Return the name of the sensor."""
        return "{} {}".format(self._name, self._sensor)

    @property
    def state(self):
        """Return the state of the device."""
        if not self.coordinator.data:
            return None
            
        data = self.coordinator.data.get("data")
        ba_data = self.coordinator.data.get("ba_data")
        
        if data is not None:
            if self.type == "current_power":
                return data.get_current_power()
            elif self.type == "total_energy":
                return data.get_total_energy()
            elif self.type == "daily_energy":
                return data.get_daily_energy()
            elif self.type == "string1_voltage":
                return data.get_string1_voltage()
            elif self.type == "string1_current":
                return data.get_string1_current()
            elif self.type == "string2_voltage":
                return data.get_string2_voltage()
            elif self.type == "string2_current":
                return data.get_string2_current()
            elif self.type == "string3_voltage":
                return data.get_string3_voltage()
            elif self.type == "string3_current":
                return data.get_string3_current()
            elif self.type == "l1_voltage":
                return data.get_l1_voltage()
            elif self.type == "l1_power":
                return data.get_l1_power()
            elif self.type == "l2_voltage":
                return data.get_l2_voltage()
            elif self.type == "l2_power":
                return data.get_l2_power()
            elif self.type == "l3_voltage":
                return data.get_l3_voltage()
            elif self.type == "l3_power":
                return data.get_l3_power()
            elif self.type == "status":
                return data.get_piko_status()

        if ba_data is not None:
            if self.type == "solar_generator_power":
                return ba_data.get_solar_generator_power() or "No BA sensor installed"
            elif self.type == "consumption_phase_1":
                return ba_data.get_consumption_phase_1() or "No BA sensor installed"
            elif self.type == "consumption_phase_2":
                return ba_data.get_consumption_phase_2() or "No BA sensor installed"
            elif self.type == "consumption_phase_3":
                return ba_data.get_consumption_phase_3() or "No BA sensor installed"
        
        return None

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement this sensor expresses itself in."""
        return self._unit_of_measurement

    @property
    def icon(self):
        """Return icon."""
        return self._icon

    @property
    def unique_id(self):
        """Return unique id based on device serial and variable."""
        return "{} {}".format(self.serial_number, self._sensor)

    @property
    def device_info(self):
        """Return information about the device."""
        return {
            "identifiers": {(DOMAIN, self.serial_number)},
            "name": self._name,
            "manufacturer": "Kostal",
            "model": self.model,
        }
