# Bluetooth Audio Manager for Home Assistant

A custom component for Home Assistant that allows you to easily manage, pair, and connect Bluetooth audio devices directly from the Home Assistant interface. This integration solves common audio issues when connecting Bluetooth speakers to Home Assistant OS/Supervised by automatically reloading the audio subsystem when a device connects.

![Icon](icon.svg)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=EspiThekiller&repository=bluetooth_audio_manager&category=integration)
[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=bluetooth_audio_manager)

## Features

- **UI Configuration (Config Flow):** Easily scan and select nearby Bluetooth devices from the Home Assistant Integrations UI. No YAML required!
- **Automatic Pairing & Trusting:** Automatically pairs and trusts the selected Bluetooth device during setup via `bluetoothctl`.
- **Connection Switch:** Provides a switch entity to manually connect or disconnect your Bluetooth device.
- **Connection Sensor:** Provides a binary sensor entity that monitors the real-time connectivity status of your device.
- **Audio Reload Integration:** Uses the Home Assistant Supervisor API to automatically reload audio (`http://supervisor/audio/reload`) upon connection, ensuring the audio output switches correctly to the Bluetooth device.
- **Custom Service:** Exposes a `bluetooth_audio_manager.connect_and_reload` service that you can call from your automations or scripts.

## Prerequisites

- Home Assistant OS or Home Assistant Supervised (requires `SUPERVISOR_TOKEN` to reload audio).
- The host must have Bluetooth capabilities and `bluetoothctl` installed and accessible.

## Installation

### Manual Installation

1. Download or clone this repository.
2. Copy the `bluetooth_audio_manager` folder into your Home Assistant's `custom_components` directory (`/config/custom_components/`).
3. Restart Home Assistant.
4. Go to **Settings** > **Devices & Services** > **Add Integration**.
5. Search for "Bluetooth Audio Manager" and follow the UI prompts to scan and select your Bluetooth device.

### HACS Installation (Recommended)

*If you add this repository to HACS:*
1. Open HACS in your Home Assistant.
2. Go to Integrations > 3 dots (top right) > Custom repositories.
3. Add the URL to this GitHub repository and select `Integration` as the category.
4. Click Download.
5. Restart Home Assistant.
6. Set it up via **Settings** > **Devices & Services** > **Add Integration**.

## Services

### `bluetooth_audio_manager.connect_and_reload`

Connects to the specified Bluetooth device and triggers an audio reload on the Supervisor.

| Data attribute | Optional | Description |
| ---------------- | -------- | ----------- |
| `mac_address`    | Yes      | The MAC address of the Bluetooth device (e.g., `00:11:22:33:44:55`). If omitted, it will use the MAC address of the configured device. |

## Entities Created

For each configured device, the following entities are created:
- `switch.<device_name>_connect`: Toggle to connect or disconnect the device.
- `binary_sensor.<device_name>_connection`: Shows whether the device is currently connected or not.

*(Note: Both entities come with a `mdi:music-note` icon by default!)*

## Troubleshooting

- **No devices found during setup:** Ensure that your Home Assistant host has Bluetooth enabled and that the target device is in pairing mode.
- **Audio not reloading:** This feature requires Home Assistant OS or Supervised. If you are running Home Assistant Container or Core, the Supervisor API is not available.
