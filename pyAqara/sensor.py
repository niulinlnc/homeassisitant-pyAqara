from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
from datetime import timedelta
import logging

DOMAIN = 'Aqara'

_LOGGER = logging.getLogger(__name__)

# Need to use own implementation
# REQUIREMENTS =
# ['https://github.com/fooxy/homeassisitant-pyAqara/archive/v0.1-alpha.zip#pyAqara==0.1']

# Magnet Sensor need frequent polls since it's possible that ist's not
# open that long
MIN_TIME_BETWEEN_SWITCH_UPDATES = timedelta(seconds=3)
MIN_TIME_BETWEEN_MOTION_UPDATES = timedelta(seconds=3)
MIN_TIME_BETWEEN_MAGNET_UPDATES = timedelta(seconds=3)
MIN_TIME_BETWEEN_HT_UPDATES = timedelta(seconds=30)


class Sensor(Entity):
    """Representation of a Termperature / Humidity Sensor."""

    def __init__(self, deviceData, deviceName, deviceID, sensor_type):
        self.deviceData = deviceData
        self._state = None
        self.deviceName = deviceName
        self.deviceID = deviceID
        self.type = sensor_type
        self.update()

    @property
    def should_poll(self):
        """We need to poll our sensors."""
        return True

    @property
    def name(self):
        """Return the name of the sensor."""
        return '{} {}'.format(self.type, self.deviceName)

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        # return TEMP_CELSIUS
        if self.type == "temperature":
            return TEMP_CELSIUS
        elif self.type == "humidity":
            return '%'
        elif self.type == "magnet":
            return None

    def update(self):
        """ Gets the latest data and updates the state. """

        try:
            self.deviceData.data = None
            self.deviceData.SID = self.deviceID
            self.deviceData.type = self.type
            self.deviceData.update()
        except:
            _LOGGER.error(
                "Aqara Entity Failed to Update the device %s, %s, %s",
                self.deviceName, self.deviceID, self.type)

        updateValue = self.deviceData.data
        if updateValue is not None:
            self._state = updateValue


class HTSensorData(object):
    """Get data from the Bbox."""

    def __init__(self, gateway):
        """Initialize the data object."""
        self.data = None
        self.SID = None
        self.type = None
        self.gateway = gateway

    @Throttle(MIN_TIME_BETWEEN_HT_UPDATES)
    def update(self):
        """Get the latest data from the Bbox."""
        try:
            if self.type == "humidity":
                humidity = self.gateway.get_humidity(self.SID)
                # sometimes sensors are not avialable and return 0 in result,
                # filter these results
                if int(humidity) == 0:
                    self.data = None
                    _LOGGER.info("Sensor did not return humidity %s", self.SID)
                else:
                    self.data = humidity
            elif self.type == "temperature":
                temperature = self.gateway.get_temperature(self.SID)
                # sometimes sensors are not avialable and return 100 in result,
                # filter these results
                if int(temperature) == 100:
                    self.data = None
                    _LOGGER.info(
                        "Sensor did not return temperature %s", self.SID)
                else:
                    self.data = temperature
        except:
            self.data = None
            _LOGGER.error(
                "Aqara Data Failed to get data from the device %s",
                self.deviceID)


class MagnetData(object):
    """Get data from the Bbox."""

    def __init__(self, gateway):
        """Initialize the data object."""
        self.data = None
        self.SID = None
        self.type = None
        self.gateway = gateway

    @Throttle(MIN_TIME_BETWEEN_MAGNET_UPDATES)
    def update(self):
        """Get the latest data from the Bbox."""
        try:
            status = self.gateway.get_status(self.SID)
            self.data = status
        except:
            self.data = None
            _LOGGER.error(
                "Aqara Data Failed to get data from the device %s",
                self.deviceID)


class MotionData(object):
    """Get data from the Bbox."""

    def __init__(self, gateway):
        """Initialize the data object."""
        self.data = None
        self.SID = None
        self.type = None
        self.gateway = gateway

    @Throttle(MIN_TIME_BETWEEN_MOTION_UPDATES)
    def update(self):
        """Get the latest data from the Bbox."""
        try:
            status = self.gateway.get_status(self.SID)
            self.data = status
        except:
            self.data = None
            _LOGGER.error(
                "Aqara Data Failed to get data from the device %s",
                self.deviceID)


class SwitchData(object):
    """Get data from the Bbox."""

    def __init__(self, gateway):
        """Initialize the data object."""
        self.data = None
        self.SID = None
        self.type = None
        self.gateway = gateway

    @Throttle(MIN_TIME_BETWEEN_SWITCH_UPDATES)
    def update(self):
        """Get the latest data from the Bbox."""
        try:
            status = self.gateway.get_switchstatus(self.SID)
            self.data = status
        except:
            self.data = None
            _LOGGER.error(
                "Aqara Data Failed to get data from the device %s",
                self.deviceID)
