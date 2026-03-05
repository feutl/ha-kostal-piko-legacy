# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
