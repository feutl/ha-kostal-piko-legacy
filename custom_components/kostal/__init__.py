"""The Kostal PIKO inverter sensor integration."""

import asyncio
import logging
import voluptuous as vol

from datetime import timedelta
from kostalpiko.kostalpiko import Piko

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_HOST,
    CONF_NAME,
    CONF_MONITORED_CONDITIONS,
    EVENT_HOMEASSISTANT_STOP,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import homeassistant.helpers.config_validation as cv

from .const import DEFAULT_NAME, DOMAIN, SENSOR_TYPES, MIN_TIME_BETWEEN_UPDATES

_LOGGER = logging.getLogger(__name__)

__version__ = "1.4.0-alpha.2"
VERSION = __version__

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
                vol.Required(CONF_HOST): cv.string,
                vol.Required(CONF_MONITORED_CONDITIONS): vol.All(
                    cv.ensure_list, [vol.In(list(SENSOR_TYPES))]
                ),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass, config):
    """Set up this integration using yaml."""
    _LOGGER.info("Setup kostal, %s", __version__)
    if DOMAIN not in config:
        return True

    data = dict(config.get(DOMAIN))

    hass.data["yaml_kostal"] = data

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_IMPORT}, data=dict(config[DOMAIN])
        )
    )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Setup KostalPiko component."""

    _LOGGER.info("Starting kostal, %s", __version__)

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    if entry.source == "import":
        if entry.options:  # config.yaml
            data = entry.options.copy()
        else:
            if "yaml_kostal" in hass.data:
                data = hass.data["yaml_kostal"]
            else:
                data = {}
        await hass.config_entries.async_remove(entry.entry_id)
    else:
        data = entry.data.copy()
        data.update(entry.options)

    hass.data[DOMAIN][entry.entry_id] = KostalInstance(hass, entry, data)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    instance = hass.data[DOMAIN][entry.entry_id]
    await instance.stop()
    await instance.clean()
    return True


class KostalDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Kostal Piko data."""

    def __init__(self, hass: HomeAssistant, piko: Piko):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=MIN_TIME_BETWEEN_UPDATES,
        )
        self.piko = piko

    async def _async_update_data(self):
        """Fetch data from Kostal Piko inverter."""
        try:
            # Run blocking update in executor
            _LOGGER.debug("Starting data update for Kostal Piko")
            await self.hass.async_add_executor_job(self.piko.update)
            
            # Check if data attributes exist
            if not hasattr(self.piko, 'data'):
                _LOGGER.error("Piko object has no 'data' attribute after update")
                raise UpdateFailed("Piko object has no 'data' attribute")
            
            if not hasattr(self.piko, 'ba_data'):
                _LOGGER.debug("Piko object has no 'ba_data' attribute (BA sensor may not be installed)")
            
            # Check if data was fetched successfully
            _LOGGER.debug("Data update complete. Data: %s, BA Data: %s", 
                         self.piko.data is not None, 
                         getattr(self.piko, 'ba_data', None) is not None)
            
            # Return both data and ba_data
            result = {
                "data": self.piko.data,
                "ba_data": getattr(self.piko, 'ba_data', None),
            }
            _LOGGER.debug("Returning coordinator data with %d keys", len(result))
            return result
        except Exception as err:
            _LOGGER.error("Error communicating with Kostal Piko: %s", err, exc_info=True)
            raise UpdateFailed(f"Error communicating with Kostal Piko: {err}") from err


class KostalInstance:
    """Config instance of Kostal."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, conf):
        """Initialize KostalInstance."""
        self.hass = hass
        self.config_entry = entry
        self.entry_id = self.config_entry.entry_id
        self.conf = conf
        
        # Create Piko instance (using raw Piko from library, not PikoHolder)
        piko = Piko(conf[CONF_HOST], conf[CONF_USERNAME], conf[CONF_PASSWORD])
        
        # Create coordinator for data updates
        self.coordinator = KostalDataUpdateCoordinator(hass, piko)

        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, self.stop)

        asyncio.create_task(self.start_up())

    async def start_up(self):
        """Start up the Kostal instance."""
        # Perform initial data fetch
        await self.coordinator.async_config_entry_first_refresh()
        self.add_sensors(self.conf[CONF_MONITORED_CONDITIONS])

    async def stop(self, _=None):
        """Stop Kostal."""
        _LOGGER.info("Shutting down Kostal")

    def add_sensors(self, sensors):
        """Add sensors."""
        self.hass.async_create_task(self._asyncadd_sensors(sensors))

    async def _asyncadd_sensors(self, sensors):
        """Add sensors asynchronously."""
        await self.hass.config_entries.async_forward_entry_setups(
            self.config_entry, ["sensor"]
        )
        async_dispatcher_send(self.hass, "kostal_init_sensors", sensors, self.coordinator)

    async def clean(self):
        """Clean up."""
        await self.hass.config_entries.async_unload_platforms(
            self.config_entry, ["sensor"]
        )
