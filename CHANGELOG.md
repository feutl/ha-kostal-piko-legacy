# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
