import logging
import subprocess
import re

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary sensor platform."""
    mac_address = entry.data.get("mac_address")
    name = entry.data.get("name", "Bluetooth Device")

    async_add_entities([BluetoothConnectionSensor(mac_address, name, entry.entry_id)])

class BluetoothConnectionSensor(BinarySensorEntity):
    """Representation of a Bluetooth Connection Sensor."""

    def __init__(self, mac_address: str, name: str, entry_id: str) -> None:
        """Initialize the sensor."""
        self._mac_address = mac_address
        self._attr_name = f"{name} Connection"
        self._attr_unique_id = f"{mac_address}_connection"
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
        self._is_on = False
        self._device_type = "Unknown"
        self._attr_extra_state_attributes = {
            "mac_address": self._mac_address,
            "device_type": self._device_type,
        }
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry_id)},
            name=name,
            manufacturer="Bluetooth Device",
        )
        self._attr_icon = "mdi:music-note"

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return self._is_on

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This runs periodically (by default every ~30s for a standard integration if we let HA poll).
        """
        try:
            result = subprocess.run(
                ["bluetoothctl", "info", self._mac_address],
                capture_output=True,
                text=True,
                timeout=5,
            )
            # Check the output of bluetoothctl for the connection state
            if "Connected: yes" in result.stdout:
                self._is_on = True
            else:
                self._is_on = False
                
            icon_match = re.search(r"Icon:\s+(.*)", result.stdout)
            if icon_match:
                self._device_type = icon_match.group(1).strip()
            
            self._attr_extra_state_attributes = {
                "mac_address": self._mac_address,
                "device_type": self._device_type,
            }
        except subprocess.TimeoutExpired:
            _LOGGER.warning(f"Timeout checking bluetooth status for {self._mac_address}")
            self._is_on = False
        except Exception as e:
            _LOGGER.error(f"Error checking bluetooth status for {self._mac_address}: {e}")
            self._is_on = False
