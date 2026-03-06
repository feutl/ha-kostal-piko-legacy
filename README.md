# Kostal Piko Legacy - Home Assistant Integration

A Home Assistant custom component for monitoring Kostal Piko solar inverters (NOT the Plenticore models).

> **Note:** This integration is for legacy Kostal Piko inverters. If you have a Kostal Plenticore inverter, please use a different integration.

## About

This custom component integrates Kostal Piko inverters with Home Assistant, providing real-time monitoring of power generation, energy production, voltage, current, and system status.

**Based on code from:**
- https://github.com/gieljnssns/kostalpiko-sensor-homeassistant
- https://github.com/rcasula/kostalpiko-homeassistant

## Features

- **Config Flow Support**: Easy setup through the Home Assistant UI
- **Multiple Sensor Types**: Monitor various parameters of your inverter
- **BA Sensor Support**: Track consumption data when BA sensor is installed
- **Automatic Device Registration**: Creates a device entity with all sensors grouped together
- **String Monitoring**: Support for up to 3 PV strings
- **Three-Phase Monitoring**: Individual monitoring of L1, L2, and L3 phases

## Compatibility

This integration works with Kostal Piko inverters that have a web interface accessible at:
```
http://pvserver:<YOUR_PASSWORD>@<YOUR_INVERTER_IP>/index.fhtml
```

Your inverter's web interface should look similar to this:

![Kostal Piko Web Interface](https://github.com/gieljnssns/kostalpiko-sensor-homeassistant/blob/master/img/Schermafbeelding%202020-03-30%20om%2011.25.18.png?raw=true)

If your web interface looks different, this integration may not work with your inverter model.

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL and select "Integration" as the category
6. Click "Install"
7. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/kostal` folder to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

### UI Configuration (Recommended)

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for **Kostal Piko**
4. Enter your inverter details:
   - **Name**: A friendly name for your inverter (default: "Kostal Piko")
   - **Host**: The IP address of your inverter (format: `http://192.168.x.x`)
   - **Username**: Usually `pvserver`
   - **Password**: Your inverter's web interface password
   - **Monitored Conditions**: Select the sensors you want to track

### YAML Configuration (Legacy)

You can still configure the integration via `configuration.yaml`:

```yaml
sensor:
  - platform: kostal
    host: !secret kostal_host  # "http://192.168.x.x"
    username: !secret kostal_username  # Usually "pvserver"
    password: !secret kostal_password
    monitored_conditions:
      - solar_generator_power  # Only available with BA sensor
      - consumption_phase_1    # Only available with BA sensor
      - consumption_phase_2    # Only available with BA sensor
      - consumption_phase_3    # Only available with BA sensor
      - current_power
      - total_energy
      - daily_energy
      - string1_voltage
      - string1_current
      - string2_voltage
      - string2_current
      - string3_voltage        # If you have 3 strings
      - string3_current        # If you have 3 strings
      - l1_voltage
      - l1_power
      - l2_voltage
      - l2_power
      - l3_voltage
      - l3_power
      - status
```

## Available Sensors

### Basic Sensors
- **Current power** - Current power output (W)
- **Total energy** - Total energy produced (kWh)
- **Daily energy** - Energy produced today (kWh)
- **Status** - Inverter status

### String Sensors (PV Panels)
- **String 1/2/3 voltage** - DC voltage from each string (V)
- **String 1/2/3 current** - DC current from each string (A)

### Phase Sensors (AC Output)
- **L1/L2/L3 voltage** - AC voltage per phase (V)
- **L1/L2/L3 power** - AC power output per phase (W)

### BA Sensor Readings (Optional)
These sensors require a BA (Battery/consumption Analysis) sensor to be installed on your inverter:
- **Solar generator power** - Total power from solar panels (W)
- **Consumption phase 1/2/3** - Power consumption per phase (W)

## Update Frequency

The integration updates sensor values every 30 seconds to avoid overloading the inverter's web interface.

## Troubleshooting

### Cannot Connect
- Verify your inverter is accessible at `http://<YOUR_IP>/index.fhtml`
- Check that your username and password are correct
- Ensure your inverter's web interface is enabled

### BA Sensor Shows "No BA sensor installed"
This is normal if you don't have a BA sensor. Either don't monitor these sensors or ignore the message.

### Sensors Not Updating
- Check Home Assistant logs for errors
- Verify network connectivity to the inverter
- Ensure the inverter is online and producing power

## Requirements

- Home Assistant 2021.12 or newer
- Python package `kostalpiko>=0.6` (automatically installed)

## Dependencies

This integration depends on the [kostalpiko](https://github.com/rcasula/kostalpiko) Python library for communicating with Kostal Piko inverters.

**Library Information:**
- **Package**: `kostalpiko` (available on [PyPI](https://pypi.org/project/kostalpiko/))
- **Source**: https://github.com/rcasula/kostalpiko
- **Maintainer**: [@rcasula](https://github.com/rcasula)
- **Functionality**: Handles HTTP communication and HTML parsing of the inverter's web interface

The library is automatically installed by Home Assistant when the integration is set up.

## Version

Current version: **1.3.1-rc.3**

## Credits

This integration is based on the excellent work from:
- [@gieljnssns](https://github.com/gieljnssns) - [kostalpiko-sensor-homeassistant](https://github.com/gieljnssns/kostalpiko-sensor-homeassistant)
- [@rcasula](https://github.com/rcasula) - [kostalpiko-homeassistant](https://github.com/rcasula/kostalpiko-homeassistant)

## Development & Maintenance

**Important Note:** The initial code for this integration was provided by the repositories mentioned above. All subsequent changes and updates to this codebase have been performed using vibe-coding techniques or with the assistance of AI agents. 

This approach was chosen as the maintainer is not a coder. Users should be aware of this development methodology and are encouraged to report any issues or contribute improvements through the issue tracker.

### For Maintainers

If you're creating a new release, please follow the workflow documented in [RELEASE.md](RELEASE.md) to ensure proper versioning, tagging, and GitHub release creation.

## License

See [LICENSE](LICENSE) file for details.
