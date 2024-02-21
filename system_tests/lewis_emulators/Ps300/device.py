from collections import OrderedDict
from .states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedPs300(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.hv = False
        self._voltage = 0.0
        self._voltage_limit = 100
        self.current_limit = 5
        self._current_trip_limit = 10
        self._current = 0
        self.current_tripped = False
        self.voltage_tripped = False

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

    def clear(self):
        if self.voltage < self.voltage_limit:
            self.voltage_tripped = False
        if self.current < self.current_trip_limit:
            self.current_tripped = False

    def set_voltage(self, voltage):
        self._voltage = voltage
        self._check_voltage_limit()

    def set_current(self, current):
        self._current = current
        self._check_current_limit(self)

    def get_limit_exceeded(self):
        return self.current_limit < self._current

    def set_current_trip_limit(self, limit):
        self._current_trip_limit = limit
        self._check_current_limit(self)

    def set_voltage_limit(self, limit):
        self._voltage_limit = limit
        self._check_voltage_limit(self)

    def _check_current_trip_limit(self):
        if self._current_trip_limit < self._current:
            self.current_tripped = True

    def get_current_tripped(self):
        return self.device._current_tripped

    def get_voltage_tripped(self):
        return self.device._voltage_tripped

    def _check_voltage_limit(self):
        if self._voltage_limit < self._voltage:
            self.voltage_tripped = True




