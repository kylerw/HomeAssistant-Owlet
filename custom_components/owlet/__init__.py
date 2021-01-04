import logging
import voluptuous as vol
from owletpy.OwletPy import OwletPy

from homeassistant.const import (CONF_USERNAME, CONF_PASSWORD, CONF_NAME)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.discovery import load_platform

from .const import SENSOR_MOVEMENT, SENSOR_BASE_STATION, SENSOR_HEART_RATE, \
    SENSOR_OXYGEN_LEVEL, SENSOR_BATTERY_LEVEL, SENSOR_SOCK_CONNECTION, \
    SENSOR_SOCK_ON, SENSOR_BATTERY_CHARGING

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'owlet'

SENSOR_TYPES = [
    SENSOR_OXYGEN_LEVEL,
    SENSOR_HEART_RATE,
    SENSOR_BASE_STATION,
    SENSOR_MOVEMENT,
    SENSOR_BATTERY_LEVEL,
    SENSOR_SOCK_CONNECTION,
    SENSOR_SOCK_ON,
    SENSOR_BATTERY_CHARGING
]

CONF_OWLET_REGION = 'region'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_OWLET_REGION, default='world'): cv.string,
        vol.Optional(CONF_NAME): cv.string
    }),
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):

    username = config[DOMAIN][CONF_USERNAME]
    password = config[DOMAIN][CONF_PASSWORD]
    region = config[DOMAIN].get(CONF_OWLET_REGION)
    name = config[DOMAIN].get(CONF_NAME)

    try:
        device = OwletPy(username, password, region)
    except KeyError:
        _LOGGER.error('Owlet authentication failed.  Please verify your '
                      'credentials are correct.')
        return False
    except:
        _LOGGER.error('Error')
        return False

    device.update_properties()

    if not name:
        name = '{}\'s Owlet'.format(device.baby_name)
    
    hass.data[DOMAIN] = OwletDevice(device, name, SENSOR_TYPES)

    load_platform(hass, 'sensor', DOMAIN, {}, config)
    load_platform(hass, 'binary_sensor', DOMAIN, {}, config)

    return True


class OwletDevice():
    """Represents a configured Owlet device."""

    def __init__(self, device, name, monitor):
        """Initialize device."""
        self.name = name
        self.monitor = monitor
        self.device = device
