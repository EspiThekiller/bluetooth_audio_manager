import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN
from .__init__ import connect_bluetooth, disconnect_bluetooth, reload_audio

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    mac_address = entry.data.get("mac_address")
    name = entry.data.get("name", "Bluetooth Device")

    async_add_entities([BluetoothConnectionSwitch(hass, mac_address, name, entry.entry_id)])

class BluetoothConnectionSwitch(SwitchEntity):
    """Representation of a Bluetooth Connection Switch."""

    def __init__(self, hass: HomeAssistant, mac_address: str, name: str, entry_id: str) -> None:
        """Initialize the switch."""
        self.hass = hass
        self._mac_address = mac_address
        self._attr_name = f"{name} Connect"
        self._attr_unique_id = f"{mac_address}_switch"
        self._is_on = False
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry_id)},
            name=name,
            manufacturer="Bluetooth Device",
        )
        self._attr_icon = "mdi:music-note"

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return self._is_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        success = await self.hass.async_add_executor_job(connect_bluetooth, self._mac_address)
        if success:
            self._is_on = True
            self.async_write_ha_state()
            # Reload audio after successful connection
            await reload_audio(self.hass)
        else:
            _LOGGER.error(f"Failed to turn on (connect) {self._attr_name}")

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        success = await self.hass.async_add_executor_job(disconnect_bluetooth, self._mac_address)
        if success:
            self._is_on = False
            self.async_write_ha_state()
        else:
            _LOGGER.error(f"Failed to turn off (disconnect) {self._attr_name}")

    async def async_update(self) -> None:
        """Update the state of the switch based on the binary_sensor or bluetoothctl info."""
        # For a more robust approach, the switch can also poll `bluetoothctl info` 
        # or rely on the binary_sensor's state. Since we just want simple syncing, 
        # let's do a quick poll to keep it in sync with reality if changed externally.
        import subprocess
        
        def _check_status():
            return subprocess.run(
                ["bluetoothctl", "info", self._mac_address],
                capture_output=True,
                text=True,
                timeout=5
            )

        try:
            result = await self.hass.async_add_executor_job(_check_status)
            if hasattr(result, 'stdout') and "Connected: yes" in result.stdout:
                self._is_on = True
            else:
                self._is_on = False
        except Exception as e:
            pass
