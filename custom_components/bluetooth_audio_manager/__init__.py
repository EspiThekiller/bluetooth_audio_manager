import logging
import os
import aiohttp
import subprocess

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Bluetooth Audio Manager component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Bluetooth Audio Manager from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    async def handle_connect_and_reload(call):
        mac = call.data.get("mac_address", entry.data.get("mac_address"))
        if mac:
            await hass.async_add_executor_job(connect_bluetooth, mac)
            await reload_audio(hass)

    hass.services.async_register(DOMAIN, "connect_and_reload", handle_connect_and_reload)
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        if entry.entry_id in hass.data[DOMAIN]:
            hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

def connect_bluetooth(mac_address):
    """Connect to a bluetooth device."""
    try:
        _LOGGER.info(f"Connecting to Bluetooth device {mac_address}...")
        result = subprocess.run(
            ["bluetoothctl", "connect", mac_address],
            capture_output=True,
            text=True,
            timeout=15
        )
        if result.returncode != 0 or "Failed to connect" in result.stdout:
            _LOGGER.error(f"Failed to connect to {mac_address}: {result.stdout} {result.stderr}")
            return False
        _LOGGER.info(f"Successfully connected to {mac_address}")
        return True
    except subprocess.TimeoutExpired:
        _LOGGER.error(f"Timeout while connecting to {mac_address}")
        return False
    except Exception as e:
        _LOGGER.error(f"Error connecting to bluetooth: {e}")
        return False

def disconnect_bluetooth(mac_address):
    """Disconnect from a bluetooth device."""
    try:
        _LOGGER.info(f"Disconnecting from Bluetooth device {mac_address}...")
        result = subprocess.run(
            ["bluetoothctl", "disconnect", mac_address],
            capture_output=True,
            text=True,
            timeout=15
        )
        if result.returncode != 0:
            _LOGGER.error(f"Failed to disconnect from {mac_address}: {result.stdout} {result.stderr}")
            return False
        _LOGGER.info(f"Successfully disconnected from {mac_address}")
        return True
    except subprocess.TimeoutExpired:
        _LOGGER.error(f"Timeout while disconnecting from {mac_address}")
        return False
    except Exception as e:
        _LOGGER.error(f"Error disconnecting from bluetooth: {e}")
        return False

async def reload_audio(hass: HomeAssistant):
    """Reload audio using Supervisor API."""
    try:
        supervisor_token = os.environ.get("SUPERVISOR_TOKEN")
        if supervisor_token:
            _LOGGER.info("Reloading audio via Supervisor API...")
            headers = {"Authorization": f"Bearer {supervisor_token}"}
            async with aiohttp.ClientSession() as session:
                async with session.post("http://supervisor/audio/reload", headers=headers) as resp:
                    _LOGGER.info(f"Audio reload status: {resp.status}")
        else:
            _LOGGER.warning("No SUPERVISOR_TOKEN found. Are you running Home Assistant OS/Supervised?")
    except Exception as e:
        _LOGGER.error(f"Error reloading audio: {e}")
