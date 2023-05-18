#openai_response_chrome_ext_helper
import asyncio
import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.input_text import DOMAIN as INPUT_TEXT_DOMAIN, SERVICE_SET_VALUE
from homeassistant.const import CONF_PLATFORM
from homeassistant.core import callback
from homeassistant.helpers import discovery
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_state_change

_LOGGER = logging.getLogger(__name__)

DOMAIN = "example_integration"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_PLATFORM): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass, config):
    """Set up the example integration."""

    @callback
    def async_text_entered(entity, old_state, new_state):
        """Handle text entered event."""
        if new_state.state != old_state.state:
            text_value = new_state.state
            _LOGGER.info("Text entered: %s", text_value)
            # Execute JavaScript function with the text value
            hass.async_create_task(send_message(text_value))

    async def send_message(text_value):
        """Execute JavaScript function sendMessage(text_value)."""
        # Perform the necessary steps to execute the JavaScript function here
        # For example, using the appropriate service or integration
        # This implementation assumes you have a service or integration that executes JavaScript code
        # Replace the following code with the actual implementation
        await hass.services.async_call(
            "browser_mod",
            "command",
            {
                "command": "execute_js",
                "entity_id": "browser_mod.target_entity_id",
                "arg": f"sendMessage('{text_value}');",
            },
        )
    await discovery.async_load_platform(
        hass, INPUT_TEXT_DOMAIN, DOMAIN, {}, config
    )  # Load input_text platform

    async_track_state_change(
        hass, f"{INPUT_TEXT_DOMAIN}.{DOMAIN}", async_text_entered
    )  # Track state changes of the input_text entity

    return True
