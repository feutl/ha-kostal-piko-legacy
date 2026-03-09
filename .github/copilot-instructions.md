# GitHub Copilot Instructions - Kostal Piko Legacy Integration

## Project Overview

This is a Home Assistant custom component for legacy Kostal Piko solar inverters (NOT Plenticore models). The integration provides real-time monitoring of power generation, energy production, voltage, current, and system status through local polling of the inverter's web interface.

**Repository:** feutl/ha-kostal-piko-legacy  
**Language:** Python 3  
**Framework:** Home Assistant Integration  
**Integration Type:** Device (local polling)  
**Update Interval:** 30 seconds

## Project Structure

```
custom_components/kostal/
├── __init__.py          # Integration setup and entry point
├── config_flow.py       # UI configuration (config flow + options flow)
├── const.py             # Constants and sensor type definitions
├── manifest.json        # Integration metadata
├── piko_holder.py       # Data fetching and caching logic
├── sensor.py            # Sensor entity implementation
└── strings.json         # UI strings (English only)
```

## Coding Standards

### Home Assistant Compatibility

- **Target Version:** Home Assistant 2026.3.0+
- **NO deprecated code:** This integration has been modernized to remove all deprecations
- Follow Home Assistant's current best practices and style guide
- Use modern async patterns with `asyncio` instead of `hass.loop`

### Code Style

1. **Use type hints** wherever possible
2. **Follow PEP 8** style guidelines
3. **Use descriptive variable names** 
4. **Add docstrings** to all functions and classes
5. **Log appropriately:**
   - Use `_LOGGER.debug()` for detailed operational info
   - Use `_LOGGER.info()` for startup/shutdown events
   - Use `_LOGGER.error()` for errors
   - Use `_LOGGER.warning()` for recoverable issues

### Modern Patterns to Use

✅ **DO USE:**
```python
import asyncio
asyncio.create_task(...)
hass.async_create_task(...)
hass.async_add_executor_job(...)
async def async_setup_entry(...)
await hass.config_entries.async_forward_entry_setups(...)
```

❌ **DO NOT USE (Deprecated):**
```python
hass.loop.create_task(...)        # Use asyncio.create_task()
hass.add_job(...)                 # Use hass.async_create_task()
@Throttle(...)                    # Use DataUpdateCoordinator
CONNECTION_CLASS                  # Removed in HA 2022+
async_setup_platforms()           # Use async_forward_entry_setups()
```

## Key Implementation Details

### Data Flow

1. **Entry Setup** (`__init__.py`):
   - ConfigEntry triggers `async_setup_entry()`
   - Creates `KostalInstance` with `PikoHolder`
   - Starts async task to fetch initial data
   - Forwards setup to sensor platform

2. **Sensor Creation** (`sensor.py`):
   - `async_setup_entry()` receives dispatcher signal
   - Creates `PikoSensor` entities for monitored conditions
   - Each sensor registers with device info

3. **Data Updates** (`piko_holder.py`):
   - Throttled updates every 30 seconds
   - Fetches data from inverter HTTP interface
   - Caches data for sensors to access

### Configuration Flow

**Two-part flow:**
1. **Config Flow** (`async_step_user`): Initial setup with host, credentials, sensors
2. **Options Flow** (`async_step_init`): Update monitored sensors after setup

**Validation:**
- Checks for duplicate hosts
- Validates connection by fetching inverter info
- Returns clear error messages to user

### Device Registration

All sensors are grouped under a single device:
- Device ID: Serial number from inverter
- Manufacturer: "Kostal"
- Model: From inverter info
- All sensors share same device identifier

### Sensor Types

**Standard Sensors:**
- Current power, total energy, daily energy
- String 1/2/3 voltage and current
- L1/L2/L3 voltage and power
- Status

**BA Sensor (optional hardware):**
- Solar generator power
- Consumption phase 1/2/3

## Testing Guidelines

### Before Any Commit

1. **Verify integration loads:** Check HA logs for errors
2. **Test config flow:** Add integration through UI
3. **Test options flow:** Update sensors via Configure button
4. **Check sensors:** Verify all selected sensors appear and update
5. **Review logs:** No errors, warnings, or deprecation notices

### Test Scenarios

- Fresh installation via UI
- Options flow to add/remove sensors
- Integration reload
- Home Assistant restart
- Network disconnection (sensors should gracefully handle)
- Inverter offline (should show unavailable, not error)

## Release Process

**Follow this order strictly** (documented in RELEASE.md):

1. Update version in `manifest.json` and `__init__.py`
2. Update CHANGELOG.md with changes
3. Commit and push changes
4. Create git tag: `git tag vX.X.X`
5. Push tag: `git push origin vX.X.X`
6. Create GitHub release (use `--prerelease` for rc/beta)

**Version Format:**
- Stable: `1.3.1`
- Release candidate: `1.3.1-rc.1`
- Beta: `1.3.1-beta.1`

## Common Tasks

### Adding a New Sensor Type

1. Add to `SENSOR_TYPES` in `const.py`
2. Add handling in `sensor.py` `_update()` method
3. Update documentation in README.md
4. Test with config flow and options flow

### Updating Dependencies

1. Update `requirements` in `manifest.json`
2. Test thoroughly - external library changes can break things
3. Document in CHANGELOG.md

### Fixing Bugs

1. Reproduce the issue locally
2. Add logging to understand the problem
3. Fix and test
4. Update CHANGELOG.md
5. Consider adding error handling for similar future issues

## Documentation

### Files to Update

- **CHANGELOG.md:** ALL changes, following Keep a Changelog format
- **README.md:** User-facing features and setup instructions
- **IMPROVEMENTS.md:** Technical roadmap and completed work
- **RELEASE.md:** Release process documentation

### Documentation Standards

- Use clear, concise language
- Include code examples where helpful
- Keep README beginner-friendly
- Keep technical details in IMPROVEMENTS.md
- Always date entries in CHANGELOG.md

## Known Limitations

1. **No DataUpdateCoordinator:** Still uses manual throttling (future improvement)
2. **No diagnostics:** No device diagnostics integration yet
3. **Limited error handling:** Network errors could be handled more gracefully
4. **No retry logic:** Failed updates don't automatically retry

## External Dependencies

- **kostalpiko library:** Handles low-level HTTP communication with inverter
- Must maintain compatibility with library's API
- Library handles basic data parsing

## Useful Commands

```bash
# Activate virtual environment (Windows)
.venv\Scripts\Activate.ps1

# Check Home Assistant version
hass --version

# View logs
# In HA UI: Settings -> System -> Logs

# Test locally with Home Assistant Core
# (Configure config_flow.py to allow local testing)
```

## Future Improvements

See IMPROVEMENTS.md for detailed roadmap. Priority areas:
1. Implement DataUpdateCoordinator pattern
2. Add comprehensive error handling
3. Add device diagnostics support
4. Consider adding configuration for update interval

## Notes for AI Assistants

- Always check current Home Assistant version compatibility
- Verify no deprecated patterns are introduced
- Follow existing code style and patterns
- Test suggested changes thoroughly
- Update documentation when making changes
- Consider backward compatibility for existing users
- This integration targets 2026.x Home Assistant releases
