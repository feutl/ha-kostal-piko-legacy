# Kostal Piko Legacy - Improvement Plan

This document outlines planned improvements for the Kostal Piko Legacy integration. Each item can be tackled independently and tested before moving to the next.

---

## Priority 1: Remove Deprecated Code

### 1.1 Remove CONNECTION_CLASS in config_flow.py
**File:** `custom_components/kostal/config_flow.py`  
**Line:** ~49  
**Current:**
```python
CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL
```
**Action:** Delete this line entirely. It's deprecated and no longer used by Home Assistant.  
**Testing:** Verify config flow still works when adding the integration through UI.

---

### 1.2 Replace hass.loop.create_task() in __init__.py
**File:** `custom_components/kostal/__init__.py`  
**Line:** ~112  
**Current:**
```python
hass.loop.create_task(self.start_up())
```
**Change to:**
```python
import asyncio
...
asyncio.create_task(self.start_up())
```
**Why:** `hass.loop` is deprecated. Use standard asyncio instead.  
**Testing:** Restart HA and verify integration loads correctly. Check logs for errors.

---

### 1.3 Replace hass.add_job() in __init__.py
**File:** `custom_components/kostal/__init__.py`  
**Line:** ~125  
**Current:**
```python
self.hass.add_job(self._asyncadd_sensors(sensors, piko))
```
**Change to:**
```python
self.hass.async_create_task(self._asyncadd_sensors(sensors, piko))
```
**Why:** `hass.add_job()` is deprecated.  
**Testing:** Verify all sensors are created and appear in HA after integration setup.

---

### 1.4 Remove @Throttle Decorator
**File:** `custom_components/kostal/sensor.py`  
**Line:** ~126  
**Current:**
```python
from homeassistant.util import Throttle
...
@Throttle(MIN_TIME_BETWEEN_UPDATES)
async def async_update(self):
```
**Action:** Remove the decorator but keep throttling logic in `piko_holder.py` for now. Long-term: implement DataUpdateCoordinator (see Priority 2).  
**Note:** The throttling is already handled in `piko_holder.py`, so removing this decorator shouldn't break functionality.  
**Testing:** Verify sensors still update every 30 seconds, not more frequently.

---

## Priority 2: Add Proper Error Handling

### 2.1 Add Exception Handling in sensor.py
**File:** `custom_components/kostal/sensor.py`  
**Function:** `_update()` (line ~131)  
**Action:** Wrap data fetching in try-except block:
```python
def _update(self):
    """Update data."""
    try:
        self.piko.update()
        data = self.piko.data
        ba_data = self.piko.ba_data
        
        if data is not None:
            # ... existing code ...
            
        if ba_data is not None:
            # ... existing code ...
            
        self._attr_available = True
    except Exception as e:
        _LOGGER.error("Error updating sensor %s: %s", self.type, e)
        self._attr_available = False
```
**Testing:** 
- Unplug network cable or turn off inverter
- Verify sensors show as "unavailable" in HA
- Reconnect and verify sensors come back online

---

### 2.2 Add _attr_available Property
**File:** `custom_components/kostal/sensor.py`  
**Class:** `PikoSensor`  
**Action:** Initialize in `__init__()`:
```python
self._attr_available = True
```
**Why:** Allows sensors to show as unavailable when inverter is offline.  
**Testing:** See 2.1 testing steps.

---

### 2.3 Improve Config Flow Error Handling
**File:** `custom_components/kostal/config_flow.py`  
**Function:** `_check_host()` (line ~62)  
**Current:** Only catches `ConnectTimeout` and `HTTPError`  
**Action:** Add broader exception handling:
```python
def _check_host(self, host, username, password) -> bool:
    """Check if we can connect to the kostal inverter."""
    try:
        piko = Piko(host, username, password)
        response = piko._get_info()
        return True
    except (ConnectTimeout, HTTPError) as e:
        _LOGGER.error("Connection error: %s", e)
        self._errors[CONF_HOST] = "could_not_connect"
        return False
    except Exception as e:
        _LOGGER.error("Unexpected error: %s", e)
        self._errors[CONF_HOST] = "unknown_error"
        return False
```
**Testing:** Try various connection scenarios (wrong IP, wrong password, invalid URL).

---

## Priority 3: Clean Up Unused Code

### 3.1 Remove Unused Exception Classes
**File:** `custom_components/kostal/config_flow.py`  
**Lines:** ~145-150  
**Action:** Delete these classes as they're never used:
```python
class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""

class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""
```
**Testing:** Verify config flow still works normally.

---

### 3.2 Remove Unused Import
**File:** `custom_components/kostal/sensor.py`  
**Line:** ~11  
**Current:**
```python
from homeassistant.helpers.entity import Entity
```
**Action:** Delete this import line.  
**Testing:** Verify no errors when reloading integration.

---

### 3.3 Remove or Implement clean() Method
**File:** `custom_components/kostal/__init__.py`  
**Line:** ~133  
**Option A (Simple):** Delete the empty method entirely.  
**Option B (Better):** Implement cleanup:
```python
async def clean(self):
    """Clean up."""
    await self.hass.config_entries.async_unload_platforms(
        self.config_entry, ["sensor"]
    )
```
**Testing:** Add/remove integration and verify no resource leaks or errors.

---

## Priority 4: Implement DataUpdateCoordinator (Advanced)

**Complexity:** High - involves significant refactoring  
**Impact:** High - better architecture, easier maintenance

### 4.1 Create Coordinator Class
**File:** Create new file `custom_components/kostal/coordinator.py`  
**Action:** Implement a coordinator to manage data updates:
```python
"""DataUpdateCoordinator for Kostal Piko."""
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .piko_holder import PikoHolder

_LOGGER = logging.getLogger(__name__)

class KostalDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Kostal Piko data."""

    def __init__(self, hass: HomeAssistant, piko: PikoHolder):
        """Initialize."""
        self.piko = piko
        
        super().__init__(
            hass,
            _LOGGER,
            name="Kostal Piko",
            update_interval=timedelta(seconds=30),
        )

    async def _async_update_data(self):
        """Fetch data from Kostal Piko."""
        try:
            await self.hass.async_add_executor_job(self.piko.update)
            return {
                "data": self.piko.data,
                "ba_data": self.piko.ba_data,
            }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with inverter: {err}")
```

### 4.2 Update __init__.py to Use Coordinator
**File:** `custom_components/kostal/__init__.py`  
**Action:** Refactor `KostalInstance` to create and use coordinator.

### 4.3 Update sensor.py to Use Coordinator
**File:** `custom_components/kostal/sensor.py`  
**Action:** 
- Remove `@Throttle` decorator
- Remove manual update logic
- Use coordinator data instead
- Inherit from `CoordinatorEntity`

**Testing:**
- Verify all sensors still update every 30 seconds
- Check that when inverter is offline, all sensors become unavailable together
- Verify logs show proper error messages

---

## Priority 5: Add Options Flow

**Complexity:** Medium  
**Impact:** High - better user experience

### 5.1 Add async_step_init in config_flow.py
**File:** `custom_components/kostal/config_flow.py`  
**Action:** Add this method to `KostalConfigFlow` class:
```python
@staticmethod
@callback
def async_get_options_flow(config_entry):
    """Get the options flow."""
    return KostalOptionsFlowHandler(config_entry)
```

### 5.2 Create Options Flow Handler
**File:** `custom_components/kostal/config_flow.py`  
**Action:** Add new class at the end of file:
```python
class KostalOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_MONITORED_CONDITIONS,
                        default=self.config_entry.options.get(
                            CONF_MONITORED_CONDITIONS,
                            self.config_entry.data.get(CONF_MONITORED_CONDITIONS, []),
                        ),
                    ): cv.multi_select(SUPPORTED_SENSOR_TYPES),
                }
            ),
        )
```

**Testing:**
- Go to Settings → Devices & Services → Kostal Piko
- Click "Configure"
- Change monitored conditions
- Verify sensors are added/removed accordingly

---

## Priority 6: Improve Data Handling

### 6.1 Replace if-elif Chain with Dictionary Mapping
**File:** `custom_components/kostal/sensor.py`  
**Function:** `_update()` (line ~131)  
**Action:** Create mapping at class level:
```python
# Add to PikoSensor class __init__ or as class variable
SENSOR_METHODS = {
    "current_power": lambda d: d.get_current_power(),
    "total_energy": lambda d: d.get_total_energy(),
    "daily_energy": lambda d: d.get_daily_energy(),
    "string1_voltage": lambda d: d.get_string1_voltage(),
    "string1_current": lambda d: d.get_string1_current(),
    # ... add all others
}

BA_SENSOR_METHODS = {
    "solar_generator_power": lambda d: d.get_solar_generator_power(),
    "consumption_phase_1": lambda d: d.get_consumption_phase_1(),
    # ... add all BA sensors
}
```

Then replace the if-elif chain:
```python
def _update(self):
    """Update data."""
    self.piko.update()
    data = self.piko.data
    ba_data = self.piko.ba_data

    if data is not None and self.type in self.SENSOR_METHODS:
        self._state = self.SENSOR_METHODS[self.type](data)
    
    if ba_data is not None and self.type in self.BA_SENSOR_METHODS:
        self._state = self.BA_SENSOR_METHODS[self.type](ba_data) or "No BA sensor installed"
```

**Testing:** Verify all sensors still update with correct values.

---

## Priority 7: Simplify to English-Only (COMPLETED)

**Decision:** Remove all translation files and use English only in strings.json

### 7.1 Update strings.json with English text
**File:** `custom_components/kostal/strings.json`  
**Action:** Replace reference keys with actual English text and add missing error messages:
```json
{
  "title": "Kostal Piko (Legacy)",
  "config": {
    "step": {
      "user": {
        "title": "Kostal Piko Setup",
        "description": "Set up your Kostal Piko inverter",
        "data": {
          "name": "Name",
          "host": "Host (e.g., http://192.168.1.100)",
          "username": "Username",
          "password": "Password",
          "monitored_conditions": "Monitored Conditions"
        }
      }
    },
    "error": {
      "could_not_connect": "Could not connect to inverter. Check host, username, and password.",
      "host_exists": "This host is already configured.",
      "unknown_error": "Unexpected error occurred."
    },
    "abort": {
      "host_exists": "This host is already configured."
    }
  },
  "options": {
    "step": {
      "init": {
        "title": "Kostal Piko Options",
        "description": "Configure which sensors to monitor",
        "data": {
          "monitored_conditions": "Monitored Conditions"
        }
      }
    }
  }
}
```

### 7.2 Remove translations folder
**Action:** Delete the entire `custom_components/kostal/translations/` folder and its contents (en.json, es.json).  
**Why:** Simplifies maintenance and reduces unnecessary files since integration will only support English.

**Testing:** 
- Restart Home Assistant
- Try adding a new integration instance through UI
- Verify text appears correctly in config flow
- Test error messages (wrong IP, wrong password)

---

## Priority 8: Add Diagnostics Support

### 8.1 Create diagnostics.py
**File:** Create new file `custom_components/kostal/diagnostics.py`  
**Action:**
```python
"""Diagnostics support for Kostal Piko."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""
    instance = hass.data["kostal"][entry.entry_id]
    
    return {
        "entry_data": {
            "host": entry.data.get("host"),
            "username": entry.data.get("username"),
            "monitored_conditions": entry.data.get("monitored_conditions"),
        },
        "piko_info": {
            "serial": instance.piko.data.serial_number if instance.piko.data else None,
            "model": instance.piko.data.model if instance.piko.data else None,
        },
        "data_available": instance.piko.data is not None,
        "ba_data_available": instance.piko.ba_data is not None,
    }
```

**Testing:** Go to device page, click "Download diagnostics" and verify file downloads.

---

## Priority 9: Improve Unique IDs

### 9.1 Use Slugified Unique IDs
**File:** `custom_components/kostal/sensor.py`  
**Function:** `unique_id` property (line ~115)  
**Current:**
```python
return "{} {}".format(self.serial_number, self._sensor)
```
**Change to:**
```python
from homeassistant.util import slugify

@property
def unique_id(self):
    """Return unique id based on device serial and variable."""
    return f"{slugify(str(self.serial_number))}_{slugify(self.type)}"
```
**Testing:** 
- **Warning:** Changing unique IDs will create duplicate entities!
- Only implement if creating a new major version
- Or add migration logic to update entity registry

---

## Priority 10: Add Entity Categories

### 10.1 Categorize Diagnostic Sensors
**File:** `custom_components/kostal/const.py`  
**Action:** Add entity category to SENSOR_TYPES:
```python
from homeassistant.helpers.entity import EntityCategory

SENSOR_TYPES = {
    "solar_generator_power": ["Solar generator power", UnitOfPower.WATT, "mdi:solar-power", None],
    # ... power/energy sensors with None category
    "status": ["Status", None, "mdi:solar-power", EntityCategory.DIAGNOSTIC],
    "string1_voltage": ["String 1 voltage", UnitOfElectricPotential.VOLT, "mdi:current-ac", EntityCategory.DIAGNOSTIC],
    # ... mark voltage/current as diagnostic
}
```

### 10.2 Use Category in Sensor
**File:** `custom_components/kostal/sensor.py`  
**Action:** In `__init__()`:
```python
self._attr_entity_category = SENSOR_TYPES[self.type][3] if len(SENSOR_TYPES[self.type]) > 3 else None
```

**Testing:** Verify diagnostic sensors appear in separate section on device page.

---

## Testing Checklist

After each change, perform these tests:

- [ ] Integration loads without errors
- [ ] Config flow works for new installations
- [ ] All selected sensors appear and update
- [ ] Sensors show correct values
- [ ] Device page shows correct info
- [ ] Integration can be removed cleanly
- [ ] Check logs for warnings/errors
- [ ] Test with inverter offline (sensors become unavailable)
- [ ] Test with inverter back online (sensors recover)

---

## Version History

Track version changes:
- **1.2.0** - Baseline release
- **1.3.0** - Current version (English-only, removed translations) ✅
- **1.4.0** - Planned (after removing deprecated code)
- **2.0.0** - Planned (after DataUpdateCoordinator implementation)

---

## Notes

- Test each change individually before moving to the next
- Create git commits after each successful change
- Keep a backup before making changes
- Test with your actual hardware between changes
- Consider creating a dev branch for testing

---

## Future Enhancements

Ideas for future versions:
- Add support for discovery (if possible)
- Add energy dashboard integration
- Add inverter configuration entities
- Add service to refresh data on demand
- Add support for multiple inverters
- Create unit tests
- Add GitHub Actions for validation
