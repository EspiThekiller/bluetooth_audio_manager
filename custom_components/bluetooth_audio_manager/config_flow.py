import logging
import subprocess
import re
import time
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

def get_bluetooth_devices():
    """Scan and return a dict of available Bluetooth devices."""
    try:
        # Trigger a short scan to discover new devices
        proc = subprocess.Popen(["bluetoothctl", "scan", "on"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)
        subprocess.run(["bluetoothctl", "scan", "off"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        proc.terminate()
        
        # Get devices
        result = subprocess.run(["bluetoothctl", "devices"], capture_output=True, text=True, timeout=5)
        devices = {}
        for line in result.stdout.splitlines():
            match = re.match(r"Device ([0-9A-F:]+) (.*)", line)
            if match:
                mac, name = match.groups()
                devices[mac] = f"{name} ({mac})"
        return devices
    except Exception as e:
        _LOGGER.error(f"Error getting bluetooth devices: {e}")
        return {}

def pair_and_trust(mac_address):
    """Pair and trust a device using bluetoothctl."""
    try:
        _LOGGER.info(f"Pairing device {mac_address}...")
        subprocess.run(["bluetoothctl", "pair", mac_address], timeout=15)
        _LOGGER.info(f"Trusting device {mac_address}...")
        subprocess.run(["bluetoothctl", "trust", mac_address], timeout=5)
        return True
    except Exception as e:
        _LOGGER.error(f"Error pairing/trusting: {e}")
        return False

class BluetoothAudioManagerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Bluetooth Audio Manager."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        
        # We need to run the blocking get_bluetooth_devices in an executor
        devices = await self.hass.async_add_executor_job(get_bluetooth_devices)
        
        if not devices:
            errors["base"] = "no_devices_found"
            
        if user_input is not None:
            mac_address = user_input["mac_address"]
            name = devices.get(mac_address, mac_address)
            
            # Try to pair
            success = await self.hass.async_add_executor_job(pair_and_trust, mac_address)
            
            if success:
                # Also try to connect and reload audio immediately
                from .__init__ import connect_bluetooth, reload_audio
                await self.hass.async_add_executor_job(connect_bluetooth, mac_address)
                await reload_audio(self.hass)
                
                return self.async_create_entry(title=name, data={"mac_address": mac_address, "name": name})
            else:
                errors["base"] = "pairing_failed"

        # Create form schema
        if devices:
            data_schema = vol.Schema({
                vol.Required("mac_address"): vol.In(devices)
            })
        else:
            data_schema = vol.Schema({
                vol.Required("mac_address"): str
            })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
