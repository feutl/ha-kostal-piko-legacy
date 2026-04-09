# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0-alpha.3] - 2026-04-09

### Fixed
- **CRITICAL FIX**: Resolved ConfigEntryError that caused all entities to be unavailable
- Fixed timing issue with `async_config_entry_first_refresh()` being called in wrong state
- Coordinator first refresh now happens during setup phase (SETUP_IN_PROGRESS) not after (LOADED)
- Changed from background task to awaited startup sequence

### Changed
- Removed unnecessary asyncio import
- `start_up()` is now awaited in `async_setup_entry` instead of running as background task
- Improved startup logging to show coordinator initialization status

### Technical Details
The issue was that `async_config_entry_first_refresh()` must be called while the config entry
is in `ConfigEntryState.SETUP_IN_PROGRESS`, but we were calling it in a background task after
`async_setup_entry` returned, when the state was already `ConfigEntryState.LOADED`.

## [1.4.0-alpha.2] - 2026-04-09

### Fixed
- Added extensive debug logging to diagnose "all entities unavailable" issue
- Improved error handling in DataUpdateCoordinator with attribute checks
- Better handling of missing ba_data attribute (for inverters without BA sensor)
- More defensive checks for Piko object attributes after update

### Debug
- Added detailed logging in coordinator _async_update_data method
- Added logging in sensor state property to track data flow
- Logs now show when data/ba_data are None vs not present
- Better exception logging with full tracebacks

### Notes
- This release includes debug logging to help diagnose availability issues
- Please check Home Assistant logs (Configuration → Logs) and report findings
- Set logger level to debug for 'custom_components.kostal' for detailed output

## [1.4.0-alpha.1] - 2026-04-08

### Added
- Implemented DataUpdateCoordinator for modern, efficient data fetching
- Automatic retry logic for failed inverter communication
- Better error handling with UpdateFailed exceptions

### Changed
- **BREAKING**: Major refactoring to use DataUpdateCoordinator pattern
- PikoSensor now extends CoordinatorEntity for automatic updates
- Removed manual async_update() and _update() methods from sensors
- Using raw Piko class from library instead of PikoHolder wrapper
- State property now computes directly from coordinator data
- More efficient updates - coordinator prevents duplicate fetches

### Improved
- Added comprehensive error handling to sensor updates
- Sensors now properly show "unavailable" when inverter is offline
- Better logging of errors with sensor type and exception details
- Simplified sensor code following modern HA patterns
- Automatic update scheduling via coordinator (30-second intervals)

### Notes
- This is an ALPHA release for testing purposes
- piko_holder.py is now unused but kept for reference
- Requires testing with real Kostal Piko inverter
- Please report any issues on GitHub

## [1.3.1] - 2026-03-09

### Fixed
- Options flow compatibility for Home Assistant 2026.3.0
- Deprecated `hass.loop.create_task()` replaced with `asyncio.create_task()`
- Deprecated `hass.add_job()` replaced with `hass.async_create_task()`
- Removed deprecated `@Throttle` decorator from sensor updates
- Removed deprecated `CONNECTION_CLASS` from config flow

### Changed
- Updated to current Home Assistant 2026 best practices
- Cleaner async code following modern patterns
- Removed unused imports

### Improved
- Better code maintainability
- More future-proof implementation
- Follows latest Home Assistant development guidelines

### Testing
- Verified with Home Assistant 2026.3.0
- All sensors working correctly
- Config flow and options flow tested successfully

### Documentation
- Updated README.md with version 1.3.1 and "What's New" section
- Reorganized IMPROVEMENTS.md to show completed work and future roadmap
- Enhanced RELEASE.md with concrete examples and command references
- Created comprehensive .github/copilot-instructions.md for AI assistant guidance
- All documentation meets quality standards (clear language, accurate versioning, proper formatting)

## [1.3.1-rc.6] - 2026-03-06

### Fixed
- Options flow compatibility for Home Assistant 2026.3.0

## [1.3.1-rc.5] - 2026-03-06

### Fixed
- Options flow initialization error when opening Configure

## [1.3.1-rc.4] - 2026-03-06

### Added
- Options flow to update monitored sensors after setup

## [1.3.1-rc.3] - 2026-03-06

### Changed
- Replaced deprecated `hass.loop.create_task()` with `asyncio.create_task()`
- Replaced deprecated `hass.add_job()` with `hass.async_create_task()`
- Removed deprecated `@Throttle` decorator from sensor updates (throttling still handled by piko_holder)
- Removed unused imports: `time`, `Throttle`, and `MIN_TIME_BETWEEN_UPDATES`

### Improved
- Updated to current Home Assistant best practices
- Cleaner code following modern async patterns

## [1.3.1-rc.1] - 2026-03-06

### Added
- .gitignore with standard Python, venv, and OS ignores
- VS Code settings to silence missing import diagnostics for Home Assistant

### Changed
- Bumped integration version to 1.3.1-rc.1 for this pre-release

### Testing
- Verified release installation works as expected (2026-03-06)

## [1.3.0] - 2026-03-05

### Changed
- Simplified integration to English-only
- Removed translations folder and language files (en.json, es.json)
- Updated strings.json with complete English text and proper error messages

### Improved
- Reduced file complexity
- Easier maintenance going forward
- Clearer error messages in config flow

### Added
- Options flow strings in strings.json for future enhancements
- Complete English descriptions for all config flow steps

## [1.2.0] - 2026-03-05

### Added
- Initial baseline release
- Config flow support for easy UI-based setup
- Support for multiple sensor types (power, energy, voltage, current)
- BA sensor support for consumption monitoring
- Device registration with all sensors grouped
- String monitoring (up to 3 PV strings)
- Three-phase monitoring (L1, L2, L3)
- 30-second update interval
- Proper manifest.json with integration metadata

### Documentation
- Comprehensive README with installation and configuration instructions
- Credits to original repositories
- Development methodology disclosure

---

Based on code from:
- [@gieljnssns](https://github.com/gieljnssns/kostalpiko-sensor-homeassistant)
- [@rcasula](https://github.com/rcasula/kostalpiko-homeassistant)
