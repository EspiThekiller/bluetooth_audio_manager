# Bluetooth Audio Manager for Home Assistant

A custom component for Home Assistant that allows you to easily manage, pair, and connect Bluetooth audio devices directly from the Home Assistant interface. This integration solves common audio issues when connecting Bluetooth speakers to Home Assistant OS/Supervised by automatically reloading the audio subsystem when a device connects.

![Icon](icon.svg)

### 1. Install via HACS
*(Note: Make sure your GitHub repository is **Public**. If it is private, HACS won't be able to find it).*

Click the button below to open HACS and automatically add this repository to your Home Assistant. If the button fails, you can manually add the URL `https://github.com/EspiThekiller/bluetooth_audio_manager` in HACS (Integrations > 3 dots > Custom repositories).

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=EspiThekiller&repository=bluetooth_audio_manager&category=integration)

***

### 2. Add and Configure Integration
Once you have installed the component from HACS and **restarted Home Assistant**, click the button below to open the setup flow and start pairing your Bluetooth audio devices.

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=bluetooth_audio_manager)

## Features

- **UI Configuration (Config Flow):** Easily scan and select nearby Bluetooth devices straight from the Integrations UI. No YAML configuration required!
- **Automatic Pairing & Trusting:** Automatically pairs and trusts the selected Bluetooth device during setup via `bluetoothctl`.
- **Connection Switch:** Provides a switch entity so you can manually connect or disconnect your Bluetooth device at any time.
- **Connection Sensor:** Provides a binary sensor entity that monitors the real-time connectivity status of your device.
- **Integrated Audio Reload:** Uses the Home Assistant Supervisor API to automatically reload audio (`http://supervisor/audio/reload`) upon connection, ensuring the sound output correctly switches to the Bluetooth device.
- **Custom Service:** Exposes the `bluetooth_audio_manager.connect_and_reload` service, perfectly suited to be called from your automations and scripts.

## Prerequisites

- Home Assistant OS or Home Assistant Supervised (`SUPERVISOR_TOKEN` is required to reload audio).
- The host system (where Home Assistant runs) must have Bluetooth capabilities and the `bluetoothctl` tool installed and accessible.

## Manual Installation

1. Download or clone this repository.
2. Copy the `bluetooth_audio_manager` folder into your Home Assistant's `custom_components` directory (`/config/custom_components/`).
3. Restart Home Assistant.
4. Go to **Settings** > **Devices & Services** > **Add Integration**.
5. Search for "Bluetooth Audio Manager" and follow the on-screen instructions to scan and select your Bluetooth device.

## Services

### `bluetooth_audio_manager.connect_and_reload`

Connects to the specified Bluetooth device and forces an audio reload on the Supervisor.

| Attribute | Optional | Description |
| --------- | -------- | ----------- |
| `mac_address` | Yes | The MAC address of the Bluetooth device (e.g., `00:11:22:33:44:55`). If omitted, it will use the default MAC address configured in the integration. |

## Entities Created

For each configured device, the following entities are created:
- `switch.<device_name>_connect`: A switch to toggle the device connection on or off.
- `binary_sensor.<device_name>_connection`: Indicates whether the device is currently connected or not.

*(Note: Both entities come with a `mdi:music-note` icon by default).*

## Troubleshooting

- **No devices found during setup:** Ensure that the Home Assistant host has Bluetooth turned on and that the speaker or headset you want to add is in pairing mode.
- **Audio not reloading after connection:** This feature requires Home Assistant OS or Supervised. If you are running a pure Home Assistant Container or Core setup, the Supervisor API is not available.
